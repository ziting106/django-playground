import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { ArticleService } from '../../services/article.service';
import { Article } from '../../models/article.model';

@Component({
  selector: 'app-article-detail',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="article-detail-container">
      <div *ngIf="loading" class="loading">載入中...</div>
      <div *ngIf="error" class="error">{{ error }}</div>
      <div *ngIf="!loading && !error && article" class="article-detail">
        <button routerLink="/articles" class="back-btn">← 返回列表</button>
        <article>
          <h1>{{ article.title }}</h1>
          <div class="meta">
            <span *ngIf="article.author">
              <strong>作者：</strong>{{ article.author.name }}
            </span>
            <span>
              <strong>發布時間：</strong>{{ article.created_at | date: 'yyyy-MM-dd HH:mm' }}
            </span>
            <span>
              <strong>更新時間：</strong>{{ article.updated_at | date: 'yyyy-MM-dd HH:mm' }}
            </span>
            <span [class.published]="article.is_published" [class.draft]="!article.is_published">
              {{ article.is_published ? '已發布' : '草稿' }}
            </span>
          </div>
          <div *ngIf="article.tags.length > 0" class="tags">
            <span *ngFor="let tag of article.tags" class="tag">{{ tag.name }}</span>
          </div>
          <div class="content" [innerHTML]="formatContent(article.content)"></div>
        </article>
      </div>
    </div>
  `,
  styles: [
    `
      .article-detail-container {
        padding: 20px;
        max-width: 800px;
        margin: 0 auto;
      }
      .loading,
      .error {
        text-align: center;
        padding: 40px;
        color: #666;
      }
      .error {
        color: #dc3545;
      }
      .back-btn {
        margin-bottom: 20px;
        padding: 8px 16px;
        background: #6c757d;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
      }
      .back-btn:hover {
        background: #5a6268;
      }
      .article-detail {
        background: white;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }
      .article-detail h1 {
        color: #333;
        margin-bottom: 20px;
      }
      .meta {
        display: flex;
        gap: 20px;
        flex-wrap: wrap;
        margin-bottom: 20px;
        padding-bottom: 20px;
        border-bottom: 1px solid #eee;
        font-size: 14px;
        color: #666;
      }
      .meta strong {
        color: #333;
      }
      .meta .published {
        color: #28a745;
        font-weight: bold;
      }
      .meta .draft {
        color: #ffc107;
        font-weight: bold;
      }
      .tags {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-bottom: 30px;
      }
      .tag {
        background: #e9ecef;
        padding: 6px 12px;
        border-radius: 4px;
        font-size: 14px;
        color: #495057;
      }
      .content {
        line-height: 1.8;
        color: #333;
        white-space: pre-wrap;
      }
    `,
  ],
})
export class ArticleDetailComponent implements OnInit {
  article: Article | null = null;
  loading = false;
  error: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private articleService: ArticleService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loadArticle(+id);
    }
  }

  loadArticle(id: number): void {
    this.loading = true;
    this.error = null;
    this.articleService.getArticle(id).subscribe({
      next: (data) => {
        this.article = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = '載入文章失敗：' + (err.message || '未知錯誤');
        this.loading = false;
        console.error(err);
      },
    });
  }

  formatContent(content: string): string {
    // 簡單的內容格式化，將換行轉換為 <br>
    return content.replace(/\n/g, '<br>');
  }
}

