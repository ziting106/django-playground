import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ArticleService } from '../../services/article.service';
import { Article } from '../../models/article.model';

@Component({
  selector: 'app-article-list',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="article-list-container">
      <h2>文章列表</h2>
      <div class="filter-buttons">
        <button (click)="loadArticles()" [class.active]="!showPublishedOnly">
          全部文章
        </button>
        <button (click)="loadPublishedArticles()" [class.active]="showPublishedOnly">
          已發布
        </button>
      </div>
      <div *ngIf="loading" class="loading">載入中...</div>
      <div *ngIf="error" class="error">{{ error }}</div>
      <div *ngIf="!loading && !error" class="articles-grid">
        <div *ngFor="let article of articles" class="article-card">
          <h3>
            <a [routerLink]="['/articles', article.id]">{{ article.title }}</a>
          </h3>
          <p class="meta">
            <span *ngIf="article.author">作者：{{ article.author.name }}</span>
            <span>發布時間：{{ article.created_at | date: 'yyyy-MM-dd HH:mm' }}</span>
            <span [class.published]="article.is_published" [class.draft]="!article.is_published">
              {{ article.is_published ? '已發布' : '草稿' }}
            </span>
          </p>
          <p class="content-preview">{{ article.content | slice: 0:150 }}...</p>
          <div *ngIf="article.tags.length > 0" class="tags">
            <span *ngFor="let tag of article.tags" class="tag">{{ tag.name }}</span>
          </div>
        </div>
      </div>
      <div *ngIf="!loading && articles.length === 0" class="empty">
        目前沒有文章
      </div>
    </div>
  `,
  styles: [
    `
      .article-list-container {
        padding: 20px;
      }
      h2 {
        color: #333;
        margin-bottom: 20px;
      }
      .filter-buttons {
        margin-bottom: 20px;
        display: flex;
        gap: 10px;
      }
      .filter-buttons button {
        padding: 8px 16px;
        border: 1px solid #ddd;
        background: white;
        cursor: pointer;
        border-radius: 4px;
        transition: all 0.3s;
      }
      .filter-buttons button:hover {
        background: #f0f0f0;
      }
      .filter-buttons button.active {
        background: #007bff;
        color: white;
        border-color: #007bff;
      }
      .loading,
      .error,
      .empty {
        text-align: center;
        padding: 40px;
        color: #666;
      }
      .error {
        color: #dc3545;
      }
      .articles-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
      }
      .article-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 20px;
        background: white;
        transition: box-shadow 0.3s;
      }
      .article-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      }
      .article-card h3 {
        margin-top: 0;
        margin-bottom: 10px;
      }
      .article-card h3 a {
        color: #333;
        text-decoration: none;
      }
      .article-card h3 a:hover {
        color: #007bff;
      }
      .meta {
        font-size: 12px;
        color: #666;
        margin-bottom: 10px;
        display: flex;
        gap: 15px;
        flex-wrap: wrap;
      }
      .meta .published {
        color: #28a745;
        font-weight: bold;
      }
      .meta .draft {
        color: #ffc107;
        font-weight: bold;
      }
      .content-preview {
        color: #555;
        line-height: 1.6;
        margin-bottom: 10px;
      }
      .tags {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-top: 10px;
      }
      .tag {
        background: #e9ecef;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        color: #495057;
      }
    `,
  ],
})
export class ArticleListComponent implements OnInit {
  articles: Article[] = [];
  loading = false;
  error: string | null = null;
  showPublishedOnly = false;

  constructor(private articleService: ArticleService) {}

  ngOnInit(): void {
    this.loadArticles();
  }

  loadArticles(): void {
    this.showPublishedOnly = false;
    this.loading = true;
    this.error = null;
    this.articleService.getArticles().subscribe({
      next: (data) => {
        this.articles = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = '載入文章失敗：' + (err.message || '未知錯誤');
        this.loading = false;
        console.error(err);
      },
    });
  }

  loadPublishedArticles(): void {
    this.showPublishedOnly = true;
    this.loading = true;
    this.error = null;
    this.articleService.getPublishedArticles().subscribe({
      next: (data) => {
        this.articles = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = '載入已發布文章失敗：' + (err.message || '未知錯誤');
        this.loading = false;
        console.error(err);
      },
    });
  }
}
