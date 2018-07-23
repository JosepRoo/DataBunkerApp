import { Component, OnInit, Pipe } from '@angular/core';

// Services
import { DataService } from './../services/data.service';

@Component({
  selector: 'app-export',
  templateUrl: './export.component.html',
  styleUrls: ['./export.component.scss']
})
export class ExportComponent implements OnInit {
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
    brands: []
  };
  startDate: Date;
  endDate: Date;
  today: Date;

  constructor(private dataService: DataService) {}

  ngOnInit() {
    this.startDate = new Date();
    this.endDate = new Date();
    this.today = new Date();
    this.dataService.getChannels().subscribe(res => {
      this.channels = res;
      this.loading = false;
    });
  }

  printInfo() {
    console.log(this.selectedData);
  }

  channelChanged() {
    for (let index = 0; index < this.selectedData.channels.length; index++) {
      const channel = this.selectedData.channels[index];
      if (channel.categories == null) {
        this.dataService.getCategories(channel._id).subscribe(res => {
          channel.categories = res;
        });
      }
    }
  }

  categoryChanged() {
    for (let index = 0; index < this.selectedData.categories.length; index++) {
      const category = this.selectedData.categories[index];
      if (category.brands == null) {
        this.dataService.getBrands(category._id).subscribe(res => {
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
          brand.products = res;
        });
      }
    }
  }
}
