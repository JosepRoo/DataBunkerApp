import { Injectable } from '@angular/core';
import { Router, NavigationStart } from '@angular/router';
import { Observable } from 'rxjs';
import { Subject } from 'rxjs/Subject';

// import models
import { Company } from "../classes/company";

@Injectable()
export class CompanyService {

  private company = new Company();

  constructor() {
    this.company.photo = "sitSolutions.png";
    this.company.name = "SIT Solutions";
  }

  getCompany() {
    return this.company;
  }
}
