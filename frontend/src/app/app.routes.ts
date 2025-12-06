import { Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { ArticleListComponent } from './components/article-list/article-list.component';
import { ArticleDetailComponent } from './components/article-detail/article-detail.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'articles', component: ArticleListComponent },
  { path: 'articles/:id', component: ArticleDetailComponent },
  { path: '**', redirectTo: '' },
];
