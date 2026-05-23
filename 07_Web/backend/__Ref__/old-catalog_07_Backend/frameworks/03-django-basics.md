# 🐍 Django — Python Web Framework "Batteries Included"

> `[INTERMEDIATE]` — Full-stack framework mạnh nhất cho Python

---

## Tại sao Django?

Mỗi framework có **philosophy** khác nhau:

| | Django | FastAPI | Flask |
|---|---|---|---|
| **Philosophy** | "Batteries included" | "Modern, async, fast" | "Micro, DIY" |
| **Cung cấp** | ORM, Admin, Auth, Forms, Templates, Security... | API only, type hints | Routing + templates (tự thêm mọi thứ) |
| **Best for** | Full-stack apps, admin panels, CMS | APIs, microservices | Small apps, prototypes |
| **Learning** | Cao (nhiều concepts) | Trung bình | Thấp |

**Chọn Django khi:**
- Cần admin panel (free, powerful — Django Admin)
- Full-stack: server-rendered HTML + API
- Cần auth, ORM, migrations built-in
- Team Python, deadline gấp (Django có sẵn mọi thứ)

**Không chọn Django khi:**
- Chỉ cần API → FastAPI (nhanh hơn, type-safe)
- Microservice nhỏ → Flask hoặc FastAPI
- Real-time heavy → Node.js + Socket.io

---

## 1. Setup & Project Structure

```bash
pip install django
django-admin startproject mysite
cd mysite
python manage.py startapp blog
```

```
mysite/
├── manage.py                ← CLI tool (runserver, migrate, etc.)
├── mysite/                  ← Project config
│   ├── settings.py          ← Database, installed apps, middleware
│   ├── urls.py              ← Root URL routing
│   └── wsgi.py              ← WSGI entry (production)
└── blog/                    ← App (1 feature domain)
    ├── models.py            ← Database models (ORM)
    ├── views.py             ← Request handlers
    ├── urls.py              ← App-specific routes
    ├── admin.py             ← Admin panel config
    ├── serializers.py       ← DRF serializers (API)
    ├── tests.py             ← Tests
    └── templates/           ← HTML templates
        └── blog/
            └── post_list.html
```

---

## 2. Models — ORM mạnh nhất Python

Django ORM cho phép định nghĩa database schema bằng Python classes. Tự generate **migrations** (SQL thay đổi schema):

```python
# blog/models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    excerpt = models.CharField(max_length=500, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[('draft', 'Draft'), ('published', 'Published')],
        default='draft',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at', 'status']),
        ]

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
```

```bash
# Tạo migration từ model changes
python manage.py makemigrations
# → blog/migrations/0001_initial.py (SQL generated automatically!)

# Apply migration
python manage.py migrate

# Xem SQL sẽ chạy (debug)
python manage.py sqlmigrate blog 0001
```

### QuerySet — Query database bằng Python

```python
# Không cần viết SQL!
Post.objects.all()                                    # SELECT * FROM post
Post.objects.filter(status='published')               # WHERE status = 'published'
Post.objects.filter(author__username='an')             # JOIN + WHERE (magic!)
Post.objects.filter(created_at__year=2026)             # WHERE EXTRACT(YEAR...)
Post.objects.filter(title__icontains='django')         # WHERE title ILIKE '%django%'
Post.objects.exclude(status='draft')                   # WHERE NOT status = 'draft'
Post.objects.order_by('-created_at')[:10]              # ORDER BY + LIMIT 10

# Aggregation
from django.db.models import Count, Avg
Post.objects.values('author__username').annotate(
    post_count=Count('id'),
).order_by('-post_count')
# → [{'author__username': 'an', 'post_count': 15}, ...]

# Efficient: select_related (JOIN) vs prefetch_related (2 queries)
Post.objects.select_related('author')                  # 1 query with JOIN
Post.objects.prefetch_related('tags')                  # 2 queries, no JOIN
```

---

## 3. Views & URLs

```python
# blog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Post

# Function-based view (đơn giản)
def post_list(request):
    posts = Post.objects.filter(status='published').select_related('author')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    return render(request, 'blog/post_detail.html', {'post': post})

# Class-based view (reusable, DRY)
from django.views.generic import ListView, DetailView

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author')
```

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('<slug:slug>/', views.post_detail, name='post-detail'),
]

# mysite/urls.py
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),        # Admin panel
    path('blog/', include('blog.urls')),     # Blog app
    path('api/', include('api.urls')),       # API app
]
```

---

## 4. Django Admin — Killer feature

```python
# blog/admin.py — 5 dòng code = full admin panel!
from django.contrib import admin
from .models import Post, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
```

```bash
# Tạo superuser
python manage.py createsuperuser
# → http://localhost:8000/admin/ → CRUD cho tất cả models!
```

Django Admin tự động generate CRUD interface cho models. Non-technical team members (content editors, support) có thể quản lý data **không cần code**.

---

## 5. Django REST Framework (DRF) — API

```python
# pip install djangorestframework
# blog/serializers.py
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author_name', 'content', 'status', 'created_at']
        read_only_fields = ['slug', 'created_at']

# blog/api_views.py
from rest_framework import viewsets, permissions
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(status='published').select_related('author')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

---

## Commands thường dùng

```bash
python manage.py runserver              # Dev server
python manage.py makemigrations         # Tạo migration
python manage.py migrate                # Apply migrations
python manage.py createsuperuser        # Tạo admin user
python manage.py shell                  # Python shell với Django context
python manage.py test                   # Chạy tests
python manage.py collectstatic          # Collect static files (production)
python manage.py dbshell                # DB shell trực tiếp
```

---

## Bài tập thực hành

- [ ] Build blog: Models (Post, Tag), Admin, Views, Templates
- [ ] API: Django REST Framework cho CRUD Posts
- [ ] Auth: Login/Register/Logout built-in views
- [ ] Deploy: Gunicorn + Nginx + PostgreSQL

---

## Tài nguyên thêm

- [Django Docs](https://docs.djangoproject.com/) — Official (rất tốt!)
- [Django REST Framework](https://www.django-rest-framework.org/) — API
- [Django Girls Tutorial](https://tutorial.djangogirls.org/) — Beginner-friendly
