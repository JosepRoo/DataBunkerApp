import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { FullComponent } from './layouts/full/full.component';
import { BlankComponent } from './layouts/blank/blank.component';
import { LogInComponent } from './log-in/log-in.component';
import { ProductsComponent } from './products/products.component';
import { ProductDetailComponent } from './product-detail/product-detail.component';
import { RecoverPasswoordComponent } from './recover-passwoord/recover-passwoord.component';



export const routes: Routes = [
{
    path: '',
    component: FullComponent,
    children: [
        { path: '', redirectTo: 'comparador', pathMatch: 'full' },
        { path: 'comparador', loadChildren: './starter/starter.module#StarterModule' },
        { path: 'component', loadChildren: './component/component.module#ComponentsModule' },
        { path: 'products', component: ProductsComponent, data: {
          title: 'Principal',
          urls: [{title: 'Principal',url: '/products'}, {title: 'Productos'}]
        } },
        { path: 'products/:id', component: ProductDetailComponent, data: {
          title: 'Principal',
          urls: [{title: 'Principal',url: '/products'}, {title: 'Productos'}]
        } }
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
        },
        { path: 'recoverPassword', data: {
              title: 'Recuperar Contraseña',
              urls: [{title: 'Recuperar Contraseña', url: '/recoverPassword'}, {title: 'Recuperar Contraseña'}]
          },
          component: RecoverPasswoordComponent
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
