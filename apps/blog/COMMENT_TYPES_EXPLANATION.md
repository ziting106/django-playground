# Python 註解類型說明

## 兩種註解類型的差異

### 1. Docstring（三引號註解）```148-159 行```

**特點：**
- 使用三個引號 `"""` 或 `'''` 包圍
- 放在函數/類別定義的**第一行**（緊接在 `def` 或 `class` 之後）
- 是 Python 的**正式文檔字串**（Documentation String）
- 可以被 Python 的內建工具讀取（如 `help()` 函數）
- 可以被 IDE 和文檔生成工具（如 Sphinx）自動提取

**用途：**
- 說明函數/類別的**整體功能**
- 描述**參數**和**返回值**
- 提供**使用範例**
- 適合寫給**使用這個函數的人**看

**範例：**
```python
def has_published_articles(self, obj):
    """
    自訂顯示欄位：檢查作者是否有已發布的文章
    
    參數：
    - obj：當前的 Author 物件
    
    返回：True 或 False
    """
    # 實際程式碼...
```

**如何查看：**
```python
# 在 Python shell 中
help(has_published_articles)
# 或
has_published_articles.__doc__
```

---

### 2. Inline Comment（井號註解）```160-162 行```

**特點：**
- 使用井號 `#` 開頭
- 可以放在**程式碼的任何位置**
- 是**普通的註解**，不會被 Python 特別處理
- 主要用於**解釋程式碼邏輯**

**用途：**
- 解釋**單行程式碼**的作用
- 說明**複雜邏輯**的步驟
- 提醒**注意事項**
- 適合寫給**閱讀程式碼的人**看

**範例：**
```python
# obj.articles：取得作者的所有文章（透過 ForeignKey 的 related_name）
# .filter(is_published=True)：篩選已發布的文章
# .exists()：檢查是否存在（比 .count() > 0 更有效率）
return obj.articles.filter(is_published=True).exists()
```

---

## 實際應用場景

### 何時使用 Docstring？
✅ 函數/類別的整體說明
✅ 參數和返回值的詳細描述
✅ 使用範例和注意事項
✅ 需要被文檔工具提取的說明

### 何時使用 Inline Comment？
✅ 解釋複雜的單行程式碼
✅ 說明演算法步驟
✅ 提醒特殊情況或注意事項
✅ 解釋為什麼這樣寫（而不是怎麼寫）

---

## 最佳實踐

### 好的寫法：
```python
def calculate_total(items):
    """
    計算購物車總金額
    
    參數：
    - items：商品列表，每個商品包含 price 和 quantity
    
    返回：總金額（浮點數）
    
    範例：
    >>> items = [{"price": 100, "quantity": 2}]
    >>> calculate_total(items)
    200.0
    """
    total = 0
    # 遍歷每個商品，計算小計並累加
    for item in items:
        # 小計 = 單價 × 數量
        subtotal = item["price"] * item["quantity"]
        total += subtotal
    return total
```

### 不好的寫法：
```python
def calculate_total(items):
    # 這個函數用來計算總金額
    # items 是商品列表
    # 返回總金額
    total = 0
    for item in items:
        subtotal = item["price"] * item["quantity"]
        total += subtotal
    return total
```

---

## 在你的程式碼中

### Docstring（148-159 行）
```python
def has_published_articles(self, obj):
    """
    自訂顯示欄位：檢查作者是否有已發布的文章
    
    參數：
    - obj：當前的 Author 物件
    
    返回：True 或 False
    """
```
**說明：** 這是函數的**正式文檔**，說明函數的用途、參數和返回值。

### Inline Comment（160-162 行）
```python
# obj.articles：取得作者的所有文章（透過 ForeignKey 的 related_name）
# .filter(is_published=True)：篩選已發布的文章
# .exists()：檢查是否存在（比 .count() > 0 更有效率）
return obj.articles.filter(is_published=True).exists()
```
**說明：** 這是**程式碼行內註解**，解釋這行程式碼的每個部分在做什麼。

---

## 總結

| 特性 | Docstring | Inline Comment |
|------|-----------|---------------|
| **語法** | `"""` 或 `'''` | `#` |
| **位置** | 函數/類別定義內第一行 | 程式碼任何位置 |
| **用途** | 函數整體說明 | 單行程式碼解釋 |
| **讀者** | 使用函數的人 | 閱讀程式碼的人 |
| **工具支援** | 可被 `help()` 讀取 | 純文字註解 |
| **長度** | 通常較長、較詳細 | 通常較短、較精簡 |

兩種註解**互補**，不是替代關係：
- **Docstring** 告訴你「這個函數做什麼」
- **Inline Comment** 告訴你「這行程式碼怎麼做」

