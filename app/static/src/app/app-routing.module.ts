import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { FullComponent } from './layouts/full/full.component';
import { BlankComponent } from './layouts/blank/blank.component';
import { LogInComponent } from './log-in/log-in.component';

export const routes: Routes = [
{
    path: '',
    component: FullComponent,
    children: [
        { path: '', redirectTo: 'comparador', pathMatch: 'full' },
        { path: 'comparador', loadChildren: './starter/starter.module#StarterModule' },
        { path: 'component', loadChildren: './component/component.module#ComponentsModule' }
    ]
},
{
    path: 'screen',
    component: BlankComponent,
    children: [
        { path: '', redirectTo: 'logIn', pathMatch: 'full' },
        { path: 'logIn', data: {
              title: 'Log In',
              urls: [{title: 'Log In', url: '/logIn'}, {title: 'Log In'}]
          },
          component: LogInComponent
        }
    ]
},
{
    path: '**',
    redirectTo: 'comparador'
}];

@NgModule({
    imports: [RouterModule.forRoot(routes), NgbModule.forRoot()],
    exports: [RouterModule]
})
export class AppRoutingModule { }
