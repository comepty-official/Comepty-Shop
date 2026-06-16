# 🛒 Comepty — Buy Your Way
> Affiliate marketing + product promotion platform. Pinterest × Product Hunt × TikTok.

---

## ⚡ Quick Start (5 minutes)

### 1. Prerequisites
- **Python 3.12+** (check: `python --version`)
- **pip** (comes with Python)

---

### 2. Create Virtual Environment

```bash
# Create the project folder and enter it
mkdir comepty-project && cd comepty-project

# Copy all project files here, then:

# Create virtual environment
python -m venv venv

# Activate it
# macOS / Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed:**
| Package | Purpose |
|---|---|
| `Django==5.0.6` | Web framework |
| `Pillow==10.3.0` | Image upload handling |
| `django-crispy-forms==2.1` | Beautiful form rendering |
| `crispy-bootstrap5` | Bootstrap 5 form theme |
| `whitenoise==6.7.0` | Static file serving |
| `python-decouple==3.8` | Environment variables |
| `django-taggit==5.0.1` | Product tags system |

---

### 4. Database Setup

```bash
# Run migrations (creates SQLite database)
python manage.py migrate

# Seed the database with categories
python manage.py seed_data

# Create your admin account
python manage.py createsuperuser
# → Enter username, email, password when prompted
```

---

### 5. Run the Server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser. 🎉

---

## 📁 Project Structure

```
comepty/
│
├── comepty/                  ← Django config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/                     ← Homepage + search
│   ├── views.py
│   ├── urls.py
│   ├── context_processors.py
│   └── management/
│       └── commands/
│           └── seed_data.py  ← Run this first!
│
├── products/                 ← Main app
│   ├── models.py             ← Product, Category, Like, etc.
│   ├── views.py              ← All product views
│   ├── forms.py              ← Product + image forms
│   ├── urls.py
│   └── admin.py              ← Admin with approve/reject actions
│
├── users/                    ← Auth + profiles
│   ├── models.py             ← Profile model
│   ├── views.py
│   ├── forms.py
│   └── urls.py
│
├── templates/
│   ├── base.html             ← Master layout (navbar, sidebar, footer)
│   ├── core/
│   │   ├── home.html         ← Homepage with hero + grids
│   │   └── search.html       ← Search results
│   ├── products/
│   │   ├── list.html         ← Browse grid with filters
│   │   ├── detail.html       ← Product page (gallery, video, comments)
│   │   ├── create.html       ← Post/edit product form
│   │   ├── feed.html         ← TikTok-style video feed
│   │   ├── my_products.html  ← Dashboard
│   │   └── saved.html        ← Saved items
│   ├── users/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   └── edit_profile.html
│   └── partials/
│       └── product_card.html ← Reusable card component
│
├── static/
│   ├── css/
│   │   └── main.css          ← Full design system (1300+ lines)
│   └── js/
│       └── main.js           ← Dark mode, AJAX likes, gallery, animations
│
├── media/                    ← User uploads (images, videos)
├── manage.py
└── requirements.txt
```

---

## 🌐 URL Map

| URL | Page |
|---|---|
| `/` | Homepage — hero, trending, newest |
| `/products/` | Browse all products |
| `/products/feed/` | TikTok-style video feed |
| `/products/create/` | Post a new product |
| `/products/<slug>/` | Product detail page |
| `/products/<slug>/edit/` | Edit your product |
| `/products/<slug>/click/` | Affiliate redirect (tracked) |
| `/products/category/<slug>/` | Category filter |
| `/products/my-products/` | Your product dashboard |
| `/products/saved/` | Saved products |
| `/users/register/` | Sign up |
| `/users/login/` | Sign in |
| `/users/profile/<username>/` | Public profile |
| `/admin/` | Admin panel |

---

## 🗄️ Database Models

### Product
```
title, slug, description, price, affiliate_link
category → Category
creator → User
tags (django-taggit)
status: pending / approved / rejected / draft
youtube_url, video_file, thumbnail
view_count, click_count, like_count
```

### ProductImage
```
product → Product (ForeignKey, multiple images per product)
image, caption, order
```

### Category
```
name, slug, icon, color, description
```

### Profile
```
user → User (OneToOne)
bio, avatar, website, twitter, instagram, is_verified
```

### Like / SavedProduct / Comment / AffiliateClick
```
Engagement + affiliate tracking models
```

---

## 🎨 Design System

| Token | Value |
|---|---|
| Primary | `#7C3AED` (violet) |
| Secondary | `#EC4899` (pink) |
| Accent | `#F59E0B` (amber) |
| Gradient | `135deg, #7C3AED → #EC4899` |
| Font | Inter (Google Fonts) |
| Dark bg | `#0D0D1A` |
| Light bg | `#F8F7FF` |

**Dark mode** is toggled by the switch in the navbar and saved to `localStorage`.

---

## ✅ Admin Workflow

1. User submits a product → status = `pending`
2. Go to `/admin/products/product/`
3. Select products → Action: **✅ Approve selected products**
4. Products go live instantly

---

## 🚀 Deployment (Render.com)

```bash
# 1. Create a Render Web Service
# 2. Set environment variables:
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com

# 3. Build command:
pip install -r requirements.txt && python manage.py migrate && python manage.py seed_data && python manage.py collectstatic --noinput

# 4. Start command:
gunicorn comepty.wsgi:application

# 5. Add gunicorn to requirements:
pip install gunicorn
```

---

## 🔧 Common Commands

```bash
# Start dev server
python manage.py runserver

# Create new migration after model changes
python manage.py makemigrations
python manage.py migrate

# Seed categories
python manage.py seed_data

# Create admin user
python manage.py createsuperuser

# Collect static files (production)
python manage.py collectstatic

# Django shell
python manage.py shell
```

---

## 💡 Features Summary

- ✅ **Multi-image upload** per product (up to 10)
- ✅ **YouTube/Vimeo embed** + video file upload
- ✅ **Affiliate click tracking** with IP + user agent logging
- ✅ **TikTok-style video feed**
- ✅ **Dark / Light mode** with localStorage persistence
- ✅ **AJAX likes & saves** (no page reload)
- ✅ **Admin approval system** before products go live
- ✅ **Category sidebar** with product counts
- ✅ **Search** across title, description, creator, category
- ✅ **Image gallery** with thumbnail switcher
- ✅ **Responsive** — mobile first design
- ✅ **Animations** — fade-in cards, hover effects, scroll reveal
- ✅ **SEO-friendly slugs** on all URLs
- ✅ **User profiles** with avatar, bio, social links
- ✅ **Comment system** on products
- ✅ **Tag system** (django-taggit)
- ✅ **Pagination** on all list views
