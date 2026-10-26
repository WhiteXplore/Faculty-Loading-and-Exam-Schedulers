import { Type } from 'class-transformer';
import {
  IsEmail,
  IsNumber,
  IsOptional,
  IsString,
  IsBoolean,
  IsArray,
} from 'class-validator';

export class CreateUserDto {
  @IsOptional()
  @IsString()
  first_name?: string;

  @IsOptional()
  @IsString()
  last_name?: string;

  @IsOptional()
  @IsEmail()
  email?: string;

  @IsOptional()
  @IsString()
  password?: string;

  @IsOptional()
  @IsString()
  role?: string;

  @IsOptional()
  @IsString()
  employment_type?: string;

  @IsOptional()
  @IsString()
  designation?: string;

  @IsOptional()
  @IsString()
  preffered_time?: string;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  unit_load?: number;

  @IsOptional()
  @IsArray()
  @IsString({ each: true })
  preferred_rest_day?: string[];

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  sp_mas_unit?: number;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  institute_id?: number;

  @IsOptional()
  @IsBoolean()
  is_active?: boolean;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  program_id?: number;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  department_id?: number;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  college_branch_id?: number;

  @IsOptional()
  @IsBoolean()
  is_under_dpt?: boolean;
}

export class ImportUserDto {
  @IsOptional()
  @IsString()
  first_name?: string;

  @IsOptional()
  @IsString()
  last_name?: string;

  @IsOptional()
  @IsEmail()
  email?: string;

  @IsOptional()
  @IsString()
  role?: string;

  @IsOptional()
  @IsString()
  program?: string;

  @IsOptional()
  @IsString()
  department?: string;

  @IsOptional()
  @IsString()
  designation?: string;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  unit_load?: number;

  @IsOptional()
  @IsString()
  employment_type?: string;

  // Branch name from the Excel "Branch Coordinator" column
  @IsOptional()
  @IsString()
  college_branch?: string;

  // Optional branch ID, if importing by ID instead
  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  college_branch_id?: number;
}

export class UpdateUserDto {
  @IsOptional()
  @IsString()
  first_name?: string;

  @IsOptional()
  @IsString()
  last_name?: string;

  @IsOptional()
  @IsEmail()
  email?: string;

  @IsOptional()
  @IsString()
  password?: string;

  @IsOptional()
  @IsString()
  role?: string;

  @IsOptional()
  @IsString()
  employment_type?: string;

  @IsOptional()
  @IsString()
  designation?: string;

  @IsOptional()
  @IsString()
  preffered_time?: string;

  @IsOptional()
  @IsBoolean()
  is_active?: boolean;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  unit_load?: number;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  institute_id?: number | null;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  program_id?: number | null;

  // Department assignment
  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  department_id?: number | null;

  // College Branch assignment
  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  college_branch_id?: number | null;

  @IsOptional()
  @IsBoolean()
  is_under_dpt?: boolean;
}
