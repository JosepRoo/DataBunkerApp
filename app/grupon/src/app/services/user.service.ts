import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { throwError } from 'rxjs';
import * as shajs from 'sha.js';

@Injectable()
export class UserService {

  private userUrl: string = environment.url + '/userstatus';
  private user: string = environment.url + '/user';
  private headers = new HttpHeaders({ 'Content-Type': 'application/json' });

  constructor(private http: HttpClient, public router: Router) {}

  logIn(data): Observable<any> {
    data.password = shajs('sha256')
      .update(data.password)
      .digest('hex');
    return this.http
      .post(this.userUrl, JSON.stringify(data), { headers: this.headers })
      .pipe(
        map(res => {
          return res;
        }),
        catchError(e => {
          if (e.status === 401) {
            return throwError(e.error.message);
          }
        })
      );
  }

  getUser(): Observable<any> {
    return this.http.get(this.user, { headers: this.headers }).pipe(
      map(res => {
        return res;
      }),
      catchError(e => {
        if (e.status === 401 || e.status === 400) {
          this.router.navigate(['../']);
          return throwError(e.error.message);
        }
      })
    );
  }
}
