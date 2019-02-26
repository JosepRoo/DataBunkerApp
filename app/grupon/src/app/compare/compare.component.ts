import { DataService } from './../services/data.service';
import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { MatPaginator, MatSort, MatTableDataSource } from '../../../node_modules/@angular/material';
import * as XLSX from 'xlsx';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-compare',
  templateUrl: './compare.component.html',
  styleUrls: ['./compare.component.scss']
})
export class CompareComponent implements OnInit {
  error = {
    text: '',
    show: false
  };
  user: any;
  loading: Boolean = false;
  displayedColumns: string[] = ['Nombre'];
  @ViewChild(MatPaginator)
  paginator: MatPaginator;
  @ViewChild(MatSort)
  sort: MatSort;
  @ViewChild('TABLE')
  table: ElementRef;
  data: MatTableDataSource<any>;
  errorData = false;

  constructor(
    private dataService: DataService,
    private userService: UserService
  ) {}

  ngOnInit() {
    this.getData();
    this.userService.getUser().subscribe(res => {
      this.user = res;
    });
  }

  exportTable() {
    this.dataService.exportTable();
  }

  getData() {
    const self = this;
    this.loading = true;
    this.dataService.getCompare().subscribe(res => {
      this.loading = false;
      this.errorData = false;
      res.forEach(el => {
        Object.keys(el).forEach(column => {
          if (column !== 'Nombre' && column !== 'UPC') {
            el['% - ' + column] = this.getDifference(el, el[column]);
          }
        });
      });
      self.data = new MatTableDataSource(res);
      self.data.sort = self.sort;
      self.data.paginator = self.paginator;
      if (res.length) {
        const headers = Object.keys(res[0]);
        const nameIndex = headers.indexOf('Nombre');
        let badLocated = headers[0];
        headers[0] = headers[nameIndex];
        headers[nameIndex] = badLocated;
        const upcIndex = headers.indexOf('UPC');
        badLocated = headers[1];
        headers[1] = headers[upcIndex];
        headers[upcIndex] = badLocated;
        const mainChannel = headers.indexOf(this.user.channel_name);
        badLocated = headers[2];
        headers[2] = headers[mainChannel];
        headers[mainChannel] = badLocated;
        this.displayedColumns = headers;
      }
    }, error => {
      this.loading = false;
      this.errorData = true;
    });
  }

  getDifference(product, price) {
    if (price === 0) {
      return 0;
    }
    const mainPrice = product[this.user.channel_name];
    const difference = ((mainPrice - price)) / mainPrice;
    if (mainPrice === 0) {
      return mainPrice;
    }
    if (difference && difference !== 0) {
      return difference;
    } else {
      return 0;
    }
  }

  exportAsExcel() {
    const ws: XLSX.WorkSheet = XLSX.utils.table_to_sheet(
      this.table.nativeElement
    );
    const wb: XLSX.WorkBook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Productos');
    XLSX.writeFile(wb, 'Comparador.xlsx');
  }

  applyFilter(filterValue: string) {
    this.data.filter = filterValue.trim().toLowerCase();

    if (this.data.paginator) {
      this.data.paginator.firstPage();
    }
  }
}
