#!/usr/bin/env python
"""
簡單的 SQLite 資料庫查看工具
使用方式: python view_db.py
"""
import sqlite3
import sys
from pathlib import Path

# 資料庫路徑
DB_PATH = Path(__file__).parent / "db.sqlite3"

def print_table(conn, table_name):
    """顯示表格內容"""
    cursor = conn.cursor()
    
    # 獲取表格結構
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    if not columns:
        print(f"表格 {table_name} 不存在或為空")
        return
    
    # 獲取欄位名稱
    column_names = [col[1] for col in columns]
    
    # 獲取資料
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    if not rows:
        print(f"\n表格 {table_name} 是空的")
        return
    
    # 計算欄位寬度
    widths = [len(name) for name in column_names]
    for row in rows:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len(str(value) or ""))
    
    # 打印表頭
    header = " | ".join(name.ljust(widths[i]) for i, name in enumerate(column_names))
    print(f"\n{'=' * len(header)}")
    print(f"表格: {table_name}")
    print(f"{'=' * len(header)}")
    print(header)
    print("-" * len(header))
    
    # 打印資料
    for row in rows:
        row_str = " | ".join(str(value or "").ljust(widths[i]) for i, value in enumerate(row))
        print(row_str)
    
    print(f"\n共 {len(rows)} 筆記錄")

def main():
    if not DB_PATH.exists():
        print(f"錯誤: 找不到資料庫檔案 {DB_PATH}")
        sys.exit(1)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 獲取所有表格
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        
        if not tables:
            print("資料庫中沒有表格")
            return
        
        print("=" * 60)
        print("SQLite 資料庫內容查看器")
        print("=" * 60)
        print(f"\n資料庫路徑: {DB_PATH}")
        print(f"\n找到 {len(tables)} 個表格:")
        for i, table in enumerate(tables, 1):
            print(f"  {i}. {table}")
        
        # 顯示 blog 相關的表格
        blog_tables = [t for t in tables if t.startswith("blog_")]
        if blog_tables:
            print("\n" + "=" * 60)
            print("Blog 相關表格:")
            print("=" * 60)
            for table in blog_tables:
                print_table(conn, table)
        
        # 詢問是否要查看其他表格
        print("\n" + "=" * 60)
        print("其他表格:")
        print("=" * 60)
        other_tables = [t for t in tables if not t.startswith("blog_")]
        for table in other_tables[:5]:  # 只顯示前 5 個
            print_table(conn, table)
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"資料庫錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


