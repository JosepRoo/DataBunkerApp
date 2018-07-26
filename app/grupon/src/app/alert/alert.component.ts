import { Component, OnInit } from '@angular/core';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-alert',
  templateUrl: './alert.component.html',
  styleUrls: ['./alert.component.scss']
})
export class AlertComponent implements OnInit {
  favorites: any;

  constructor(
    private userService: UserService
  ) { }

  ngOnInit() {
    this.userService.getFavorites().subscribe(res => {
      this.favorites = res;
      console.log(this.favorites);
    });
  }

}
