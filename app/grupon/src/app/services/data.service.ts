import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private elementsUrl: string = environment.url + '/elements';
  private subElementsUrl: string = environment.url + '/subelements';
  private channelUrl: string = this.elementsUrl + '/channel';
  private channelSubElementsUrl: string = this.subElementsUrl + '/channel';
  private categorySubElementsUrl: string = this.subElementsUrl + '/category';
  private brandSubElementsUrl: string = this.subElementsUrl + '/brand';
  private headers = new HttpHeaders({ 'Content-Type': 'application/json' });

  constructor(private http: HttpClient, public router: Router) {}

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
      .pipe( map(res => {
          return res;
        }), catchError(e => {
          if (e.status === 401) {
            this.router.navigate(['../']);
            return throwError(e.error.message);
          }
        }) );
  }
}
