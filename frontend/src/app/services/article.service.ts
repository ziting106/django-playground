import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { Article } from '../models/article.model';

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

@Injectable({
  providedIn: 'root',
})
export class ArticleService {
  private apiUrl = `${environment.apiUrl}/blog`;

  constructor(private http: HttpClient) {}

  getArticles(published?: boolean): Observable<Article[]> {
    let params = new HttpParams();
    if (published !== undefined) {
      params = params.set('published', published.toString());
    }
    return this.http
      .get<PaginatedResponse<Article>>(`${this.apiUrl}/articles/`, { params })
      .pipe(map((response) => response.results));
  }

  getArticle(id: number): Observable<Article> {
    return this.http.get<Article>(`${this.apiUrl}/articles/${id}/`);
  }

  createArticle(article: Partial<Article>): Observable<Article> {
    return this.http.post<Article>(`${this.apiUrl}/articles/`, article);
  }

  updateArticle(id: number, article: Partial<Article>): Observable<Article> {
    return this.http.put<Article>(`${this.apiUrl}/articles/${id}/`, article);
  }

  deleteArticle(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/articles/${id}/`);
  }

  getPublishedArticles(): Observable<Article[]> {
    return this.http
      .get<PaginatedResponse<Article>>(`${this.apiUrl}/articles/published/`)
      .pipe(map((response) => response.results));
  }
}
