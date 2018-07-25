import { DataService } from './../services/data.service';
import { Component, OnInit, ViewChild, OnDestroy } from '@angular/core';
import { DataSelectComponent } from './../data-select/data-select.component';
import { AmChartsService, AmChart } from '@amcharts/amcharts3-angular';

// Services

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, OnDestroy {
  buttonStatus: Boolean = false;
  startDate: Date;
  selectedData: any = [];
  chartLoading: Boolean = false;
  dateChanged = false;
  subscribes = [];
  chart: AmChart;

  // Children
  @ViewChild(DataSelectComponent) dataSelect: DataSelectComponent;

  constructor(
    private dataService: DataService,
    private AmCharts: AmChartsService
  ) {}

  ngOnInit() {
    this.startDate = new Date();
    this.startDate.setMonth(this.startDate.getMonth() - 3);
    this.chart = this.AmCharts.makeChart('chartdiv', {
      type: 'serial',
      theme: 'light',
      legend: {
        'useGraphSettings': true
      },
      dataProvider: [],
      synchronizeGrid: true,
    });
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

  ngOnDestroy() {
    if (this.chart) {
      this.AmCharts.destroyChart(this.chart);
    }
  }
}
