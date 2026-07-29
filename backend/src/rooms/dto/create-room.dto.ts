import { IsNumber, IsOptional, IsString, IsBoolean } from 'class-validator';
import { Type } from 'class-transformer';

export class CreateRoomDto {
  @IsOptional()
  @IsString()
  room_name: string;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  room_capacity: number;

  @IsOptional()
  @IsString()
  room_type: string;

  @IsOptional()
  @IsBoolean()
  is_active?: boolean;

  @IsOptional()
  @IsBoolean()
  is_sp_mas?: boolean;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  institute_id?: number | null;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  building_id?: number | null;
}
