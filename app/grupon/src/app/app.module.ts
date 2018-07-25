import { AppRoutingModule } from './app.routing';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HttpClientModule } from '@angular/common/http';
import { MomentModule } from 'angular2-moment';

// Angular material modules
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule, MatNativeDateModule } from '@angular/material';
import { MatInputModule } from '@angular/material';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatSelectModule } from '@angular/material/select';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MAT_DATE_LOCALE } from '@angular/material';
import { MatExpansionModule } from '@angular/material/expansion';

// Charts
// import { AmChartsModule } from '@amcharts/amcharts3-angular';
import { ChartsModule } from 'ng2-charts';

// Services
import { UserService } from './services/user.service';
import { DataService } from './services/data.service';

// Components
import { InSessionComponent } from './templates/in-session/in-session.component';
import { OutSessionComponent } from './templates/out-session/out-session.component';
import { LogInComponent } from './log-in/log-in.component';
import { ErrorSnackComponent } from './log-in/log-in.component';
import { SideNavbarComponent } from './templates/in-session/side-navbar/side-navbar.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ExportComponent } from './export/export.component';
import { DataSelectComponent } from './data-select/data-select.component';
import { ProductsListComponent } from './dashboard/products-list/products-list.component';

@NgModule({
  declarations: [
    AppComponent,
    InSessionComponent,
    OutSessionComponent,
    LogInComponent,
    ErrorSnackComponent,
    SideNavbarComponent,
    DashboardComponent,
    ExportComponent,
    DataSelectComponent,
    ProductsListComponent
  ],
  imports: [
    // angular dependencies
    BrowserModule,
    BrowserAnimationsModule,
    NgbModule.forRoot(),
    AppRoutingModule,
    ReactiveFormsModule,
    FormsModule,
    HttpClientModule,
    MatListModule,
    MomentModule,
    // material modules
    MatCardModule,
    MatInputModule,
    MatFormFieldModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    MatSnackBarModule,
    MatSidenavModule,
    MatToolbarModule,
    MatIconModule,
    MatSelectModule,
    MatAutocompleteModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatExpansionModule,
    // charts modules
    ChartsModule
  ],
  entryComponents: [ErrorSnackComponent],
  providers: [
    UserService,
    DataService,
    { provide: MAT_DATE_LOCALE, useValue: 'es-ES' }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
