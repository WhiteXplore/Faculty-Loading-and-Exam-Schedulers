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
import { Department } from 'src/departments/entities/department.entity';
import { CollegeBranch } from 'src/college_branch/entities/college_branch.entity';
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
    @InjectRepository(Department)
    private readonly departmentRepository: Repository<Department>,
    @InjectRepository(CollegeBranch)
    private readonly collegeBranchRepository: Repository<CollegeBranch>,
  ) {}

  async create(createUserDto: CreateUserDto): Promise<User_Accounts> {
    const user = this.userRepository.create({
      ...createUserDto,
      is_active: createUserDto.is_active ?? true,
    });

    return await this.userRepository.save(user);
  }

  async assignExpertise(body: any) {
    const { user_id, course_id } = body;

    const user = await this.userRepository.findOne({
      where: { id: Number(user_id) },
    });

    if (!user) {
      throw new NotFoundException('User not found');
    }

    const course = await this.courseRepository.findOne({
      where: { course_id: Number(course_id) },
    });

    if (!course) {
      throw new NotFoundException('Course not found');
    }

    const existing = await this.userExpertiseRepository.findOne({
      where: {
        user: { id: Number(user_id) },
        course: { course_id: Number(course_id) },
      },
      relations: ['user', 'course'],
    });

    if (existing) {
      throw new BadRequestException(
        'This instructor is already assigned to this course.',
      );
    }

    const expertise = this.userExpertiseRepository.create({
      user,
      course,
      status: 'PRIMARY', // default
    });

    return await this.userExpertiseRepository.save(expertise);
  }

  async findAll(): Promise<User_Accounts[]> {
    return await this.userRepository.find({
      relations: [
        'institute',
        'program',
        'expertise',
        'expertise.course',
        'department',
        'college_branch',
        // ✅ include course details
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
      relations: ['program', 'institute', 'college_branch'],
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

    if (updateUserDto.department_id !== undefined) {
      if (updateUserDto.department_id === null) {
        user.department = null;
      } else {
        const department = await this.departmentRepository.findOne({
          where: {
            department_id: Number(updateUserDto.department_id),
          },
        });

        if (!department) {
          throw new NotFoundException('Department not found');
        }

        user.department = department;
      }

      // Compute based on the department assignment
      user.is_under_dpt = user.department != null;
    }

    // COLLEGE BRANCH ASSIGNMENT
    if (updateUserDto.college_branch_id !== undefined) {
      if (updateUserDto.college_branch_id === null) {
        user.college_branch = null;
      } else {
        const collegeBranch = await this.collegeBranchRepository.findOne({
          where: {
            college_branch_id: Number(updateUserDto.college_branch_id),
          },
        });

        if (!collegeBranch) {
          throw new NotFoundException('College branch not found');
        }

        user.college_branch = collegeBranch;
      }
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

    // Load reference data once before processing rows
    const programs = await this.programRepository.find({
      relations: ['institute'],
    });

    const departments = await this.departmentRepository.find();

    const branches = await this.collegeBranchRepository.find();

    // Normalize names for matching
    const normalizeName = (value: unknown): string =>
      String(value ?? '')
        .normalize('NFKC')
        .trim()
        .replace(/&/g, 'and')
        .replace(/\s+/g, ' ')
        .toLowerCase();

    for (let i = 0; i < importData.length; i++) {
      const userData = importData[i];
      const rowNumber = i + 2;

      try {
        // 1. REQUIRED VALIDATION
        if (
          !userData.first_name?.trim() ||
          !userData.last_name?.trim() ||
          !userData.email?.trim() ||
          !userData.role?.trim()
        ) {
          results.failed++;

          results.errors.push({
            row: rowNumber,
            error:
              'Missing required fields: First Name, Last Name, Email, or Role.',
            data: userData,
          });

          continue;
        }

        const email = userData.email.trim().toLowerCase();

        // 2. CHECK EXISTING EMAIL
        const existingUser = await this.userRepository.findOne({
          where: { email },
        });

        if (existingUser) {
          results.failed++;

          results.errors.push({
            row: rowNumber,
            email,
            error: 'Email already exists',
          });

          continue;
        }

        // 3. FIND PROGRAM
        let program: Program | null = null;

        const programName = normalizeName(userData.program);

        if (programName) {
          program =
            programs.find(
              (p) =>
                normalizeName(p.program_name) === programName ||
                normalizeName(p.program_code) === programName,
            ) ?? null;

          if (!program) {
            results.failed++;

            results.errors.push({
              row: rowNumber,
              email,
              error: `Program not found: "${userData.program}"`,
              data: userData,
            });

            continue;
          }
        }

        // 4. FIND DEPARTMENT
        let department: Department | null = null;

        const departmentName = normalizeName(userData.department);

        if (departmentName) {
          department =
            departments.find(
              (d) => normalizeName(d.department_name) === departmentName,
            ) ?? null;

          if (!department) {
            results.failed++;

            results.errors.push({
              row: rowNumber,
              email,
              error: `Department not found: "${userData.department}"`,
              data: userData,
            });

            continue;
          }
        }

        // 5. FIND COLLEGE BRANCH
        let collegeBranch: CollegeBranch | null = null;

        const branchName = normalizeName(userData.college_branch);

        if (branchName) {
          /*
           * IMPORTANT:
           * This assumes the CollegeBranch entity property is
           * college_branch_name.
           * Change it if your entity uses a different property.
           */
          collegeBranch =
            branches.find(
              (branch) =>
                normalizeName(branch.college_branch_name) === branchName,
            ) ?? null;

          if (!collegeBranch) {
            results.failed++;

            results.errors.push({
              row: rowNumber,
              email,
              error: `College branch not found: "${userData.college_branch}"`,
              data: userData,
            });

            continue;
          }
        }

        // 6. LOG MATCHED REFERENCE RECORDS
        console.log(`Import row ${rowNumber}`, {
          email,
          program: program?.program_name ?? null,
          program_id: program?.program_id ?? null,
          department: department?.department_name ?? null,
          department_id: department?.department_id ?? null,
          college_branch_id: collegeBranch?.college_branch_id ?? null,
          is_under_dpt: department !== null,
        });

        // 7. HASH DEFAULT PASSWORD
        const hashedPassword = await bcrypt.hash('Password', 10);

        // 8. BUILD USER PAYLOAD
        const userPayload: Partial<User_Accounts> = {
          first_name: userData.first_name.trim(),
          last_name: userData.last_name.trim(),
          email,
          password: hashedPassword,
          role: userData.role.trim(),
          employment_type: userData.employment_type?.trim() || 'Full Time',
          unit_load: Number(userData.unit_load || 0),
          designation: userData.designation?.trim() || '',
          preffered_time: '',
          is_active: true,

          // Department relationship and flag
          department: department,
          is_under_dpt: department !== null,

          // Program and institute relationships
          program: program,
          institute: program?.institute ?? null,

          // College branch relationship
          college_branch: collegeBranch,
        };

        // 9. SAVE USER
        const newUser = this.userRepository.create(userPayload);

        const savedUser = await this.userRepository.save(newUser);

        // 10. COUNT SUCCESS ONLY AFTER SAVE
        results.success++;

        console.log(`Successfully imported row ${rowNumber}`, {
          user_id: savedUser.id,
          department_id: savedUser.department?.department_id ?? null,
          is_under_dpt: savedUser.is_under_dpt,
          college_branch_id:
            savedUser.college_branch?.college_branch_id ?? null,
        });
      } catch (error) {
        results.failed++;

        results.errors.push({
          row: rowNumber,
          email: userData.email,
          error: error.message || 'Unknown error',
          data: userData,
        });

        console.error(`Failed to import row ${rowNumber}:`, error);
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
      const key = `${c.course_code.replace(/\s+/g, '').toUpperCase()}-${Number(c.course_semester)}`;
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

      const courseSemester = Number(row.course_semester);

      const courseKey = `${courseCode}-${courseSemester}`;

      const course = courseMap.get(courseKey);

      if (!course) {
        results.failed++;
        results.errors.push({
          row: i + 2,
          error: `Course not found: ${courseCode} (Semester ${courseSemester})`,
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
