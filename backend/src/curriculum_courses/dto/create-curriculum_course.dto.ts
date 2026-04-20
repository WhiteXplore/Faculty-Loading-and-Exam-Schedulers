import { IsInt } from 'class-validator';
import { Type } from 'class-transformer';

export class CreateCurriculumCourseDto {
  @Type(() => Number)
  @IsInt()
  curriculum_id: number;

  @Type(() => Number)
  @IsInt()
  course_id: number;
}
