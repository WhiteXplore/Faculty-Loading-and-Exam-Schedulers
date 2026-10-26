import {
  Injectable,
  NotFoundException,
  ConflictException,
  BadRequestException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, Not } from 'typeorm';

import { Department } from './entities/department.entity';
import { Institute } from 'src/institute/entities/institute.entity';
import { CreateDepartmentDto } from './dto/create-department.dto';
import { UpdateDepartmentDto } from './dto/update-department.dto';

@Injectable()
export class DepartmentsService {
  constructor(
    @InjectRepository(Department)
    private readonly departmentRepository: Repository<Department>,

    @InjectRepository(Institute)
    private readonly instituteRepository: Repository<Institute>,
  ) {}

  // CREATE department
  async create(createDepartmentDto: CreateDepartmentDto) {
    const department_name = createDepartmentDto.department_name.trim();

    if (!department_name) {
      throw new BadRequestException('Department name is required.');
    }

    const existingDepartment = await this.departmentRepository.findOneBy({
      department_name,
    });

    if (existingDepartment) {
      throw new ConflictException('Department name already exists.');
    }

    const institute = await this.instituteRepository.findOneBy({
      institute_id: createDepartmentDto.institute_id,
    });

    if (!institute) {
      throw new NotFoundException(
        `Institute with ID ${createDepartmentDto.institute_id} not found.`,
      );
    }

    const department = this.departmentRepository.create({
      department_name,
      institute,
    });

    return await this.departmentRepository.save(department);
  }

  // GET all departments
  async findAll() {
    return await this.departmentRepository.find({
      relations: {
        institute: true,
      },
      order: {
        department_id: 'DESC',
      },
    });
  }

  // GET department by ID
  async findOne(id: number) {
    const department = await this.departmentRepository.findOne({
      where: { department_id: id },
      relations: {
        institute: true,
      },
    });

    if (!department) {
      throw new NotFoundException(`Department with ID ${id} not found.`);
    }

    return department;
  }

  // UPDATE department
  async update(id: number, updateDepartmentDto: UpdateDepartmentDto) {
    const department = await this.findOne(id);

    if (updateDepartmentDto.department_name !== undefined) {
      const department_name = updateDepartmentDto.department_name.trim();

      if (!department_name) {
        throw new BadRequestException('Department name cannot be empty.');
      }

      const existingDepartment = await this.departmentRepository.findOneBy({
        department_name,
        department_id: Not(id),
      });

      if (existingDepartment) {
        throw new ConflictException('Department name already exists.');
      }

      department.department_name = department_name;
    }

    if (updateDepartmentDto.institute_id !== undefined) {
      const institute = await this.instituteRepository.findOneBy({
        institute_id: updateDepartmentDto.institute_id,
      });

      if (!institute) {
        throw new NotFoundException(
          `Institute with ID ${updateDepartmentDto.institute_id} not found.`,
        );
      }

      department.institute = institute;
    }

    await this.departmentRepository.save(department);

    // Return the updated department with its institute
    return await this.findOne(id);
  }

  // DELETE department
  async remove(id: number) {
    const department = await this.findOne(id);

    await this.departmentRepository.remove(department);

    return {
      message: 'Department deleted successfully.',
      department_id: id,
    };
  }
}
