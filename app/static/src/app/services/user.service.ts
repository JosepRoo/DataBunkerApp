import { Injectable } from '@angular/core';
import { Router, NavigationStart } from '@angular/router';
import { Observable } from 'rxjs';
import { Subject } from 'rxjs/Subject';

// import models
import { User } from "../classes/user";

// import services
import { CompanyService } from "../services/company.service";

@Injectable()
export class UserService {

  private user = new User();

  constructor(private companyService: CompanyService) {
    this.user.name = "Josep Romagosa";
    this.user.company = companyService.getCompany();
  }

  getUser() {
    return this.user;
  }
}
