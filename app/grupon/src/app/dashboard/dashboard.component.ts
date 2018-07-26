import { DataService } from './../services/data.service';
import { Component, OnInit, ViewChild, OnDestroy } from '@angular/core';
import { DataSelectComponent } from './../data-select/data-select.component';

declare global {
  interface Date {
    addDays(any): Date;
  }
}

Date.prototype.addDays = function (days) {
  const date = new Date(this.valueOf());
  date.setDate(date.getDate() + days);
  return date;
};

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  buttonStatus: Boolean = false;
  startDate: Date;
  selectedData: any = [];
  chartLoading: Boolean = false;
  dateChanged = false;
  subscribes = [];
  lineChartLabels = [];

  // Children
  @ViewChild(DataSelectComponent) dataSelect: DataSelectComponent;

  constructor(private dataService: DataService) {}

  ngOnInit() {
    this.startDate = new Date();
    this.startDate.setMonth(this.startDate.getMonth() - 3);
    this.lineChartLabels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
  }

  switchButton(status) {
    this.buttonStatus = status;
  }

  getSelectedData() {
    const data = this.dataSelect.getData().products;
    for (let index = 0; index < data.length; index++) {
      const product = data[index];
      const find = this.selectedData.find(el => {
        return el._id === product._id;
      });
      if (!find) {
        this.selectedData.push(product);
      }
    }
    this.getProductsValues();
  }

  getProductsValues() {
    let isDataChanged = false;
    this.selectedData.forEach(product => {
      if (!product.values || this.dateChanged) {
        isDataChanged = true;
        this.chartLoading = true;
        this.subscribes.push({ id: product._id });
        this.dataService
          .getProductData(
            product._id,
            this.dataSelect.getStartDate(),
            this.dataSelect.getEndDate()
          )
          .subscribe(res => {
            product.values = res.map(value => {
              value._id = new Date(value._id.replace('/', '-'));
              return value;
            });
            if (product.values.length > 1) {
              product.values.sort(function (a, b) {
                a = new Date(a._id);
                b = new Date(b.d_id);
                return a > b ? -1 : a < b ? 1 : 0;
              });
              const size = product.values.length;
              product.change = (product.values[size - 1].average -
                product.values[size - 2].average) /
                product.values[size - 2].average;
            }
            this.subscribes.splice(0, 1);
            if (!this.subscribes.length) {
              this.chartLoading = false;
            }
          });
      }
    });
    if (isDataChanged) {
      this.generateData();
    }
    this.dateChanged = false;
  }

  onDateChanged() {
    this.dateChanged = true;
  }

  generateData() {
    this.lineChartLabels = this.getDates(this.dataSelect.getStartDate(), this.dataSelect.getEndDate());
  }

  getDates(startDate, stopDate) {
    const dateArray = new Array();
    let currentDate = startDate;
    while (currentDate <= stopDate) {
      dateArray.push(new Date(currentDate));
      currentDate = currentDate.addDays(1);
    }
    return dateArray;
  }

  removeProduct(product) {
    this.selectedData = this.selectedData.filter(function (obj) {
      return obj._id !== product._id;
    });
  }
}
