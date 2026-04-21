import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, DataSource } from 'typeorm';
import { Course } from './entities/course.entity';
import { CreateCourseDto } from './dto/create-course.dto';
import { UpdateCourseDto } from './dto/update-course.dto';

@Injectable()
export class CoursesService {
  constructor(
    @InjectRepository(Course)
    private readonly courseRepository: Repository<Course>,
    private readonly dataSource: DataSource,
  ) {}

  // 🔹 BULK INSERT COURSES
  // async createMany(createCourseDtos: CreateCourseDto[]) {
  //   const queryRunner = this.dataSource.createQueryRunner();

  //   await queryRunner.connect();
  //   await queryRunner.startTransaction();

  //   try {
  //     await queryRunner.manager.insert(Course, createCourseDtos);

  //     await queryRunner.commitTransaction();

  //     return {
  //       message: `${createCourseDtos.length} courses uploaded successfully`,
  //     };
  //   } catch (error) {
  //     await queryRunner.rollbackTransaction();
  //     throw error;
  //   } finally {
  //     await queryRunner.release();
  //   }
  // }
// 🔹 BULK INSERT COURSES
async createMany(createCourseDtos: CreateCourseDto[]): Promise<Course[]> {
  const queryRunner = this.dataSource.createQueryRunner();

  await queryRunner.connect();
  await queryRunner.startTransaction();

  try {
    if (!createCourseDtos?.length) {
      await queryRunner.commitTransaction();
      return [];
    }

    const normalize = (val: string) =>
      String(val || '')
        .replace(/\s+/g, '')
        .toUpperCase()
        .trim();

    // remove duplicate course_code inside uploaded file
    const uniqueDtos = Array.from(
      new Map(
        createCourseDtos.map((item) => [normalize(item.course_code), item]),
      ).values(),
    );

    const courseCodes = uniqueDtos
      .map((item) => item.course_code)
      .filter(Boolean);

    // find already existing courses
    const existingCourses = await queryRunner.manager.find(Course, {
      where: courseCodes.map((code) => ({ course_code: code })),
    });

    const existingMap = new Map(
      existingCourses.map((course) => [normalize(course.course_code), course]),
    );

    // only insert new course_code
    const toInsert = uniqueDtos.filter(
      (item) => !existingMap.has(normalize(item.course_code)),
    );

    if (toInsert.length) {
      const newCourses = queryRunner.manager.create(
        Course,
        toInsert.map((item) => ({
          course_level: item.course_level,
          course_semester: item.course_semester,
          course_code: item.course_code,
          course_title: item.course_title,
          course_lec: item.course_lec,
          course_lab: item.course_lab,
        })),
      );

      await queryRunner.manager.save(Course, newCourses);
    }

    // return all matched/saved courses so frontend gets course_id
    const finalCourses = await queryRunner.manager.find(Course, {
      where: courseCodes.map((code) => ({ course_code: code })),
    });

    await queryRunner.commitTransaction();
    return finalCourses;
  } catch (error) {
    await queryRunner.rollbackTransaction();
    throw error;
  } finally {
    await queryRunner.release();
  }
}
  async create(createCourseDto: CreateCourseDto): Promise<Course> {
    const course = this.courseRepository.create(createCourseDto);
    return await this.courseRepository.save(course);
  }

  async findAll(): Promise<Course[]> {
    return await this.courseRepository.find({
      relations: [
        'curriculumCourses',
        'curriculumCourses.curriculum',
        'curriculumCourses.curriculum.program',
        'curriculumCourses.curriculum.program.institute',
      ],
    });
  }

  async findOne(id: number): Promise<Course> {
    const course = await this.courseRepository.findOne({
      where: { course_id: id },
      relations: [
        'curriculumCourses',
        'curriculumCourses.curriculum',
        'curriculumCourses.curriculum.program',
        'curriculumCourses.curriculum.program.institute',
      ],
    });

    if (!course) {
      throw new NotFoundException(`Course with ID ${id} not found`);
    }

    return course;
  }

  async update(id: number, updateCourseDto: UpdateCourseDto): Promise<Course> {
    const course = await this.courseRepository.preload({
      course_id: id,
      ...updateCourseDto,
    });

    if (!course) {
      throw new NotFoundException(`Course with ID ${id} not found`);
    }

    return await this.courseRepository.save(course);
  }

  async remove(id: number): Promise<{ message: string }> {
    const course = await this.findOne(id);
    await this.courseRepository.remove(course);
    return { message: `Course with ID ${id} deleted successfully` };
  }

  async findReportCurriculum(): Promise<any[]> {
    const rawQuery = `
SELECT 
  i.institute_id,
  i.institute_name,
  i.institute_code,
  COUNT(DISTINCT c.course_id) AS total_courses,
  GROUP_CONCAT(DISTINCT c.course_code ORDER BY c.course_code SEPARATOR ', ') AS course_codes,
  GROUP_CONCAT(DISTINCT cu.curriculum_id ORDER BY cu.curriculum_id SEPARATOR ', ') AS curriculum_ids
FROM courses c
JOIN curriculum_courses cc ON c.course_id = cc.course_id
JOIN curricula cu ON cc.curriculum_id = cu.curriculum_id
JOIN programs p ON cu.program_id = p.program_id
JOIN institutes i ON p.institute_id = i.institute_id
GROUP BY i.institute_id, i.institute_name, i.institute_code;
    `;

    return await this.dataSource.query(rawQuery);
  }
}
