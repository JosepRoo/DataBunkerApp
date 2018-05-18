import { Component, AfterViewInit, OnInit } from '@angular/core';
import { NgbModal} from '@ng-bootstrap/ng-bootstrap';
import { ROUTES } from './menu-items';
import { RouteInfo } from "./sidebar.metadata";
import { Router, ActivatedRoute } from "@angular/router";
import { Observable } from 'rxjs';


//import models
import { User } from "../../classes/user";
import { UserService } from "../../services/user.service";

declare var $: any;
@Component({
  selector: 'ap-sidebar',
  templateUrl: './sidebar.component.html'

})
export class SidebarComponent implements OnInit {

    user: User;
    showMenu: string = '';
    showSubMenu: string = '';
    public sidebarnavItems: any[];
    //this is for the open close
    addExpandClass(element: any) {
        if (element === this.showMenu) {
            this.showMenu = '0';

        } else {
            this.showMenu = element;
        }
    }
    addActiveClass(element: any) {
        if (element === this.showSubMenu) {
            this.showSubMenu = '0';

        } else {
            this.showSubMenu = element;
        }
    }

    constructor(private modalService: NgbModal, private router: Router,
        private route: ActivatedRoute, private userService: UserService) {}

    ngOnInit() {
        this.sidebarnavItems = ROUTES.filter(sidebarnavItem => sidebarnavItem);
        $(function () {
            $(".sidebartoggler").on('click', function() {
                if ($("#main-wrapper").hasClass("mini-sidebar")) {
                    $("body").trigger("resize");
                    $("#main-wrapper").removeClass("mini-sidebar");

                } else {
                    $("body").trigger("resize");
                    $("#main-wrapper").addClass("mini-sidebar");
                }
            });

        });

        // this.userService.getUser('b7faddc73eca4461bbfcca2f3939b483')
        //   .subscribe(user => this.user = user);
    }

    logOut() {
      this.userService.logOut().subscribe(res => {
        this.router.navigateByUrl('/screen');

      }, (err) => {
        this.router.navigateByUrl('/screen');

    });
    }
}
