import { element } from 'protractor';
import { Component, OnInit, Output, Input } from '@angular/core';

// Services
import { DataService } from './../services/data.service';
import { EventEmitter } from '@angular/core';
import { ELEMENT_PROBE_PROVIDERS } from '../../../node_modules/@angular/platform-browser/src/dom/debug/ng_probe';

@Component({
  selector: 'app-data-select',
  templateUrl: './data-select.component.html',
  styleUrls: ['./data-select.component.scss']
})
export class DataSelectComponent implements OnInit {
  channels: Array<any>;
  categories: Array<any>;
  brands: Array<any>;
  products: Array<any>;
  loading = true;
  error = {
    show: false,
    text: ''
  };
  selectedData = {
    channels: [],
    categories: [],
    brands: [],
    products: []
  };
  endDate: Date;
  today: Date;

  // Outputs
  @Output() status: EventEmitter<any> = new EventEmitter();
  @Output() productsSelected: EventEmitter<any> = new EventEmitter();
  @Output() dateChanged: EventEmitter<any> = new EventEmitter();

  // Inputs
  @Input() startDate: Date;
  @Input() isDateDisabled: Boolean;
  @Input() filterLabel: String;

  constructor(private dataService: DataService) {}

  ngOnInit() {
    this.endDate = new Date();
    this.today = new Date();
    this.dataService.getChannels().subscribe(res => {
      this.channels = res;
      this.loading = false;
    });
    if (!this.filterLabel) {
      this.filterLabel = 'Filtros';
    }
  }

  printInfo() {
    console.log(this.selectedData);
  }

  channelChanged() {
    for (let index = 0; index < this.selectedData.channels.length; index++) {
      const channel = this.selectedData.channels[index];
      if (channel.categories == null) {
        this.dataService.getCategories(channel._id).subscribe(res => {
          res.map(category => {
            category.channel = channel.name;
            category.channel_id = channel._id;
          });
          channel.categories = res;
        });
      }
    }
    if (this.selectedData.channels.length && !this.loading) {
      this.status.emit(true);
    } else {
      this.status.emit(false);
    }
  }

  categoryChanged() {
    for (let index = 0; index < this.selectedData.categories.length; index++) {
      const category = this.selectedData.categories[index];
      if (category.brands == null) {
        this.dataService.getBrands(category._id).subscribe(res => {
          res.map(brand => {
            brand.channel = category.channel;
            brand.channel_id = category.channel_id;
          });
          category.brands = res;
        });
      }
    }
  }

  brandChanged() {
    for (let index = 0; index < this.selectedData.brands.length; index++) {
      const brand = this.selectedData.brands[index];
      if (brand.products == null) {
        this.dataService.getProducts(brand._id).subscribe(res => {
          res.map(product => {
            product.channel = brand.channel;
          });
          brand.products = res;
        });
      }
    }
  }

  productChanged() {
    if (this.selectedData.products.length && !this.loading) {
      this.productsSelected.emit(true);
    } else {
      this.productsSelected.emit(false);
    }
  }

  getData() {
    const data: any = {};
    if (this.selectedData.products.length) {
      data.type = 'products';
      data.data = this.selectedData.products;
    } else if (this.selectedData.brands.length) {
      data.type = 'brands';
      data.data = this.selectedData.brands;
    } else if (this.selectedData.categories.length) {
      data.type = 'categories';
      data.data = this.selectedData.categories;
    } else if (this.selectedData.channels.length) {
      data.type = 'channels';
      data.data = this.selectedData.channels;
    }
    return data;
  }

  getPrivileges() {
    const privileges: any = [];
    if (this.selectedData.products.length) {
      this.selectedData.products.forEach(_element => {
        const data: any = {};
        data.element_type = 'product';
        data.element = {};
        data.element[_element.greatGrandParentId] = {
          [_element.grandParentId]: {
            [_element.parentElementId]: {
              [_element._id]: 1
            }
          }
        };
        privileges.push(data);
      });
    } else if (this.selectedData.brands.length) {
      this.selectedData.brands.forEach(_element => {
        const data: any = {};
        data.element_type = 'brand';
        data.element = {};
        data.element[_element.channel_id] = {
          [_element.parentElementId]: {
            [_element._id]: 1
          }
        };
        privileges.push(data);
      });
    } else if (this.selectedData.categories.length) {
      this.selectedData.categories.forEach(_element => {
        const data: any = {};
        data.element_type = 'category';
        data.element = {};
        data.element[_element.parentElementId] = {
          [_element._id]: 1
        };
        privileges.push(data);
      });
    } else if (this.selectedData.channels.length) {
      this.selectedData.channels.forEach(_element => {
        const data: any = {};
        data.element_type = 'channel';
        data.element = {};
        data.element[_element._id] = 1;
        privileges.push(data);
      });
    }
    return privileges;
  }

  getStartDate() {
    return this.startDate;
  }

  getEndDate() {
    return this.endDate;
  }

  onDateChanged() {
    this.dateChanged.emit(true);
  }
}
