import { DataService } from './../services/data.service';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Component, OnInit, ViewChild } from '@angular/core';
import { DataSelectComponent } from './../data-select/data-select.component';
import { UserService } from '../services/user.service';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material';

@Component({
  selector: 'app-user-added',
  template: '<span>Usuario creado.</span>',
  styles: [
    ``
  ]
})
export class UserAddedComponent {}

@Component({
  selector: 'app-new-user',
  templateUrl: './new-user.component.html',
  styleUrls: ['./new-user.component.scss']
})
export class NewUserComponent implements OnInit {
  user: FormGroup;
  loading: Boolean;

  // Children
  @ViewChild(DataSelectComponent) dataSelect: DataSelectComponent;

  privileges: any;
  channels: any;

  constructor(
    private formBuilder: FormBuilder,
    private userService: UserService,
    private router: Router,
    private snackBar: MatSnackBar,
    private dataService: DataService
  ) {}

  ngOnInit() {
    this.user = this.formBuilder.group({
      name: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]],
      channel: ['', Validators.required]
    });
    this.dataService.getChannels().subscribe(res => {
      this.channels = res;
    });
  }

  addNewUser() {
    this.privileges = this.dataSelect.getPrivileges();
    if (this.user.valid && this.privileges.length) {
      this.loading = true;
      this.userService.register(this.user.getRawValue()).subscribe(
        res => {
          this.privileges.forEach(element => {
            element.target_user_mail = this.user.controls.email.value;
            this.userService.addPrivilege(element).subscribe(_res => {});
          });
        },
        error => {
          this.loading = false;
          alert(error.error.message);
        },
        () => {
          this.loading = false;
          this.snackBar
            .openFromComponent(UserAddedComponent, {
              duration: 1000
            })
            .afterDismissed()
            .subscribe(_res => {
              this.router.navigate(['/app/users']);
            });
        }
      );
    }
  }
}
