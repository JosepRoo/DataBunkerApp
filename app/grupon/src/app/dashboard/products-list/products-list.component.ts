import { Component, OnInit, Input, Output, EventEmitter, OnChanges } from '@angular/core';

@Component({
  selector: 'app-products-list',
  templateUrl: './products-list.component.html',
  styleUrls: ['./products-list.component.scss']
})
export class ProductsListComponent implements OnInit, OnChanges {
  @Input() selectedData: any;
  @Output() clickedProduct: EventEmitter<any> = new EventEmitter();

  constructor() {}

  ngOnInit() {}

  ngOnChanges() {
  }
}
