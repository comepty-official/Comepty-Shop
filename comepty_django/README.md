# Comepty 🚀

The marketplace for creators, affiliates, and entrepreneurs.

## Quick Start

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Run migrations
```bash
python manage.py migrate
```

### 3. Seed sample data (optional but recommended)
```bash
python manage.py seed_data
# Creates: admin/admin123 and demo/demo1234
```

### 4. Create your own superuser
```bash
python manage.py createsuperuser
```

### 5. Run the development server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## Features

- 🛒 Product listings with multiple images & videos
- 🎬 TikTok-style vertical video feed
- 🤖 Comepty AI 1.0 — trending & marketing assistant
- 💬 User-to-user chat with message history
- ❤️ Like, save, and comment on products
- 📊 Affiliate click tracking & analytics
- 🛡️ Admin approval system for products
- 🚩 Report system for products & content
- 📝 Admin blog posts
- 🌙 Dark/light mode toggle
- 📱 Mobile-first responsive design
- 🔒 Soft account deletion (data retained)
- 📄 Terms of Service & Privacy Policy

## Comepty AI 1.0

The AI works in two modes:
1. **Keyword mode** (default) — smart pattern matching for trending topics, marketing, pricing, and growth tips
2. **OpenAI mode** — set your OpenAI API key for full conversational AI

To enable OpenAI:
```bash
export OPENAI_API_KEY=your_key_here
# or add to comepty/settings.py:
# OPENAI_API_KEY = 'your_key_here'
```

## Admin Panel

Go to http://127.0.0.1:8000/admin/ (superusers only)

Admin capabilities:
- Approve / reject products
- Feature products on homepage
- Manage blog posts
- View and resolve reports
- Approve user-submitted videos
- Restore deactivated accounts

## Notes

- Users don't need to log in to browse or click affiliate links
- Soft delete: deactivated accounts hide content but retain data
- Email notifications use console backend by default (check terminal output)
