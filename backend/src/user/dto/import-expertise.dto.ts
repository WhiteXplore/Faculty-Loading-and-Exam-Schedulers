import { IsNotEmpty, IsString, IsNumber } from 'class-validator';
import { Type } from 'class-transformer';

export class ImportExpertiseDto {
  @IsNotEmpty()
  @IsString()
  instructor_name: string;

  @IsNotEmpty()
  @IsString()
  course_code: string;

  @IsNotEmpty()
  @Type(() => Number)
  @IsNumber()
  course_semester: number;
}
