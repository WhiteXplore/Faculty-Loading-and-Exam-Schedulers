import { IsNumber, IsOptional, IsString } from 'class-validator';
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
  @IsString()
  status: string;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  institute_id?: number | null;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  building_id?: number | null;
}
