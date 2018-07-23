import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-out-session',
  templateUrl: './out-session.component.html',
  styleUrls: ['./out-session.component.scss']
})
export class OutSessionComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

  openTerms() {
    window.open('http://data-bunker.com.mx');
  }

}
