import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { MyFilterPipe } from './favoritePipe';

@Component({
  selector: 'app-products',
  templateUrl: './products.component.html',
  styleUrls: ['./products.component.css']
})
export class ProductsComponent implements OnInit {

  favFilter = {
    rate: 1
  };

  prodFilter = {
    rate: 0
  };

  products = [{
    name: "Producto 1",
    price: 99.99,
    scope: .036,
    rate: 0
  },{
    name: "Producto 2",
    price: 34.50,
    scope: .026,
    rate: 0
  },{
    name: "Producto 3",
    price: 112.99,
    scope: -.012,
    rate: 1
  }, {
    name: "Producto 4",
    price: 70.45,
    scope: .011,
    rate: 1
  }, {
    name: "Producto 5",
    price: 87.99,
    scope: -.076,
    rate: 0
  }];

  constructor() { }

  ngOnInit() {
  }

  clickStar(product: any){
    if (product.rate == 1)
      return product.rate = 0;
    return product.rate = 1;
  }


}
