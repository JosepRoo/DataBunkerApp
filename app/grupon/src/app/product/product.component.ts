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
        res.values = res.sub_elements;
        res.values.map(el => {
          el._id = new Date(el.date);
          el.average = el.value;
        });
        this.product = res;
        this.product.channel = '';
        this.selectedData.push(this.product);
        this.product.values.forEach(element => {
          const day = new Date(element.date);
          this.lineChartLabels.push(day);
        });
      }, error => {
        this.router.navigate(['/app']);
      });
    });
  }
}
