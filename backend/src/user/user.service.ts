import {
  Injectable,
  NotFoundException,
  BadRequestException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User_Accounts } from './entities/user.entity';
import { CreateUserDto, ImportUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';
import { ImportExpertiseDto } from './dto/import-expertise.dto';
import { Program } from 'src/programs/entities/program.entity';
import { Course } from 'src/courses/entities/course.entity';
import { UserExpertise } from './entities/user_expertise.entity';
import * as bcrypt from 'bcrypt';

export interface ImportError {
  row: number;
  error: string;
  email?: string;
  data?: any;
}

export interface ImportResult {
  success: number;
  failed: number;
  errors: ImportError[];
}

@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User_Accounts)
    private readonly userRepository: Repository<User_Accounts>,
    @InjectRepository(Program)
    private readonly programRepository: Repository<Program>,
    @InjectRepository(Course)
    private readonly courseRepository: Repository<Course>,
    @InjectRepository(UserExpertise)
    private readonly userExpertiseRepository: Repository<UserExpertise>,
  ) {}

  async create(createUserDto: CreateUserDto): Promise<User_Accounts> {
    const user = this.userRepository.create({
      ...createUserDto,
      is_active: createUserDto.is_active ?? true,
    });

    return await this.userRepository.save(user);
  }

  async findAll(): Promise<User_Accounts[]> {
    return await this.userRepository.find({
      relations: [
        'institute',
        'program',
        'expertise',
        'expertise.course', // ✅ include course details
        // 'other_expertise',
        // 'other_expertise.course',
      ], // eager load relations if needed
    });
  }

  async findOne(id: number): Promise<User_Accounts> {
    const user = await this.userRepository.findOne({
      where: { id },
      relations: ['institute', 'program'],
    });
    if (!user) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }
    return user;
  }

  async update(
    id: number,
    updateUserDto: UpdateUserDto,
  ): Promise<User_Accounts> {
    const user = await this.userRepository.findOne({
      where: { id },
      relations: ['program', 'institute'],
    });

    if (!user) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }

    if (updateUserDto.email !== undefined) {
      const email = updateUserDto.email.trim().toLowerCase();

      const existingEmail = await this.userRepository.findOne({
        where: { email },
      });

      if (existingEmail && existingEmail.id !== id) {
        throw new BadRequestException('Email already exists');
      }

      user.email = email;
    }

    if (updateUserDto.first_name !== undefined) {
      user.first_name = updateUserDto.first_name.trim();
    }

    if (updateUserDto.last_name !== undefined) {
      user.last_name = updateUserDto.last_name.trim();
    }

    if (updateUserDto.role !== undefined) {
      user.role = updateUserDto.role.trim();
    }

    if (updateUserDto.password && updateUserDto.password.trim() !== '') {
      user.password = await bcrypt.hash(updateUserDto.password, 10);
    }

    // ADMIN: clear faculty-only fields
    if (user.role === 'Admin') {
      user.employment_type = '';
      user.designation = '';
      user.preffered_time = '';
      user.unit_load = 0;
      user.program = null;
      user.institute = null;

      return await this.userRepository.save(user);
    }

    if (updateUserDto.employment_type !== undefined) {
      user.employment_type =
        updateUserDto.employment_type?.trim() || 'Full Time';
    }

    if (updateUserDto.designation !== undefined) {
      user.designation = updateUserDto.designation?.trim() || '';
    }

    if (updateUserDto.preffered_time !== undefined) {
      user.preffered_time = updateUserDto.preffered_time?.trim() || '';
    }

    if (updateUserDto.unit_load !== undefined) {
      user.unit_load = Number(updateUserDto.unit_load || 0);
    }
    if (updateUserDto.is_active !== undefined) {
      user.is_active = updateUserDto.is_active;
    }

    if (
      updateUserDto.program_id !== undefined &&
      updateUserDto.program_id !== null
    ) {
      const program = await this.programRepository.findOne({
        where: { program_id: Number(updateUserDto.program_id) },
        relations: ['institute'],
      });

      if (!program) {
        throw new NotFoundException('Program not found');
      }

      user.program = program;
      user.institute = program.institute;
    }

    return await this.userRepository.save(user);
  }

  async remove(id: number): Promise<void> {
    const result = await this.userRepository.delete(id);
    if (result.affected === 0) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }
  }

  async importUsers(importData: ImportUserDto[]): Promise<ImportResult> {
    const results: ImportResult = {
      success: 0,
      failed: 0,
      errors: [],
    };

    const programs = await this.programRepository.find({
      relations: ['institute'],
    });

    for (let i = 0; i < importData.length; i++) {
      try {
        const userData = importData[i];

        // REQUIRED VALIDATION
        if (
          !userData.first_name ||
          !userData.last_name ||
          !userData.email ||
          !userData.role
        ) {
          results.failed++;

          results.errors.push({
            row: i + 2,
            error: 'Missing required fields',
            data: userData,
          });

          continue;
        }

        // CHECK EXISTING EMAIL
        const existingUser = await this.userRepository.findOne({
          where: {
            email: userData.email.trim().toLowerCase(),
          },
        });

        if (existingUser) {
          results.failed++;

          results.errors.push({
            row: i + 2,
            error: 'Email already exists',
            email: userData.email,
          });

          continue;
        }

        // FIND PROGRAM
        // FIND PROGRAM
        let program: Program | undefined = undefined;

        if (userData.program) {
          const programSearch = userData.program.toLowerCase();

          program = programs.find(
            (p) =>
              p.program_name?.toLowerCase() === programSearch ||
              p.program_code?.toLowerCase() === programSearch,
          );
        }
        // DEFAULT PASSWORD
        const defaultPassword = 'Password123!';
        const hashedPassword = await bcrypt.hash(defaultPassword, 10);

        // CREATE USER PAYLOAD
        const userPayload: any = {
          first_name: userData.first_name.trim(),
          last_name: userData.last_name.trim(),
          email: userData.email.trim().toLowerCase(),
          password: hashedPassword,

          role: userData.role?.trim(),

          employment_type: userData.employment_type?.trim() || 'Full Time',

          unit_load: Number(userData.unit_load || 0),

          designation: userData.designation?.trim() || '',

          preffered_time: '',
        };

        // PROGRAM + INSTITUTE
        if (program) {
          userPayload.program = program;

          if (program.institute) {
            userPayload.institute = program.institute;
          }
        }

        const newUser = this.userRepository.create(userPayload);

        await this.userRepository.save(newUser);

        results.success++;
      } catch (error) {
        results.failed++;

        results.errors.push({
          row: i + 2,
          error: error.message || 'Unknown error',
          data: importData[i],
        });
      }
    }

    return results;
  }

  async importExpertise(
    importData: ImportExpertiseDto[],
  ): Promise<ImportResult> {
    const results: ImportResult = { success: 0, failed: 0, errors: [] };

    const users = await this.userRepository.find({ relations: ['program'] });
    const courses = await this.courseRepository.find();
    const existingExpertise = await this.userExpertiseRepository.find({
      relations: ['user', 'course'],
    });

    // -----------------------------
    // FAST LOOKUP MAPS
    // -----------------------------

    const userMap = new Map<string, User_Accounts>();
    const courseMap = new Map<string, Course>();
    const existingMap = new Set<string>();

    users.forEach((u) => {
      const key = `${u.first_name.toLowerCase()} ${u.last_name.toLowerCase()}`;
      userMap.set(key, u);
    });

    courses.forEach((c) => {
      const key = c.course_code.replace(/\s+/g, '').toUpperCase();
      courseMap.set(key, c);
    });

    existingExpertise.forEach((e) => {
      const key = `${e.user.id}-${e.course.course_id}`;
      existingMap.add(key);
    });

    const allPrograms = await this.programRepository.find();
    const programInstituteMap = new Map<number, number>();
    allPrograms.forEach((p) =>
      programInstituteMap.set(p.program_id, p.institute_id),
    );

    const courseProgramRows: { course_id: number; program_id: number }[] =
      await this.courseRepository.manager.query(`
        SELECT DISTINCT cc.course_id, cu.program_id
        FROM curriculum_courses cc
        JOIN curricula cu ON cu.curriculum_id = cc.curriculum_id
      `);

    const courseProgramMap = new Map<number, Set<number>>();
    courseProgramRows.forEach(({ course_id, program_id }) => {
      if (!courseProgramMap.has(course_id)) {
        courseProgramMap.set(course_id, new Set());
      }
      courseProgramMap.get(course_id)!.add(program_id);
    });

    const expertiseToInsert: UserExpertise[] = [];

    // -----------------------------
    // PROCESS EXCEL DATA
    // -----------------------------

    for (let i = 0; i < importData.length; i++) {
      const row = importData[i];

      // if (!row.instructor_name || !row.course_code) {
      //   results.failed++;
      //   results.errors.push({
      //     row: i + 2,
      //     error: 'Missing instructor or course',
      //   });
      //   continue;
      // }

      const instructor = row.instructor_name
        .trim()
        .replace(/\s+/g, ' ')
        .toLowerCase();

      const [last = '', first = ''] = instructor
        .split(',')
        .map((item) => item.trim());

      const userKey = `${first} ${last}`;
      const user = userMap.get(userKey);
      if (!user) {
        results.failed++;
        results.errors.push({
          row: i + 2,
          error: `Instructor not found: ${row.instructor_name}`,
        });
        continue;
      }

      const courseCode = row.course_code
        .trim()
        .replace(/\s+/g, '')
        .toUpperCase();

      const course = courseMap.get(courseCode);

      if (!course) {
        results.failed++;
        results.errors.push({
          row: i + 2,
          error: `Course not found: ${courseCode}`,
        });
        continue;
      }

      const userProgramId = user.program?.program_id;
      const userInstituteId = user.program?.institute_id;
      const coursePrograms =
        courseProgramMap.get(course.course_id) ?? new Set<number>();

      let status: 'PRIMARY' | 'OTHER' | 'CROSS';
      if (userProgramId && coursePrograms.has(userProgramId)) {
        status = 'PRIMARY';
      } else if (
        userInstituteId &&
        [...coursePrograms].some(
          (pid) => programInstituteMap.get(pid) === userInstituteId,
        )
      ) {
        status = 'OTHER';
      } else {
        status = 'CROSS';
      }

      const key = `${user.id}-${course.course_id}`;

      if (existingMap.has(key)) {
        results.failed++;
        results.errors.push({
          row: i + 2,
          error: `Duplicate expertise`,
        });
        continue;
      }

      const expertise = this.userExpertiseRepository.create({
        user,
        course,
        status,
      });

      expertiseToInsert.push(expertise);
      existingMap.add(key);
      results.success++;
    }

    // -----------------------------
    // BULK INSERT (FAST)
    // -----------------------------

    if (expertiseToInsert.length > 0) {
      await this.userExpertiseRepository.save(expertiseToInsert);
    }

    return results;
  }
}
