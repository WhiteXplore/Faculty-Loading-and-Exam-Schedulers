import {
  Injectable,
  UnauthorizedException,
  BadRequestException,
} from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Response, Request } from 'express';
import * as bcrypt from 'bcrypt';
import { User_Accounts } from 'src/user/entities/user.entity';
import { Institute } from 'src/institute/entities/institute.entity';
import { Program } from 'src/programs/entities/program.entity';
import { UpdateUserDto } from './dto/update-user.dto';
import { UserExpertise } from 'src/user/entities/user_expertise.entity';
import { UserOtherExpertise } from 'src/user/entities/user_other_expertise.entity';
import { SchoolYear } from 'src/school_year/entities/school_year.entity';
@Injectable()
export class AuthService {
  constructor(
    private readonly jwtService: JwtService,
    @InjectRepository(User_Accounts)
    private readonly userRepository: Repository<User_Accounts>,
  ) {}

  async findUserByEmail(email: string): Promise<User_Accounts | null> {
    return this.userRepository.findOne({ where: { email } });
  }

  async validateUser(email: string, password: string) {
    const user = await this.userRepository.findOne({
      where: { email },
      relations: ['institute', 'program'], // ✅ load relations
    });

    if (!user) {
      throw new UnauthorizedException('Invalid email or password');
    }

    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      throw new UnauthorizedException('Invalid email or password');
    }

    return user;
  }

  async login(email: string, password: string, res: Response) {
    const user = await this.validateUser(email, password);
    const payload = {
      sub: user.id,
      email: user.email,
      role: user.role,
      first_name: user.first_name,
      last_name: user.last_name,
      institute_id: user.institute?.institute_id ?? null, // ✅ only the ID
      program_id: user.program?.program_id ?? null, // optional if you also want program_id
    };

    const token = this.jwtService.sign(payload, { expiresIn: '1h' });

    res.cookie('jwt', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 3600000,
    });

    return res.json({
      message: 'Login successful',
      role: user.role,
      institute_id: user.institute?.institute_id ?? null, // ✅ also in response
      program_id: user.program?.program_id ?? null,
    });
  }

  async logout(res: Response) {
    res.clearCookie('jwt');
    return res.status(200).json({ message: 'Logged out successfully' });
  }

  async getProfile(req: Request) {
    try {
      const token = req.cookies['jwt'];
      if (!token) {
        throw new UnauthorizedException('Not authenticated');
      }

      const decoded = this.jwtService.verify(token);
      const user = await this.userRepository.findOne({
        where: { id: decoded.sub },
      });

      if (!user) {
        throw new UnauthorizedException('User not found');
      }

      return {
        id: user.id,
        email: user.email,
        role: user.role,
        first_name: user.first_name,
        last_name: user.last_name,
      };
    } catch (error) {
      throw new UnauthorizedException('Invalid or expired token');
    }
  }

  // ✅ New Registration Method
