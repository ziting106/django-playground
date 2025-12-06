export interface Author {
  id: number;
  name: string;
  email: string;
  bio: string;
  created_at: string;
}

export interface Tag {
  id: number;
  name: string;
}

export interface Article {
  id: number;
  title: string;
  content: string;
  created_at: string;
  updated_at: string;
  is_published: boolean;
  author: Author | null;
  author_id?: number;
  tags: Tag[];
  tag_ids?: number[];
}
