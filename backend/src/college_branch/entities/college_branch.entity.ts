import { Entity, PrimaryGeneratedColumn, Column, OneToMany } from 'typeorm';
import { Class } from 'src/class/entities/class.entity';

import { FacultyBranch } from 'src/faculty_branch/entities/faculty_branch.entity';

import { BuildingArea } from 'src/building_areas/entities/building_area.entity';
import { User_Accounts } from 'src/user/entities/user.entity';

@Entity('college_branch')
export class CollegeBranch {
  @PrimaryGeneratedColumn()
  college_branch_id: number;

  @Column({ type: 'varchar', length: 100 })
  college_branch_name: string;

  @OneToMany(() => Class, (cls) => cls.colleges)
  classes: Class[];

  @OneToMany(() => FacultyBranch, (fb) => fb.collegeBranch)
  facultyBranches: FacultyBranch[];

  // ONE CollegeBranch → MANY BuildingAreas
  @OneToMany(() => BuildingArea, (area) => area.collegeBranch)
  buildingAreas: BuildingArea[];

  @OneToMany(() => User_Accounts, (user) => user.college_branch)
  users: User_Accounts[];
}
