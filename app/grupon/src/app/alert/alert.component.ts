import { DataService } from './../services/data.service';
import { Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-alert',
  templateUrl: './alert.component.html',
  styleUrls: ['./alert.component.scss']
})
export class AlertComponent implements OnInit {
  favorites: any;
  loading: Boolean = true;
  constructor(private userService: UserService, private dataService: DataService, private router: Router) {}

  ngOnInit() {
    this.loadFavorites();
  }

  removeFavorite(id) {
    this.dataService.removeFavorite(id).subscribe(_res => {
      this.loadFavorites();
    });
  }

  loadFavorites() {
    this.loading = true;
    this.userService.getFavorites().subscribe(res => {
      res.map(product => {
        this.dataService.getProduct(product._id).subscribe(_res => {
          product.prices = _res.sub_elements;
          console.log(product);
        });
      });
      this.favorites = res;
      this.loading = false;
    });
  }

  selectProduct(id) {
    this.router.navigate(['/app/product/' + id]);
  }
}
