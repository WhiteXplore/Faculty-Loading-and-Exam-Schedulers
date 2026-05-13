import { Type } from 'class-transformer';
import {
  IsEmail,
  IsNumber,
  IsOptional,
  IsString,
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
  @Type(() => Number)
  @IsNumber()
  institute_id?: number;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  program_id?: number;
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
  designation?: string;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  unit_load?: number;

  @IsOptional()
  @IsString()
  employment_type?: string;
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
}