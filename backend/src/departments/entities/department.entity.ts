import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  JoinColumn,
  ManyToOne,
  OneToMany,
} from 'typeorm';

import { Institute } from 'src/institute/entities/institute.entity';
import { User_Accounts } from 'src/user/entities/user.entity';

@Entity('departments')
export class Department {
  @PrimaryGeneratedColumn()
  department_id: number;

  @Column({ unique: true, length: 255 })
  department_name: string;

  @ManyToOne(() => Institute, {
    nullable: true,
    onDelete: 'SET NULL',
    eager: true,
  })
  @JoinColumn({ name: 'institute_id' })
  institute: Institute | null;

  @OneToMany(() => User_Accounts, (user) => user.department)
  users: User_Accounts[];

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
