import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Components
import { InSessionComponent } from './templates/in-session/in-session.component';
import { OutSessionComponent } from './templates/out-session/out-session.component';
import { LogInComponent } from './log-in/log-in.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ExportComponent } from './export/export.component';

const routes: Routes = [
  {
    path: 'app',
    component: InSessionComponent,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: DashboardComponent },
      { path: 'export', component: ExportComponent },
      { path: '**', component: DashboardComponent }
    ]
  },
  {
    path: '',
    component: OutSessionComponent,
    children: [
      { path: '', redirectTo: 'logIn', pathMatch: 'full' },
      { path: 'logIn', component: LogInComponent },
      { path: '**', component: LogInComponent }
    ]
  },
  {
    path: '**',
    redirectTo: 'app'
  }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { useHash: true })
  ],
  exports: [
    RouterModule
  ],
  declarations: []
})
export class AppRoutingModule { }
