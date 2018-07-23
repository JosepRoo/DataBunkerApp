import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { UserService } from "../../services/user.service";


import { PerfectScrollbarConfigInterface } from 'ngx-perfect-scrollbar';

@Component({
    selector: 'full-layout',
    templateUrl: './full.component.html',
    styleUrls: ['./full.component.scss']
})
export class FullComponent implements OnInit {

    color = 'default';
    showSettings = false;
    showMinisidebar = false;
    showDarktheme = false;
    private res: any;

	public config: PerfectScrollbarConfigInterface = {};

    constructor(public router: Router,
    private cookieService: CookieService,
    private userService: UserService
  ) { }

    ngOnInit() {
      this.userService.checkStatus().subscribe(res => {
          if (res){
            return true;
          } else {
            this.router.navigateByUrl('/screen');
          }

      }, (err) => {
        this.router.navigateByUrl('/screen');

    });

          if (this.router.url === '/') {
              this.router.navigate(['/comparador']);
          }

    }

}
