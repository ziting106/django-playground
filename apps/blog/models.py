from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    author = models.ForeignKey(
        Author,
        # If an author is deleted, set the author field to null
        # CASCADE = 作者被刪掉文章也刪掉
        # PROTECT = 作者如果還有文章就不讓刪
        on_delete=models.CASCADE,
        related_name="articles",
        null=True,
        blank=True,
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="articles",
        blank=True,
    )

    def __str__(self):
        return self.title
