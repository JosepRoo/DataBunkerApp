import { Router } from '@angular/router';
import { Component, OnInit, Input, Output, EventEmitter, OnChanges } from '@angular/core';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-products-list',
  templateUrl: './products-list.component.html',
  styleUrls: ['./products-list.component.scss']
})
export class ProductsListComponent implements OnInit, OnChanges {
  @Input()
  selectedData: any;
  @Output()
  clickedProduct: EventEmitter<any> = new EventEmitter();
  @Output()
  addFavorite: EventEmitter<any> = new EventEmitter();
  @Output()
  removeAll: EventEmitter<any> = new EventEmitter();

  constructor(private router: Router, private userService: UserService) {}
  public favorites = [];

  ngOnInit() {}

  ngOnChanges() {
    this.userService.getFavorites().subscribe(res => {
      this.favorites = res;
    });
  }

  selectProductDetails(id) {
    this.router.navigate(['/app/product/' + id]);
  }

  findFavorite(productId) {
    return !this.favorites.filter(product => {
      return product._id === productId;
    }).length;
  }

  changed() {
    this.userService.getFavorites().subscribe(res => {
      this.favorites = res;
    });
  }
}
