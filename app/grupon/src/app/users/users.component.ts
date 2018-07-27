import { Component, OnInit } from '@angular/core';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss']
})
export class UsersComponent implements OnInit {
  users: any;
  loading: Boolean = false;
  displayedColumns: string[] = ['name', 'email', 'favorites', '_id'];
  constructor(private userService: UserService) {}

  ngOnInit() {
    this.userService.getUsers().subscribe(res => {
      this.users = res;
    });
  }

  deleteUser(email) {
    this.userService.deleteUser(email).subscribe(_res => {
      this.userService.getUsers().subscribe(res => {
        this.users = res;
      });
    });
  }
}
