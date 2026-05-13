import {
  Controller,
  Post,
  Get,
  Body,
  Res,
  Req,
  UseGuards,
  BadRequestException,
} from '@nestjs/common';
import { AuthService } from './auth.service';
import { Response, Request } from 'express';
import { JwtAuthGuard } from './jwt-auth.guard';
import { AuthRequest } from './types';
import { UpdateUserDto } from './dto/update-user.dto';
import { Param, Patch, Delete } from '@nestjs/common';
@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post('login')
  async login(
    @Body('email') email: string,
    @Body('password') password: string,
    @Res() res: Response,
  ) {
    return this.authService.login(email, password, res);
  }

  // src/auth/auth.controller.ts

@Post('register')
async register(@Body() body: any, @Res() res: Response) {
  const {
    email,
    password,
    first_name,
    last_name,
    role,
    employment_type,
    designation,
    preffered_time,
    unit_load,
    institute_id,
    program_id,
  } = body;
  if (!email || !password || !first_name || !last_name || !role) {
    throw new BadRequestException('Basic user fields are required');
  }

  if (role !== 'Admin' && (!institute_id || !program_id)) {
    throw new BadRequestException('Institute and Program are required');
  }

  return this.authService.register(
    {
      email,
      password,
      first_name,
      last_name,
      role,
      employment_type,
      designation,
      preffered_time,
      unit_load,
      institute_id,
      program_id,
    },
    res,
  );
}

  @Post('logout')
  async logout(@Res() res: Response) {
    return this.authService.logout(res);
  }

  @Get('me')
  @UseGuards(JwtAuthGuard)
  async getProfile(@Req() req: AuthRequest) {
    return req.user; // ✅ will include institute_id and program_id now
  }

  @Get('all')
  // @UseGuards(JwtAuthGuard) // Optional: secure this route
  async getAllUsers() {
    return this.authService.getAllUsers();
  }

  @Get('all-raw')
  async getAllUsersRaw() {
    return this.authService.getAllUsersRaw();
  }

  @Patch('update/:id')
  async updateUser(@Param('id') id: number, @Body() updates: UpdateUserDto) {
    return this.authService.updateUser(Number(id), updates);
  }
  @Delete('remove/:id')
  async removeUser(@Param('id') id: number) {
    return this.authService.removeUser(+id);
  }
}
