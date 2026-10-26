import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  OneToMany,
} from 'typeorm';
import { Program } from 'src/programs/entities/program.entity';
import { Room } from 'src/rooms/entities/room.entity';
import { User_Accounts } from 'src/user/entities/user.entity';
import { Department } from 'src/departments/entities/department.entity';

@Entity('institutes')
export class Institute {
  @PrimaryGeneratedColumn()
  institute_id: number;

  @Column({ type: 'varchar', length: 255 })
  institute_name: string;

  @Column({ type: 'varchar', length: 255 })
  institute_code: string;

  @CreateDateColumn({ type: 'timestamp' })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp' })
  updated_at: Date;

  // 🔹 Relations

  @OneToMany(() => Program, (program) => program.institute)
  programs: Program[];

  @OneToMany(() => Room, (room) => room.institute)
  rooms: Room[];

  @OneToMany(() => Department, (department) => department.institute)
  departments: Department[];

  @OneToMany(() => User_Accounts, (user) => user.institute)
  users: User_Accounts[];
}
