import { map } from 'rxjs/operators';
import { DataService } from './../services/data.service';
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
  loading: Boolean = false;

  // Children
  @ViewChild(DataSelectComponent) dataSelect: DataSelectComponent;

  constructor(
    private dataService: DataService
  ) {}

  ngOnInit() {
    this.startDate = new Date();
  }

  switchButton(status) {
    this.buttonStatus = status;
  }

  getSelectedData() {
    this.selectedData = this.dataSelect.getData();
    const ids = this.selectedData.data.map(el => {
      return el._id;
    });
    this.loading = true;
    this.dataService.exportData(
      ids,
      this.selectedData.type,
      this.dataSelect.getStartDate(),
      this.dataSelect.getEndDate());
    this.loading = false;
  }
}
