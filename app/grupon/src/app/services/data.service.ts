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
  private favoriteUrl: string = environment.url + '/user/favorites';

  // get refs
  private channelUrl: string = this.elementsUrl + '/channel';

  // get subelements refs
  private channelSubElementsUrl: string = this.subElementsUrl + '/channel';
  private categorySubElementsUrl: string = this.subElementsUrl + '/category';
  private brandSubElementsUrl: string = this.subElementsUrl + '/brand';

  // export
  private exportChannels: string = this.elementsUrl + '/channel/report';
  private exportCategories: string = this.elementsUrl + '/category/report';
  private exportBrands: string = this.elementsUrl + '/brand/report';
  private exportProducts: string = this.elementsUrl + '/product/report';

  // get value refs
  private productsValue: string = this.valueUrl + '/product';

  private headers = new HttpHeaders({ 'Content-Type': 'application/json' });

  constructor(
    private http: HttpClient,
    public router: Router,
    private datePipe: DatePipe
  ) {}

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
      .get(
        this.productsValue +
          '/' +
          productId +
          '/' +
          this.datePipe.transform(starDate, 'yyyy-MM-dd') +
          '/' +
          this.datePipe.transform(endDate, 'yyyy-MM-dd'),
        { headers: this.headers }
      )
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

  addFavorite(productId): Observable<any> {
    const data = {
      product_id: productId
    };
    return this.http
      .put(this.favoriteUrl, data, {
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
          } else {
            return throwError(e);
          }
        })
      );
  }

  exportData(idArray, type, starDate, endDate): Observable<any> {
    let url;
    switch (type) {
      case 'channels':
        url = this.exportChannels;
        break;
      case 'categories':
        url = this.exportCategories;
        break;
      case 'brands':
        url = this.exportBrands;
        break;
      case 'products':
        url = this.exportProducts;
        break;
      default:
        break;
    }
    let ids = idArray[0];
    for (let index = 1; index < idArray.length; index++) {
      const element = idArray[index];
      ids = ids + '&&' + element;
    }
    return this.http
      .get(
        url +
          '/' +
          ids +
          '/' +
          this.datePipe.transform(starDate, 'yyyy-MM-dd') +
          '/' +
          this.datePipe.transform(endDate, 'yyyy-MM-dd'),
        { headers: this.headers }
      )
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
