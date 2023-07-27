import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { HttpService } from './http.service';
import { Strings } from '../invariables/strings';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  constructor(private httpService: HttpService) {}
  private categoryObs$: BehaviorSubject<any> = new BehaviorSubject(undefined);
  private cartQuantityObs$: BehaviorSubject<any> = new BehaviorSubject([]);
  baseUrl: string = '';
  initialize(): void {
    this.initializeServerUri();
  }

  private initializeServerUri(): void {
    this.baseUrl = environment.baseUrl + '/api/v1';
  }

  getUsers(): Observable<any> {
    return this.httpService.get(this.baseUrl + Strings.API_ENDPOINT_GET_USERS);
  }

  getPublicKey(receiverId: number): Observable<any> {
    return this.httpService.get(
      this.baseUrl + Strings.API_ENDPOINT_GET_PUBLIC_KEY + receiverId
    );
  }
  sendMessage(body: any): Observable<any> {
    return this.httpService.post(
      this.baseUrl + Strings.API_ENDPOINT_SEND_MESSAGE,
      body
    );
  }
  send(body: any): Observable<any> {
    return this.httpService.post(
      this.baseUrl + Strings.API_ENDPOINT_SEND,
      body
    );
  }
  getUserMessages(): Observable<any> {
    return this.httpService.get(
      this.baseUrl + Strings.API_ENDPOINT_GET_USER_MESSAGES
    );
  }
  getMessages(): Observable<any> {
    return this.httpService.get(
      this.baseUrl + Strings.API_ENDPOINT_GET_MESSAGES
    );
  }

  getCategoriesWithPdtCount(): Observable<any> {
    return this.httpService.get(
      this.baseUrl + Strings.API_ENDPOINT_GET_CATEGORIES_WITH_PRODUCT_COUNT
    );
  }

  deleteCategory(id: number): Observable<any> {
    return this.httpService.delete(
      this.baseUrl + Strings.API_ENDPOINT_DELETE_CATEGORY + id
    );
  }
  saveProduct(body: any): Observable<any> {
    return this.httpService.post(
      this.baseUrl + Strings.API_ENDPOINT_SAVE_PRODUCTS,
      body
    );
  }
  getProducts(id: number = 0): Observable<any> {
    return this.httpService.get(
      this.baseUrl + Strings.API_ENDPOINT_GET_PRODUCTS + id
    );
  }
  getProductById(id: number = 0): Observable<any> {
    return this.httpService.get(
      this.baseUrl + Strings.API_ENDPOINT_GET_PRODUCT_BY_ID + id
    );
  }
  updateProduct(body: any, id: number): Observable<any> {
    return this.httpService.put(
      this.baseUrl + Strings.API_ENDPOINT_UPDATE_PRODUCTS + id,
      body
    );
  }
  deleteProduct(id: number): Observable<any> {
    return this.httpService.delete(
      this.baseUrl + Strings.API_ENDPOINT_DELETE_PRODUCT + id
    );
  }

  cancelOrder(orderId: number): Observable<any> {
    return this.httpService.put(
      this.baseUrl + Strings.API_ENDPOINT_CANCEL_ORDER,
      { id: orderId }
    );
  }

  addFavourites(body: any): Observable<any> {
    return this.httpService.post(
      this.baseUrl + Strings.API_ENDPOINT_FAVOURITE_PRODUCT,
      body
    );
  }
}
