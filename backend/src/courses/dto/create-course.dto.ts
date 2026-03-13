import {
  IsInt,
  IsOptional,
  IsString,
  MaxLength,
} from 'class-validator';

export class CreateCourseDto {
  @IsString()
  @MaxLength(100)
  course_code: string;

  @IsString()
  @MaxLength(255)
  course_title: string;

  @IsInt()
  course_semester: number;

  @IsInt()
  course_level: number;

  @IsInt()
  course_lec: number;

  @IsInt()
  course_lab: number;

  @IsOptional()
  @IsString()
  course_requisite?: string;

  @IsOptional()
  @IsInt()
  institute_id?: number;

  @IsOptional()
  @IsInt()
  program_id?: number;

  @IsOptional()
  @IsInt()
  curriculum_id?: number;
}