import { DataService } from './../services/data.service';
import { Component, OnInit, ViewChild, OnDestroy } from '@angular/core';
import { DataSelectComponent } from './../data-select/data-select.component';

// Services

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

  // Children
  @ViewChild(DataSelectComponent) dataSelect: DataSelectComponent;

  constructor(
    private dataService: DataService,
  ) {}

  ngOnInit() {
    this.startDate = new Date();
    this.startDate.setMonth(this.startDate.getMonth() - 3);
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
    this.selectedData.forEach(product => {
      if (!product.values || this.dateChanged) {
        this.chartLoading = true;
        this.subscribes.push({ id: product._id });
        this.dataService
          .getProductData(
            product._id,
            this.dataSelect.getStartDate(),
            this.dataSelect.getEndDate()
          )
          .subscribe(res => {
            product.values = res;
            this.subscribes.splice(0, 1);
            if (!this.subscribes.length) {
              this.chartLoading = false;
            }
          });
      }
    });
    this.dateChanged = false;
  }

  onDateChanged() {
    this.dateChanged = true;
  }
}
