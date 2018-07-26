import { Component, OnInit, ViewChild } from '@angular/core';

// Components
import { DataSelectComponent } from './../data-select/data-select.component';

@Component({
  selector: 'app-export',
  templateUrl: './export.component.html',
  styleUrls: ['./export.component.scss']
})
export class ExportComponent implements OnInit {
  buttonStatus: Boolean = false;
  startDate: Date;
  selectedData: any;

  // Children
  @ViewChild(DataSelectComponent) dataSelect: DataSelectComponent;

  constructor() {}

  ngOnInit() {
    this.startDate = new Date();
  }

  switchButton(status) {
    this.buttonStatus = status;
  }

  getSelectedData() {
    this.selectedData = this.dataSelect.getData();
    console.log(this.selectedData);
  }
}
