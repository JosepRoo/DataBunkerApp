import { Injectable } from '@angular/core';
import { Router, NavigationStart } from '@angular/router';
import { Observable } from 'rxjs';
import { Subject } from 'rxjs/Subject';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { of } from 'rxjs/observable/of';
import { catchError, map, tap } from 'rxjs/operators';
import { HttpHeaders } from '@angular/common/http';
import * as shajs from 'sha.js';
import 'rxjs/add/operator/catch';

// import models
import { User } from "../classes/user";

// import services
import { CompanyService } from "../services/company.service";
import { MessageService } from "../services/messages.service";

@Injectable()
export class UserService {

  private userUrl: string = environment.url+'userstatus';
  private headers = new HttpHeaders({ 'Content-Type': 'application/json'});

  constructor(private companyService: CompanyService, private http: HttpClient, private msgService: MessageService) {
    // this.user.company = companyService.getCompany();
  }

  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      console.log(`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

  getUser(id: string): Observable<User> {
    return this.http.get<User>(this.userUrl+'get_user/'+id).pipe(
      tap(_ => this.checkError(_)),
      catchError(this.handleError<User>(`getUser id=${id}`))
    );
  }

  logIn(data): Observable<any> {
    data.password = shajs('sha256').update(data.password).digest('hex');
    return this.http.post(this.userUrl, JSON.stringify(data), {headers: this.headers})
      .map(res => {
            return res;
      })
      .catch(e => {
          if (e.status === 401) {
              return Observable.throw('Unauthorized');
          }
          // do any other checking for statuses here
      });
  }

  checkError(res) {
    if(res.msg_response){
      this.msgService.warn("User Service: "+res.msg_response)
    }
  }
}
