import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
} from 'typeorm';

@Entity('unscheduled_meetings')
export class UnscheduledMeeting {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  class_id: number;

  @Column()
  course_code: string;

  @Column()
  course_id: number;

  @Column()
  class_size: number;

  @Column()
  faculty_name: string;

  @Column()
  program_id: number;

  @Column()
  program_code: string;

  @Column()
  type: string;

  @Column({
    type: 'text',
  })
  hours: string;

  @Column({
    type: 'text',
  })
  reason: string;

  @Column()
  school_year: string;

  @Column()
  semester: string;

  @CreateDateColumn({
    type: 'timestamp',
  })
  created_at: Date;
}
