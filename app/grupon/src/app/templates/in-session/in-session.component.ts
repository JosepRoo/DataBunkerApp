import { Component, OnInit } from '@angular/core';

// Services
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-in-session',
  templateUrl: './in-session.component.html',
  styleUrls: ['./in-session.component.scss']
})
export class InSessionComponent implements OnInit {

  user: any;

  constructor(
    private userService: UserService
  ) { }

  ngOnInit() {
    this.userService.getUser().subscribe(res => {
      this.user = res;
    });
  }

}
