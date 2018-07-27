import { DataService } from './../services/data.service';
import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { MatPaginator, MatSort, MatTableDataSource } from '../../../node_modules/@angular/material';
import * as XLSX from 'xlsx';

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
  loading: Boolean = false;
  displayedColumns: string[] = ['Nombre'];
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  @ViewChild('TABLE') table: ElementRef;
  data: MatTableDataSource<any>;

  constructor(private dataService: DataService) {}

  ngOnInit() {
    const self = this;
    this.loading = true;
    this.dataService.getCompare().subscribe(res => {
      this.loading = false;
      this.data = new MatTableDataSource(res);
      this.data.paginator = self.paginator;
      this.data.sort = self.sort;
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
        this.displayedColumns = headers;
        console.log(this.table);
      }
    });
  }

  exportAsExcel() {
    const ws: XLSX.WorkSheet = XLSX.utils.table_to_sheet(this.table.nativeElement);
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
