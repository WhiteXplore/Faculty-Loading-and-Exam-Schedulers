import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
} from '@nestjs/common';
import { CurriculumCoursesService } from './curriculum_courses.service';
import { CreateCurriculumCourseDto } from './dto/create-curriculum_course.dto';
import { UpdateCurriculumCourseDto } from './dto/update-curriculum_course.dto';

@Controller('curriculum-courses')
export class CurriculumCoursesController {
  constructor(
    private readonly curriculumCoursesService: CurriculumCoursesService,
  ) {}

  @Post('add-curriculum-course')
  create(@Body() createCurriculumCourseDto: CreateCurriculumCourseDto) {
    return this.curriculumCoursesService.create(createCurriculumCourseDto);
  }

  @Get('get-curriculum-courses')
  findAll() {
    return this.curriculumCoursesService.findAll();
  }

  @Get('get-id/:id')
  findOne(@Param('id') id: string) {
    return this.curriculumCoursesService.findOne(+id);
  }

  @Patch('update-curriculum-course/:id')
  update(
    @Param('id') id: string,
    @Body() updateCurriculumCourseDto: UpdateCurriculumCourseDto,
  ) {
    return this.curriculumCoursesService.update(+id, updateCurriculumCourseDto);
  }

  @Delete('delete-id/:id')
  remove(@Param('id') id: string) {
    return this.curriculumCoursesService.remove(+id);
  }
}
