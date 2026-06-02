import { Injectable,   BadRequestException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { FinalGeneratedClassSchedule } from './entities/final_generated_class_schedule.entity';
import { CreateFinalGeneratedClassScheduleDto } from './dto/create-final_generated_class_schedule.dto';
import { UpdateFinalGeneratedClassScheduleDto } from './dto/update-final_generated_class_schedule.dto';

@Injectable()
export class FinalGeneratedClassScheduleService {
  constructor(
    @InjectRepository(FinalGeneratedClassSchedule)
    private readonly scheduleRepo: Repository<FinalGeneratedClassSchedule>,
  ) {}

  // Save a single schedule
  async create(createDto: CreateFinalGeneratedClassScheduleDto) {
    const schedule = this.scheduleRepo.create(createDto);
    return await this.scheduleRepo.save(schedule);
  }

  // Save multiple schedules at once
async createMany(
  createDtos: CreateFinalGeneratedClassScheduleDto[],
  override = false,
) {
  if (!createDtos.length) {
    return {
      success: false,
      message: 'No schedules provided',
    };
  }

  const { school_year, semester } = createDtos[0];

  const existingCount = await this.scheduleRepo.count({
    where: {
      school_year,
      semester,
    },
  });

  if (existingCount > 0 && !override) {
    return {
      exists: true,
      school_year,
      semester,
    };
  }

  if (existingCount > 0 && override) {
    await this.scheduleRepo.delete({
      school_year,
      semester,
    });
  }

  const schedules = this.scheduleRepo.create(createDtos);

  await this.scheduleRepo.save(schedules);

  return {
    success: true,
  };
}
  findAll() {
    return this.scheduleRepo.find();
  }

  findOne(id: number) {
    return this.scheduleRepo.findOneBy({ id });
  }

  async update(id: number, updateDto: UpdateFinalGeneratedClassScheduleDto) {
    await this.scheduleRepo.update(id, updateDto);
    return this.findOne(id);
  }

  async remove(id: number) {
    const schedule = await this.findOne(id);
    if (!schedule) {
      throw new Error(`Schedule with ID ${id} not found`);
    }
    return this.scheduleRepo.remove(schedule);
  }
}
