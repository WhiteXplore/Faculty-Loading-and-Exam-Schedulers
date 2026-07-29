import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  ManyToOne,
  OneToMany,
  JoinColumn,
} from 'typeorm';
import { Institute } from 'src/institute/entities/institute.entity';
import { Program } from 'src/programs/entities/program.entity';
import { UserExpertise } from 'src/user/entities/user_expertise.entity';
import { UserOtherExpertise } from 'src/user/entities/user_other_expertise.entity';
import { SchoolYear } from 'src/school_year/entities/school_year.entity';
import { FacultyBranch } from 'src/faculty_branch/entities/faculty_branch.entity';
@Entity('user_accounts')
export class User_Accounts {
  @PrimaryGeneratedColumn('increment')
  id: number;

  @Column()
  first_name: string;

  @Column()
  last_name: string;

  @Column()
  email: string;

  @Column()
  password: string;

  @Column()
  role: string;

  @Column()
  employment_type: string;

  @Column({
    type: 'decimal',
    precision: 5,
    scale: 2,
    default: 0,
  })
  unit_load: number;

  @Column('simple-array', { nullable: true })
  preferred_rest_day: string[];

  @Column({
    type: 'decimal',
    precision: 10,
    scale: 2,
    nullable: true,
  })
  sp_mas_unit: number | null;

  @Column()
  designation: string;

  @Column({ nullable: true })
  preffered_time: string;
  @Column({ type: 'boolean', default: true })
  is_active: boolean;

  @ManyToOne(() => Program, { nullable: true })
  @JoinColumn({ name: 'program_id' })
  program: Program | null;

  @ManyToOne(() => Institute, { nullable: true })
  @JoinColumn({ name: 'institute_id' })
  institute: Institute | null;

  // School Year Relationship ✅
  @ManyToOne(() => SchoolYear, {
    onDelete: 'SET NULL',
    eager: true,
  })
  @JoinColumn({ name: 'school_year_id' })
  school_year: SchoolYear;

  // Expertise Relationships
  @OneToMany(() => UserExpertise, (expertise) => expertise.user, {
    cascade: true,
  })
  expertise: UserExpertise[];

  @OneToMany(() => UserOtherExpertise, (other) => other.user, {
    cascade: true,
  })
  other_expertise: UserOtherExpertise[];

  @OneToMany(() => FacultyBranch, (fb) => fb.user, {
    cascade: true,
  })
  facultyBranches: FacultyBranch[];
}
