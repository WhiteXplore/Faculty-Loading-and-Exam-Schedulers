import { IsNotEmpty, IsString, MaxLength, IsInt, Min } from 'class-validator';

export class CreateDepartmentDto {
  @IsString()
  @IsNotEmpty()
  @MaxLength(255)
  department_name: string;

  @IsInt()
  @Min(1)
  institute_id: number;
}
