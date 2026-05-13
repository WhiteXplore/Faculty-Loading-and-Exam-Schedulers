import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, In } from 'typeorm';
import { CurriculumCourse } from './entities/curriculum_course.entity';
import { CreateCurriculumCourseDto } from './dto/create-curriculum_course.dto';
import { UpdateCurriculumCourseDto } from './dto/update-curriculum_course.dto';

@Injectable()
export class CurriculumCoursesService {
  constructor(
    @InjectRepository(CurriculumCourse)
    private readonly curriculumCourseRepository: Repository<CurriculumCourse>,
  ) {}

  async create(createCurriculumCourseDto: CreateCurriculumCourseDto) {
    const existing = await this.curriculumCourseRepository.findOne({
      where: {
        curriculum_id: createCurriculumCourseDto.curriculum_id,
        course_id: createCurriculumCourseDto.course_id,
      },
    });

    if (existing) {
      return existing;
    }

    const newLink = this.curriculumCourseRepository.create(createCurriculumCourseDto);
    return await this.curriculumCourseRepository.save(newLink);
  }

  async submit(
    body:
      | CreateCurriculumCourseDto
      | CreateCurriculumCourseDto[]
      | {
          links: CreateCurriculumCourseDto[];
          raw_payload?: any[];
        },
  ) {
    let links: CreateCurriculumCourseDto[] = [];
    let raw_payload: any[] = [];

    if (Array.isArray(body)) {
      links = body;
    } else if ('links' in body) {
      links = Array.isArray(body.links) ? body.links : [];
      raw_payload = Array.isArray(body.raw_payload) ? body.raw_payload : [];
    } else {
      links = [body];
    }

    if (!links.length) {
      return {
        message: 'No curriculum-course links received.',
        inserted: 0,
        skipped: 0,
        data: [],
        raw_payload,
      };
    }

    // remove invalid rows
    const cleanedLinks = links.filter(
      (item) => item?.curriculum_id && item?.course_id,
    );

    if (!cleanedLinks.length) {
      return {
        message: 'No valid curriculum-course links found.',
        inserted: 0,
        skipped: links.length,
        data: [],
        raw_payload,
      };
    }

    // deduplicate inside payload
    const uniqueMap = new Map<string, CreateCurriculumCourseDto>();
    for (const item of cleanedLinks) {
      const key = `${item.curriculum_id}-${item.course_id}`;
      if (!uniqueMap.has(key)) {
        uniqueMap.set(key, item);
      }
    }

    const uniqueLinks = [...uniqueMap.values()];

    // check existing in DB
    const curriculumIds = [...new Set(uniqueLinks.map((x) => x.curriculum_id))];
    const courseIds = [...new Set(uniqueLinks.map((x) => x.course_id))];

    const existing = await this.curriculumCourseRepository.find({
      where: {
        curriculum_id: In(curriculumIds),
        course_id: In(courseIds),
      },
    });

    const existingSet = new Set(
      existing.map((item) => `${item.curriculum_id}-${item.course_id}`),
    );

    const toInsert = uniqueLinks.filter(
      (item) => !existingSet.has(`${item.curriculum_id}-${item.course_id}`),
    );

    let insertedRows: CurriculumCourse[] = [];
    if (toInsert.length) {
      const entities = this.curriculumCourseRepository.create(toInsert);
      insertedRows = await this.curriculumCourseRepository.save(entities);
    }

    return {
      message: 'Curriculum-course submission completed.',
      inserted: insertedRows.length,
      skipped: uniqueLinks.length - insertedRows.length,
      data: insertedRows,
      raw_payload,
    };
  }

  findAll() {
    return this.curriculumCourseRepository.find({
      relations: ['curriculum', 'curriculum.institute', 'curriculum.program', 'course'],
    });
  }

  findOne(id: number) {
    return this.curriculumCourseRepository.findOne({
      where: { curriculum_course_id: id },
      relations: ['curriculum', 'curriculum.institute', 'curriculum.program', 'course'],
    });
  }

  async update(
    id: number,
    updateCurriculumCourseDto: UpdateCurriculumCourseDto,
  ) {
    await this.curriculumCourseRepository.update(id, updateCurriculumCourseDto);
    return this.findOne(id);
  }

  async remove(id: number) {
    const data = await this.findOne(id);
    if (!data) {
      return { message: 'Curriculum-course not found' };
    }

    await this.curriculumCourseRepository.delete(id);
    return { message: 'Curriculum-course deleted successfully' };
  }
}