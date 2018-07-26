import { Router } from '@angular/router';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material';

// Services
import { UserService } from './../services/user.service';

@Component({
  selector: 'app-error-snack',
  template: '<span>Credenciales incorrectas, intente de nuevo.</span>',
  styles: [
    `
      .example-pizza-party {
        color: white;
      }
    `
  ]
})
export class ErrorSnackComponent { }

@Component({
  selector: 'app-log-in',
  templateUrl: './log-in.component.html',
  styleUrls: ['./log-in.component.scss']
})
export class LogInComponent implements OnInit {
  logIn: FormGroup;
  loading = {
    show: false,
    text: ''
  };

  constructor(
    private formBuilder: FormBuilder,
    private userService: UserService,
    private route: Router,
    public snackBar: MatSnackBar
  ) {}

  ngOnInit() {
    this.logIn = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]]
    });
  }

  logInUser() {
    const self = this;
    if (this.logIn.valid) {
      self.loading.show = true;
      this.userService.logIn(this.logIn.getRawValue()).subscribe(
        res => {
          self.loading.show = false;
          this.route.navigate(['app']);
        },
        error => {
          this.snackBar.openFromComponent(ErrorSnackComponent, {
            duration: 2000
          });
          self.loading.show = false;
        }
      );
    }
  }
}
