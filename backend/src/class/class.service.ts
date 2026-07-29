import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Class } from './entities/class.entity';
import { CreateClassDto } from './dto/create-class.dto';
import { UpdateClassDto } from './dto/update-class.dto';
import { DataSource } from 'typeorm';
@Injectable()
export class ClassService {
  constructor(
    @InjectRepository(Class)
    private readonly classRepository: Repository<Class>,
    private readonly dataSource: DataSource,
  ) {}

  async create(createClassDto: CreateClassDto): Promise<Class> {
    const classEntity = this.classRepository.create(createClassDto);
    return await this.classRepository.save(classEntity);
  }

  async findAll(): Promise<Class[]> {
    return await this.classRepository.find({
      relations: {
        schoolYear: true,
        program: {
          institute: true,
        },
        colleges: true,
      },
      order: {
        created_at: 'DESC',
      },
    });
  }

  async findOne(id: number): Promise<Class> {
    const classEntity = await this.classRepository.findOne({
      where: { class_id: id },
      relations: {
        schoolYear: true,
        program: {
          institute: true,
        },
        colleges: true,
      },
    });

    if (!classEntity) {
      throw new NotFoundException(`Class with ID ${id} not found`);
    }

    return classEntity;
  }

  async update(id: number, updateClassDto: UpdateClassDto): Promise<Class> {
    const classEntity = await this.classRepository.preload({
      class_id: id,
      ...updateClassDto,
    });
    if (!classEntity) {
      throw new NotFoundException(`Class with ID ${id} not found`);
    }
    return await this.classRepository.save(classEntity);
  }

  async remove(id: number): Promise<void> {
    const classEntity = await this.findOne(id);
    await this.classRepository.remove(classEntity);
  }
  async getClassesCourseRaw() {
    return await this.dataSource.query(`
    SELECT *
    FROM dnsc_class_scheduler2.classes_course
  `);
  }
}
