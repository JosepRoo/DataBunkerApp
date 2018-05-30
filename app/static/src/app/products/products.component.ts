import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { MyFilterPipe } from './favoritePipe';

import { MessageService } from '../services/messages.service';
import { ChannelService } from '../services/channels.service';
import { ColorGeneratorService } from '../services/colorGenerator.service';

// classes
import { Line } from '../classes/line';
import { Channel } from '../classes/channel';

@Component({
  selector: 'app-products',
  templateUrl: './products.component.html',
  styleUrls: ['./products.component.css']
})
export class ProductsComponent implements OnInit {

  channels: Channel[];
  line = new Line();

  startDate : Date = new Date();
  endDate: Date = new Date();

  favorites = [];

  prodFilter = {
    rate: 0
  };

  products = [];

  constructor(
    private messageService: MessageService,
    private channelService: ChannelService,
    private colorGenerator: ColorGeneratorService
  ) { }

  ngOnInit() {
    var self = this;
    this.channelService.getChannels().subscribe(res => {
      self.channels = res.sort((a, b) => {
    if (a.name < b.name) return -1;
    else if (a.name > b.name) return 1;
    else return 0;
  });;
    }, (err) => {
        if (err === 'Unauthorized'){
        }
    });

    this.startDate.setDate(this.endDate.getDate()-30);
    this.channelService.getFavorites().subscribe(res => {
      self.favorites = res
      for (var i = 0; i < self.favorites.length; i++){
        self.favorites[i].scope = (self.favorites[i].sub_elements[1].value - self.favorites[i].sub_elements[0].value)*100/self.favorites[i].sub_elements[1].value;
      }
    });
  }

  addLine() {
    var self = this;
    this.line.name = this.line.product.name;
    this.channelService.getProduct(this.line.product._id).subscribe(res => {
      self.line.data = res;
      res.scope = (res.sub_elements[1].value - res.sub_elements[0].value)*100/res.sub_elements[1].value;
      self.products.push(res);
      self.line.color = self.colorGenerator.getColor();
      self.line.product = null;
    }, (err) => {
        if (err === 'Unauthorized'){
        }
    });
  }

  getCategories() {
    var self = this;
    self.line.category = null;
    self.line.brand = null;
    self.line.product = null;
    if (this.line.channel)
      this.channelService.getChannelSubElemenets(this.line.channel._id).subscribe(res => {
        self.line.channel.sub_elements = res.sort((a, b) => {
          if (a.name < b.name) return -1;
          else if (a.name > b.name) return 1;
          else return 0;
        });;
      }, (err) => {
          if (err === 'Unauthorized'){
          }
      });
  }

  getBrands() {
    var self = this;
    self.line.brand = null;
    self.line.product = null;
    if (this.line.category)
      this.channelService.getCategorySubElemenets(this.line.category._id).subscribe(res => {
        self.line.category.sub_elements = res.sort((a, b) => {
    if (a.name < b.name) return -1;
    else if (a.name > b.name) return 1;
    else return 0;
  });;
      }, (err) => {
          if (err === 'Unauthorized'){
          }
      });
  }

  getProducts() {
    var self = this;
    self.line.product = null;
    if (this.line.brand)
      this.channelService.getBrandSubElemenets(this.line.brand._id).subscribe(res => {
        self.line.brand.sub_elements = res.sort((a, b) => {
    if (a.name < b.name) return -1;
    else if (a.name > b.name) return 1;
    else return 0;
  });;
      }, (err) => {
          if (err === 'Unauthorized'){
          }
      });
  }

  clickStar(product: any){
    var self = this;
    this.channelService.addFavorite(product._id).subscribe(res=> {
      console.log(res);
      this.channelService.getFavorites().subscribe(res => {self.favorites = res});
    });
  }

  removeStar(product: any){
    var self = this;
    this.channelService.removeFavorite(product._id).subscribe(res=> {
      console.log(res);
      this.channelService.getFavorites().subscribe(res => {self.favorites = res});
    });
  }




}
