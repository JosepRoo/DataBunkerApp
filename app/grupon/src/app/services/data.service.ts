import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { throwError } from 'rxjs';
import { DatePipe } from '../../../node_modules/@angular/common';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  // base refs
  private elementsUrl: string = environment.url + '/elements';
  private subElementsUrl: string = environment.url + '/subelements';
  private valueUrl: string = environment.url + '/elementvalue';

  // get refs
  private channelUrl: string = this.elementsUrl + '/channel';

  // get subelements refs
  private channelSubElementsUrl: string = this.subElementsUrl + '/channel';
  private categorySubElementsUrl: string = this.subElementsUrl + '/category';
  private brandSubElementsUrl: string = this.subElementsUrl + '/brand';

  // get value refs
  private productsValue: string = this.valueUrl + '/product';

  private headers = new HttpHeaders({ 'Content-Type': 'application/json' });

  constructor(private http: HttpClient, public router: Router, private datePipe: DatePipe) {}

  getChannels(): Observable<any> {
    return this.http.get(this.channelUrl, { headers: this.headers }).pipe(
      map(res => {
        return res;
      }),
      catchError(e => {
        if (e.status === 401) {
          this.router.navigate(['../']);
          return throwError(e.error.message);
        }
      })
    );
  }

  getCategories(channelId): Observable<any> {
    return this.http
      .get(this.channelSubElementsUrl + '/' + channelId, {
        headers: this.headers
      })
      .pipe(
        map(res => {
          return res;
        }),
        catchError(e => {
          if (e.status === 401) {
            this.router.navigate(['../']);
            return throwError(e.error.message);
          }
        })
      );
  }

  getBrands(categoryId): Observable<any> {
    return this.http
      .get(this.categorySubElementsUrl + '/' + categoryId, {
        headers: this.headers
      })
      .pipe(
        map(res => {
          return res;
        }),
        catchError(e => {
          if (e.status === 401) {
            this.router.navigate(['../']);
            return throwError(e.error.message);
          }
        })
      );
  }

  getProducts(brandId): Observable<any> {
    return this.http
      .get(this.brandSubElementsUrl + '/' + brandId, {
        headers: this.headers
      })
      .pipe(
        map(res => {
          return res;
        }),
        catchError(e => {
          if (e.status === 401) {
            this.router.navigate(['../']);
            return throwError(e.error.message);
          }
        })
      );
  }

  getProductData(productId, starDate, endDate): Observable<any> {
    return this.http
      .get(this.productsValue + '/' +
            productId + '/' +
            this.datePipe.transform(starDate, 'yyyy-MM-dd') + '/' +
            this.datePipe.transform(endDate, 'yyyy-MM-dd'), { headers: this.headers })
      .pipe(
        map(res => {
          return res;
        }),
        catchError(e => {
          if (e.status === 401) {
            this.router.navigate(['../']);
            return throwError(e.error.message);
          }
        })
      );
  }
}
