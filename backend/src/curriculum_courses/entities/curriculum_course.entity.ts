import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  ManyToOne,
  JoinColumn,
} from 'typeorm';
import { Curriculum } from 'src/curriculum/entities/curriculum.entity';
import { Course } from 'src/courses/entities/course.entity';

@Entity('curriculum_courses')
export class CurriculumCourse {
  @PrimaryGeneratedColumn()
  curriculum_course_id: number;

  @Column({ type: 'int' })
  curriculum_id: number;

  @Column({ type: 'int' })
  course_id: number;

  @CreateDateColumn({ type: 'timestamp' })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp' })
  updated_at: Date;

  // 🔹 Relations
 @ManyToOne(() => Curriculum, (curriculum) => curriculum.curriculumCourses, {
    onDelete: 'CASCADE',
    })
    @JoinColumn({ name: 'curriculum_id' })
    curriculum: Curriculum;

    @ManyToOne(() => Course, (course) => course.curriculumCourses, {
    onDelete: 'CASCADE',
    })
    @JoinColumn({ name: 'course_id' })
    course: Course;

}
