import { Injectable, BadRequestException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { UnscheduledMeeting } from './entities/unscheduled_meeting.entity';
import { CreateUnscheduledMeetingDto } from './dto/create-unscheduled_meeting.dto';
import { UpdateUnscheduledMeetingDto } from './dto/update-unscheduled_meeting.dto';

@Injectable()
export class UnscheduledMeetingsService {
  constructor(
    @InjectRepository(UnscheduledMeeting)
    private readonly repository: Repository<UnscheduledMeeting>,
  ) {}

  // Save a single meeting
  async createOne(createDto: CreateUnscheduledMeetingDto) {
    const meeting = this.repository.create(createDto);
    return await this.repository.save(meeting);
  }

  // Save multiple meetings
  async create(
    createDtos: CreateUnscheduledMeetingDto[],
    override = false,
    restore = false,
  ) {
    if (!createDtos.length) {
      return {
        success: false,
        message: 'No unscheduled meetings provided',
      };
    }

    const { school_year, semester } = createDtos[0];

    // ==========================================
    // RESTORE FROM CANCEL
    // ==========================================
    if (restore) {
      const meetings: UnscheduledMeeting[] = [];

      for (const dto of createDtos) {
        const meetingData = {
          ...dto,
        };

        // Do not restore the old database ID.
        // Let @PrimaryGeneratedColumn() generate a new ID.
        delete (meetingData as any).unscheduled_id;

        const meeting = new UnscheduledMeeting();

        Object.assign(meeting, meetingData);

        meetings.push(meeting);
      }

      await this.repository.save(meetings);

      return {
        success: true,
        restored: meetings.length,
      };
    }
    // ==========================================
    // NORMAL BULK SAVE
    // ==========================================

    const existingCount = await this.repository.count({
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

    // ==========================================
    // OVERRIDE
    // ==========================================

    if (existingCount > 0 && override) {
      await this.repository.delete({
        school_year,
        semester,
      });
    }

    const meetings = this.repository.create(createDtos);

    await this.repository.save(meetings);

    return {
      success: true,
    };
  }

  async findAll() {
    return await this.repository.find({
      order: {
        created_at: 'DESC',
      },
    });
  }

  async findOne(id: number) {
    return await this.repository.findOne({
      where: {
        id,
      },
    });
  }

  async update(id: number, updateDto: UpdateUnscheduledMeetingDto) {
    await this.repository.update(id, updateDto);
    return this.findOne(id);
  }

  async remove(id: number) {
    const meeting = await this.findOne(id);

    if (!meeting) {
      throw new BadRequestException(
        `Unscheduled meeting with ID ${id} not found`,
      );
    }

    return this.repository.remove(meeting);
  }
}
