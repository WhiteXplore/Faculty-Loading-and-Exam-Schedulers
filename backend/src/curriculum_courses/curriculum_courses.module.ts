import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { CurriculumCoursesService } from './curriculum_courses.service';
import { CurriculumCoursesController } from './curriculum_courses.controller';
import { CurriculumCourse } from './entities/curriculum_course.entity';

@Module({
  imports: [TypeOrmModule.forFeature([CurriculumCourse])],
  controllers: [CurriculumCoursesController],
  providers: [CurriculumCoursesService],
})
export class CurriculumCoursesModule {}