async register(body: any, res: Response) {
  const {
    email,
    password,
    first_name,
    last_name,
    role,
    employment_type,
    designation,
    preffered_time,
    unit_load,
    institute_id,
    program_id,
  } = body;

  const existingUser = await this.findUserByEmail(email);
  if (existingUser) {
    throw new BadRequestException('Email already in use');
  }

  const hashedPassword = await bcrypt.hash(password, 10);

  let institute: Institute | null = null;
  let program: Program | null = null;

  if (role !== 'Admin') {
    institute = await this.userRepository.manager.findOne(Institute, {
      where: { institute_id: Number(institute_id) },
    });

    if (!institute) {
      throw new BadRequestException(
        `Institute with ID ${institute_id} not found`,
      );
    }

    program = await this.userRepository.manager.findOne(Program, {
      where: { program_id: Number(program_id) },
    });

    if (!program) {
      throw new BadRequestException(`Program with ID ${program_id} not found`);
    }
  }

  const newUser = this.userRepository.create({
    email,
    password: hashedPassword,
    first_name,
    last_name,
    role,

  employment_type: role === 'Admin' ? '' : employment_type || 'Full Time',
designation: role === 'Admin' ? '' : designation || '',
    preffered_time: preffered_time || '',
    unit_load: role === 'Admin' ? 0 : Number(unit_load || 0),

    institute: role === 'Admin' ? null : institute,
    program: role === 'Admin' ? null : program,
  });

  const savedUser = await this.userRepository.save(newUser);

  const payload = {
    sub: savedUser.id,
    email: savedUser.email,
    role: savedUser.role,
    first_name: savedUser.first_name,
    last_name: savedUser.last_name,
    institute_id: savedUser.institute?.institute_id ?? null,
    program_id: savedUser.program?.program_id ?? null,
  };

  const token = this.jwtService.sign(payload, { expiresIn: '1h' });

  res.cookie('jwt', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
    maxAge: 3600000,
  });

  return res.status(201).json({
    message: 'Registration successful',
    user: {
      id: savedUser.id,
      email: savedUser.email,
      first_name: savedUser.first_name,
      last_name: savedUser.last_name,
      role: savedUser.role,
      employment_type: savedUser.employment_type,
      designation: savedUser.designation,
      preffered_time: savedUser.preffered_time,
      unit_load: savedUser.unit_load,
      institute_id: savedUser.institute?.institute_id ?? null,
      program_id: savedUser.program?.program_id ?? null,
    },
  });
}

  // Inside AuthService
  async getAllUsers(): Promise<any[]> {
    const users = await this.userRepository.find({
      relations: ['institute', 'program'],
    });

    return users.map(({ password, institute, program, ...rest }) => ({
      ...rest,
      institute_id: institute ? institute.institute_id : null,
      program_id: program ? program.program_id : null,
    }));
  }

  async getAllUsersRaw(): Promise<User_Accounts[]> {
    return this.userRepository.find({
      relations: [
        'institute',
        'program',
        'expertise',
        'expertise.course', // ✅ include course details
        'other_expertise',
        'other_expertise.course', // ✅ include course details
      ],
    });
  }

async updateUser(
  id: number,
  updates: UpdateUserDto,
): Promise<Partial<User_Accounts>> {
  const user = await this.userRepository.findOne({
    where: { id },
    relations: [
      'institute',
      'program',
      'school_year',
      'expertise',
    ],
  });

  if (!user) {
    throw new BadRequestException(`User with ID ${id} not found`);
  }

  // =========================
  // PASSWORD UPDATE
  // =========================
  if (updates.password) {
    updates.password = await bcrypt.hash(updates.password, 10);
  }

  // =========================
  // INSTITUTE
  // =========================
  if (updates.institute_id) {
    const institute = await this.userRepository.manager.findOne(Institute, {
      where: { institute_id: updates.institute_id },
    });

    if (!institute) {
      throw new BadRequestException(
        `Institute with ID ${updates.institute_id} not found`,
      );
    }

    user.institute = institute;
  }

  // =========================
  // PROGRAM
  // =========================
  if (updates.program_id) {
    const program = await this.userRepository.manager.findOne(Program, {
      where: { program_id: updates.program_id },
    });

    if (!program) {
      throw new BadRequestException(
        `Program with ID ${updates.program_id} not found`,
      );
    }

    user.program = program;
  }

  // =========================
  // SCHOOL YEAR
  // =========================
  if (updates.school_year_id) {
    const schoolYear = await this.userRepository.manager.findOne(SchoolYear, {
      where: { school_year_id: updates.school_year_id },
    });

    if (!schoolYear) {
      throw new BadRequestException(
        `School Year with ID ${updates.school_year_id} not found`,
      );
    }

    user.school_year = schoolYear;
  }

  // =========================
  // 🔥 UNIFIED EXPERTISE (FIXED)
  // =========================
 if (updates.expertise) {
  await this.userRepository.manager.delete(UserExpertise, {
    user: { id: user.id },
  });

  user.expertise = updates.expertise.map((item) =>
    this.userRepository.manager.create(UserExpertise, {
      user,
      course: { course_id: item.course_id },
      status: item.status,
    }),
  );
}

  // =========================
  // ASSIGN REMAINING FIELDS
  // =========================
  const {
    institute_id,
    program_id,
    school_year_id,
    expertise,
    ...rest
  } = updates;

  Object.assign(user, rest);

  const savedUser = await this.userRepository.save(user);

  const { password, ...userWithoutPassword } = savedUser;

  return userWithoutPassword;
}

  async removeUser(id: number): Promise<{ message: string }> {
    const user = await this.userRepository.findOne({ where: { id } });

    if (!user) {
      throw new BadRequestException(`User with ID ${id} not found`);
    }

    await this.userRepository.remove(user);
    return { message: `User with ID ${id} has been removed` };
  }
}
