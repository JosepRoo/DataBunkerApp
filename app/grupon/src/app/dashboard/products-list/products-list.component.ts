import { Router } from '@angular/router';
import { Component, OnInit, Input, Output, EventEmitter, OnChanges } from '@angular/core';

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

  constructor(private router: Router) {}

  ngOnInit() {}

  ngOnChanges() {}

  selectProductDetails(id) {
    this.router.navigate(['/app/product/' + id]);
  }
}
