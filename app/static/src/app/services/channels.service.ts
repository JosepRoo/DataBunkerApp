import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';
import { Channel } from '../classes/channel';
import { Product } from '../classes/product';
import { Category } from '../classes/category';
import { Brand } from '../classes/brand';
import { catchError, map, tap } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import 'rxjs/add/operator/catch';

// services
import { MessageService } from "../services/messages.service";

@Injectable()
export class ChannelService {


  private channelUrl = environment.url+'elements/channel';
  private subElementsUrl = environment.url+'subelements/';
  private dataUrl = environment.url+'elementvalue/';
  private headers = new HttpHeaders({ 'Content-Type': 'application/json'});

  constructor(private http: HttpClient, private msgService: MessageService) {
    // this.user.company = companyService.getCompany();
  }

  getChannels(): Observable<Channel[]> {
    return this.http.get<Channel>(this.channelUrl,  {headers: this.headers})
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

  getChannelSubElemenets(channelId): Observable<Category[]> {
    return this.http.get<Channel>(this.subElementsUrl+"channel/"+channelId,  {headers: this.headers})
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

  getCategorySubElemenets(categoryId): Observable<Brand[]> {
    return this.http.get<Channel>(this.subElementsUrl+"category/"+categoryId,  {headers: this.headers})
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

  getBrandSubElemenets(brandId): Observable<Product[]> {
    return this.http.get<Product>(this.subElementsUrl+"brand/"+brandId,  {headers: this.headers})
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

  getData(type, id, startDate, endDate){
    startDate = startDate.getYear()+1900 + '-' + ("0" + (startDate.getMonth() + 1)).slice(-2) + '-' +("0" + (startDate.getDate())).slice(-2);
    endDate = endDate.getYear()+1900 + '-' + ("0" + (endDate.getMonth() + 1)).slice(-2) + '-' +("0" + (endDate.getDate())).slice(-2);
    return this.http.get<any>(this.dataUrl+type+'/'+id+'/'+startDate+'/'+endDate,  {headers: this.headers})
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



}
