import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  OneToMany,
} from 'typeorm';
import { AssignClass } from 'src/assign_class/entities/assign_class.entity';
import { CurriculumCourse } from 'src/curriculum_courses/entities/curriculum_course.entity';

@Entity('courses')
export class Course {
  @PrimaryGeneratedColumn()
  course_id: number;

  @Column({ type: 'varchar', length: 100 })
  course_code: string;

  @Column({ type: 'varchar', length: 255 })
  course_title: string;

  @Column({ type: 'int' })
  course_semester: number;

  @Column({ type: 'int' })
  course_level: number;

  @Column({ type: 'int' })
  course_lec: number;

  @Column({ type: 'int' })
  course_lab: number;

  @Column({ type: 'varchar', length: 255, nullable: true })
  course_requisite: string;

  // 🔹 Relationships
  @OneToMany(() => AssignClass, (assignClass) => assignClass.course)
  assignClasses: AssignClass[];

  @OneToMany(
    () => CurriculumCourse,
    (curriculumCourse) => curriculumCourse.course,
  )
  curriculumCourses: CurriculumCourse[];

  @CreateDateColumn({ type: 'timestamp' })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp' })
  update_at: Date;
}
