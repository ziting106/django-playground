import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="home-container">
      <h2>歡迎使用 Django + Angular 前後端分離專案</h2>
      <p>這是一個使用 Django REST Framework 作為後端 API，Angular 作為前端的範例專案。</p>
      <div class="features">
        <h3>功能特色：</h3>
        <ul>
          <li>✅ Django REST Framework API</li>
          <li>✅ Angular 20 前端框架</li>
          <li>✅ CORS 跨域支援</li>
          <li>✅ 文章 CRUD 操作</li>
        </ul>
      </div>
      <div class="links">
        <a routerLink="/articles" class="btn">查看文章列表</a>
      </div>
    </div>
  `,
  styles: [
    `
      .home-container {
        text-align: center;
        padding: 40px 20px;
      }
      h2 {
        color: #333;
        margin-bottom: 20px;
      }
      .features {
        text-align: left;
        max-width: 600px;
        margin: 30px auto;
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 8px;
      }
      .features ul {
        list-style: none;
        padding: 0;
      }
      .features li {
        padding: 8px 0;
        font-size: 16px;
      }
      .links {
        margin-top: 30px;
      }
      .btn {
        display: inline-block;
        padding: 12px 24px;
        background-color: #007bff;
        color: white;
        text-decoration: none;
        border-radius: 4px;
        transition: background-color 0.3s;
      }
      .btn:hover {
        background-color: #0056b3;
      }
    `,
  ],
})
export class HomeComponent {}
