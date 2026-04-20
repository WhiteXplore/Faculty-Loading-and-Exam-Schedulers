import { PartialType } from '@nestjs/swagger';
import { CreateCurriculumCourseDto } from './create-curriculum_course.dto';

export class UpdateCurriculumCourseDto extends PartialType(CreateCurriculumCourseDto) {}
