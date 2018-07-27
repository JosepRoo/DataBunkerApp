import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { Location } from '@angular/common';
import { throwError } from 'rxjs';
import * as shajs from 'sha.js';

@Injectable()
export class UserService {
  private userUrl: string = environment.url + '/userstatus';
  private user: string = environment.url + '/user';
  private favorites: string = this.user + '/favorites';
  private headers = new HttpHeaders({ 'Content-Type': 'application/json' });

  constructor(private http: HttpClient, public router: Router, private location: Location) {}

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

  getFavorites(): Observable<any> {
    return this.http
      .get(this.favorites, { headers: this.headers })
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

  logOut(): Observable<any> {
    return this.http
      .delete(this.userUrl, { headers: this.headers })
      .pipe(
        map(res => {
          this.location.replaceState('/');
          this.router.navigate(['/']);
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

  register(user): Observable<any> {
    user.password = shajs('sha256')
      .update(user.password)
      .digest('hex');
    return this.http
      .post(this.user, user, { headers: this.headers })
      .pipe(
        map(res => {
          return res;
        }),
        catchError(e => {
          if (e.status === 401) {
            return throwError(e.error.message);
          } else {
            return throwError(e);
          }
        })
      );
  }

  getUsers(): Observable<any> {
    return this.http
      .get(this.user + 's', { headers: this.headers })
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

  addPrivilege(privilege): Observable<any> {
    return this.http
      .put(this.user + '/privilege', privilege, { headers: this.headers })
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

  deleteUser(email): Observable<any> {
    return this.http
      .delete(this.user + '/' + email, { headers: this.headers })
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
}
