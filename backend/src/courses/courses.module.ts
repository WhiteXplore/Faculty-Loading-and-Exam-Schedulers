import { Module } from '@nestjs/common';
import { CoursesService } from './courses.service';
import { CoursesController } from './courses.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Course } from './entities/course.entity';
import { CurriculumCourse } from 'src/curriculum_courses/entities/curriculum_course.entity';
@Module({
  imports: [TypeOrmModule.forFeature([Course, CurriculumCourse])],
  controllers: [CoursesController],
  providers: [CoursesService],
})
export class CoursesModule {}
