import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
} from '@nestjs/common';
import { UnscheduledMeetingsService } from './unscheduled_meetings.service';
import { CreateUnscheduledMeetingDto } from './dto/create-unscheduled_meeting.dto';
import { UpdateUnscheduledMeetingDto } from './dto/update-unscheduled_meeting.dto';

@Controller('unscheduled-meetings')
export class UnscheduledMeetingsController {
  constructor(private readonly service: UnscheduledMeetingsService) {}

  // Single meeting
  @Post()
  create(@Body() createDto: CreateUnscheduledMeetingDto) {
    return this.service.createOne(createDto);
  }

  // Bulk meetings
  @Post('add-unscheduled-meetings')
  createMany(@Body() body: any) {
    return this.service.create(
      body.meetings || body,
      body.override || false,
      body.restore || false,
    );
  }

  @Get('get-all-unscheduled-meetings')
  findAll() {
    return this.service.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.service.findOne(+id);
  }

  @Patch(':id')
  update(
    @Param('id') id: string,
    @Body() updateDto: UpdateUnscheduledMeetingDto,
  ) {
    return this.service.update(+id, updateDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.service.remove(+id);
  }
}
