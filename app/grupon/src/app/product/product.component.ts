import { Router } from '@angular/router';
import { DataService } from './../services/data.service';
import { ActivatedRoute } from '@angular/router';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.scss']
})
export class ProductComponent implements OnInit {
  product_id: any;
  product: any;
  loading: Boolean;
  selectedData = [];
  lineChartLabels = [];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private dataService: DataService
  ) {}

  ngOnInit() {
    this.loading = true;
    this.route.params.subscribe(params => {
      this.loading = false;
      this.product_id = params['id'];
      this.dataService.getProduct(this.product_id).subscribe(res => {
        const date = new Date();
        const today = new Date();
        date.setMonth(date.getMonth() - 3);
        this.dataService.getProductData(this.product_id, date, today).subscribe(
          _res => {
            res.values = _res.map(el => {
              if (el._id) {
                el._id = new Date(el._id.replace('/', '-'));
                return el;
              }
            });
            res.values.sort(function (a, b) {
              a = a._id;
              b = b._id;
              return a > b ? -1 : a < b ? 1 : 0;
            });
            res.values = res.values.filter(el =>
              el !== 0
            );
            this.product = res;
            this.product.channel = '';
            this.selectedData.push(this.product);
            this.product.values.forEach(element => {
              const day = new Date(element._id);
              this.lineChartLabels.push(day);
            });
          }
        );
      }, error => {
        this.router.navigate(['/app']);
      });
    });
  }
}
