import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { CurriculumCourse } from './entities/curriculum_course.entity';
import { CreateCurriculumCourseDto } from './dto/create-curriculum_course.dto';
import { UpdateCurriculumCourseDto } from './dto/update-curriculum_course.dto';

@Injectable()
export class CurriculumCoursesService {
  constructor(
    @InjectRepository(CurriculumCourse)
    private readonly curriculumCourseRepository: Repository<CurriculumCourse>,
  ) {}

  async create(
    createCurriculumCourseDto: CreateCurriculumCourseDto,
  ): Promise<CurriculumCourse> {
    const existing = await this.curriculumCourseRepository.findOne({
      where: {
        curriculum_id: createCurriculumCourseDto.curriculum_id,
        course_id: createCurriculumCourseDto.course_id,
      },
    });

    if (existing) {
      return existing;
    }

    const newCurriculumCourse = this.curriculumCourseRepository.create(
      createCurriculumCourseDto,
    );

    return await this.curriculumCourseRepository.save(newCurriculumCourse);
  }

  async findAll(): Promise<CurriculumCourse[]> {
    return await this.curriculumCourseRepository.find({
      relations: ['curriculum', 'course'],
    });
  }

  async findOne(id: number): Promise<CurriculumCourse> {
    const curriculumCourse = await this.curriculumCourseRepository.findOne({
      where: { curriculum_course_id: id },
      relations: ['curriculum', 'course'],
    });

    if (!curriculumCourse) {
      throw new NotFoundException(`CurriculumCourse with ID ${id} not found`);
    }

    return curriculumCourse;
  }

  async update(
    id: number,
    updateCurriculumCourseDto: UpdateCurriculumCourseDto,
  ): Promise<CurriculumCourse> {
    const curriculumCourse = await this.findOne(id);
    const updated = Object.assign(curriculumCourse, updateCurriculumCourseDto);
    return await this.curriculumCourseRepository.save(updated);
  }

  async remove(id: number): Promise<void> {
    const curriculumCourse = await this.findOne(id);
    await this.curriculumCourseRepository.remove(curriculumCourse);
  }
}
