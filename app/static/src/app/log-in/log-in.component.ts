import { Component, OnInit } from '@angular/core';
import { environment } from '../../environments/environment';
import { FormBuilder, FormGroup, Validators, FormControl } from '@angular/forms';
import { UserService } from "../services/user.service";
import { Observable } from 'rxjs';
import { Router } from '@angular/router';
import { Location } from '@angular/common';


@Component({
  selector: 'app-log-in',
  templateUrl: './log-in.component.html',
  styleUrls: ['./log-in.component.css']
})
export class LogInComponent implements OnInit {

  logIn: FormGroup;
  first = true;
  res: any;

  constructor(private _formBuilder: FormBuilder, private userService: UserService, private router: Router, private location: Location ) { }

  ngOnInit() {
    this.logIn = this._formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]],
    });
  }

  onSubmit(event:Event) {
    event.preventDefault();
    this.res = null;
    this.first = false;
    if (this.logIn.valid) {
      this.userService.logIn(this.logIn.getRawValue()).subscribe(res => {
        this.res = res;
        if (this.res.success){
          this.location.replaceState('/'); // clears browser history so they can't navigate with back button
          this.router.navigate(['/']);
        }
      });
    } else {
      console.log("Error in form");
    }
  }

}
