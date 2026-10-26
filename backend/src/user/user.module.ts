import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { UserService } from './user.service';
import { UserController } from './user.controller';
import { User_Accounts } from './entities/user.entity';
import { UserExpertise } from './entities/user_expertise.entity';
import { UserOtherExpertise } from './entities/user_other_expertise.entity';
import { Program } from 'src/programs/entities/program.entity';
import { Course } from 'src/courses/entities/course.entity';
import { Department } from 'src/departments/entities/department.entity';
import { CollegeBranch } from 'src/college_branch/entities/college_branch.entity';
UserOtherExpertise;
@Module({
  imports: [
    TypeOrmModule.forFeature([
      User_Accounts,
      UserExpertise,
      UserOtherExpertise,
      Program,
      Course,
      Department,
      CollegeBranch,
    ]),
  ],
  controllers: [UserController],
  providers: [UserService],
})
export class UserModule {}
