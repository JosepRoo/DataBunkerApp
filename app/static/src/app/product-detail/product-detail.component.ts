import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-product-detail',
  templateUrl: './product-detail.component.html',
  styleUrls: ['./product-detail.component.css']
})
export class ProductDetailComponent implements OnInit {

  product = {
    name: "Producto 1",
    price: 99.99,
    previousPrice: 89.99,
    scope: .036,
    rate: 0,
    createdDate: new Date()
  };

  constructor() { }

  ngOnInit() {
  }

}
