import { Injectable } from '@angular/core';
import { Router, NavigationStart } from '@angular/router';
import { Observable } from 'rxjs';
import { Subject } from 'rxjs/Subject';

// import models
import { ColorGenerator } from "../classes/colorGenerator";

@Injectable()
export class ColorGeneratorService {

  private colorGenerator: ColorGenerator;

  constructor() {
    this.colorGenerator = new ColorGenerator();
  }

  getColor() {
    return this.colorGenerator.next();
  }
}
