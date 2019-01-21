import {
  Component,
  OnInit,
  Input,
  OnChanges
} from '@angular/core';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.scss']
})
export class GraphComponent implements OnInit, OnChanges {
  @Input()
  selectedData: any;
  @Input()
  lineChartLabels: any;
  lineChartData = [];
  lineChartOptions: any = {
    responsive: true,
    bezierCurve: false,
    legend: {
        display: false
    },
    maintainAspectRatio: false,
    tooltips: {
      enabled: true,
      mode: 'single',
      callbacks: {
        title: function(_tooltipItems) {
          const date = new Date(_tooltipItems[0].xLabel);
          const str = date.toString().split(' ');
          return str[0] + ' ' + str[1] + ' ' + str[2];
        },
        label: function(tooltipItems, data) {
          return (
            '$' +
            tooltipItems.yLabel +
            ' - ' +
            data.datasets[tooltipItems.datasetIndex].label
          );
        }
      }
    },
    spanGaps: true,
    pan: {
      enabled: true,
      mode: 'x',
      rangeMin: {
        x: null,
        y: 1
      },
      rangeMax: {
        x: null,
        y: 50000
      }
    },
    zoom: {
      enabled: true,
      mode: 'x',
      rangeMin: {
        x: null,
        y: 0
      },
      rangeMax: {
        x: null,
        y: 50000
      }
    },
    scales: {
      xAxes: [
        {
          type: 'time',
          time: {
            displayFormats: {
              day: 'MMM DD',
              week: 'MMM DD',
              month: 'MMM DD',
              quarter: 'MMM DD',
              year: 'MMM DD'
            }
          }
        }
      ],
      yAxes: [
        {
          ticks: {
            callback: function(value) {
              value += '';
              const x = value.split('.');
              let x1 = x[0];
              const x2 = x.length > 1 ? '.' + x[1] : '';
              const rgx = /(\d+)(\d{3})/;
              while (rgx.test(x1)) {
                x1 = x1.replace(rgx, '$1' + ',' + '$2');
              }
              return '$' + x1 + x2;
            }
          }
        }
      ]
    }
  };
  lineChartLegend: Boolean = true;
  lineChartType: String = 'line';

  constructor() {}

  ngOnInit() {}

  ngOnChanges() {
    this.lineChartData = [];
    Promise.resolve(true).then(() => this.refresh());
  }

  refresh() {
    const lines = [];
    this.selectedData.forEach(product => {
      const data = {
        data: [],
        fill: false,
        label: product.channel + ' - ' + product.name
      };
      this.lineChartLabels.forEach(day => {
        const price = product.values.find(value => {
          let day1 = value._id.toUTCString();
          day1 = day1
            .split(' ')
            .slice(0, 4)
            .join(' ');
          let day2 = day.toUTCString();
          day2 = day2
            .split(' ')
            .slice(0, 4)
            .join(' ');
          if (day1 === day2) {
            return value;
          } else {
            return null;
          }
        });
        if (price) {
          data.data.push(price.average);
        } else {
          data.data.push(null);
        }
      });
      lines.push(data);
    });
    this.lineChartData = lines;
  }

  public getHeight() {
    let height;
    if (this.selectedData) {
      height = this.selectedData.length * 40;
      console.log(height);
    }
    if (height < 400) {
      return 400;
    } else {
      return height;
    }
  }

  // events
  public chartClicked(e: any): void {
    console.log(e);
  }

  public chartHovered(e: any): void {
    console.log(e);
  }
}
