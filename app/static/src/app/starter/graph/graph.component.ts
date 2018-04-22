import { Component } from '@angular/core';
import { AmChartsService, AmChart } from "@amcharts/amcharts3-angular"

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent {

  private chart: AmChart;

  constructor(private AmCharts: AmChartsService) {

  }

  generateChartData() {
      var chartData = [];
      var firstDate = new Date();
      firstDate.setDate(firstDate.getDate() - 100);

          var visits = 1000;
          var hits = 1000;
          var views = 1000;


      for (var i = 0; i < 100; i++) {
          // we create date objects here. In your data, you can have date strings
          // and then set format of your dates using chart.dataDateFormat property,
          // however when possible, use date objects, as this will speed up chart rendering.
          var newDate = new Date(firstDate);
          newDate.setDate(newDate.getDate() + i);

          visits += Math.round((Math.random()<0.5?1:-1)*Math.random()*10);
          hits += Math.round((Math.random()<0.5?1:-1)*Math.random()*10);
          views += Math.round((Math.random()<0.5?1:-1)*Math.random()*10);

          chartData.push({
              date: newDate,
              visits: visits,
              hits: hits,
              views: views
          });
      }
      return chartData;
  }

  ngAfterViewInit() {
    var chartData = this.generateChartData();
    this.chart = this.AmCharts.makeChart("chartdiv", {
        "type": "serial",
        "theme": "none",
        "legend": {
            "useGraphSettings": true
        },
        "dataProvider": chartData,
        "synchronizeGrid":true,
        "valueAxes": [
          {
            "id":"v1",
            "axisColor": "gray",
            "axisThickness": 1,
            "axisAlpha": 1,
            "position": "left"
          }
        // }, {
        //     "id":"v2",
        //     "axisColor": "green",
        //     "axisThickness": 2,
        //     "axisAlpha": 1,
        //     "position": "right"
        // }, {
        //     "id":"v3",
        //     "axisColor": "purple",
        //     "axisThickness": 2,
        //     "gridAlpha": 0,
        //     "offset": 50,
        //     "axisAlpha": 1,
        //     "position": "left"
        // }
      ],
        "graphs": [{
            "valueAxis": "v1",
            "lineColor": "#009efb",
            "bullet": "round",
            "bulletBorderThickness": 1,
            "hideBulletsCount": 30,
            "title": "Producto 1",
            "valueField": "visits",
    		"fillAlphas": 0
        }, {
            "valueAxis": "v2",
            "lineColor": "rgb(101, 186, 105)",
            "bullet": "square",
            "bulletBorderThickness": 1,
            "hideBulletsCount": 30,
            "title": "Producto 2",
            "valueField": "hits",
    		"fillAlphas": 0
        }, {
            "valueAxis": "v3",
            "lineColor": "#5c4ac7",
            "bullet": "triangleUp",
            "bulletBorderThickness": 1,
            "hideBulletsCount": 30,
            "title": "Producto 3",
            "valueField": "views",
    		"fillAlphas": 0
        }],
        "chartScrollbar": {},
        "chartCursor": {
            "cursorPosition": "mouse"
        },
        "categoryField": "date",
        "categoryAxis": {
            "parseDates": true,
            "axisColor": "#DADADA",
            "minorGridEnabled": true
        },
        "export": {
        	"enabled": true,
          "divId": "exportdiv"
        }
    });
  }

  ngOnDestroy() {
    if (this.chart) {
      this.AmCharts.destroyChart(this.chart);
    }
  }

}
