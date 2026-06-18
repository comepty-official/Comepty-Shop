# Google OAuth Setup Guide for Comepty

## Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- `django-allauth` - Social authentication framework
- `google-auth-oauthlib` - Google OAuth library
- `google-auth` - Google authentication library

## Step 2: Create Google OAuth Credentials

### 2.1 Go to Google Cloud Console
1. Visit https://console.cloud.google.com/
2. Create a new project or select existing one
3. Name it "Comepty" (or your preference)

### 2.2 Enable Google+ API
1. Go to **APIs & Services** → **Library**
2. Search for "Google+ API"
3. Click **Enable**

### 2.3 Create OAuth 2.0 Credentials
1. Go to **APIs & Services** → **Credentials**
2. Click **+ Create Credentials** → **OAuth client ID**
3. If prompted, configure the OAuth consent screen first:
   - Click **Configure Consent Screen**
   - Choose **External** user type
   - Fill in required info (app name, email, etc.)
   - Add scopes: `email`, `profile`
   - Add yourself as a test user
   - Save & Continue

4. Back to Create Credentials:
   - Select **Web application**
   - Add authorized origins:
     - `http://localhost:8000`
     - `http://127.0.0.1:8000`
     - Your production domain (e.g., `https://yourdomain.com`)
   - Add authorized redirect URIs:
     - `http://localhost:8000/accounts/google/login/callback/`
     - `http://127.0.0.1:8000/accounts/google/login/callback/`
     - `https://yourdomain.com/accounts/google/login/callback/`
   - Click **Create**

### 2.4 Copy Your Credentials
You'll see a dialog with:
- **Client ID**
- **Client Secret**

Save these — you need them next.

## Step 3: Configure Django

### 3.1 Create `.env` file in project root:
```bash
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
```

### 3.2 Update settings (already done in comepty/settings.py)
The settings now read from environment variables:
```python
'APP': {
    'client_id': os.environ.get('GOOGLE_CLIENT_ID', ''),
    'secret': os.environ.get('GOOGLE_CLIENT_SECRET', ''),
}
```

### 3.3 Install python-decouple (already in requirements.txt)
This allows reading from .env:
```bash
pip install python-decouple
```

Update `comepty/settings.py` imports (optional, if not already there):
```python
from decouple import config
```

Then update the Google settings to use:
```python
'APP': {
    'client_id': config('GOOGLE_CLIENT_ID', default=''),
    'secret': config('GOOGLE_CLIENT_SECRET', default=''),
}
```

## Step 4: Run Migrations
```bash
python manage.py migrate
```

This creates the necessary tables for django-allauth.

## Step 5: Create Django Admin Site Record (optional but recommended)
```bash
python manage.py shell
```

Then in the shell:
```python
from django.contrib.sites.models import Site
Site.objects.get_or_create(id=1, defaults={'domain': 'localhost:8000', 'name': 'Comepty'})
exit()
```

## Step 6: Test Locally
```bash
python manage.py runserver
```

1. Go to `http://localhost:8000/users/login/`
2. Click **"Continue with Google"** button
3. You'll be redirected to Google login
4. After signing in, you'll be auto-logged into Comepty

## Production Deployment

For production (e.g., Heroku, Railway, PythonAnywhere):

1. Set environment variables:
   ```
   GOOGLE_CLIENT_ID=your_production_client_id
   GOOGLE_CLIENT_SECRET=your_production_client_secret
   ```

2. Update Django Site in admin:
   - Go to Django admin
   - Sites → Change domain to your production domain
   - Update authorized URIs in Google Cloud Console

3. Add your production domain to `ALLOWED_HOSTS` in settings.py

## Features Enabled

✅ **Google Login** - Users can sign in with Google account
✅ **Auto-signup** - New Google users automatically get accounts created
✅ **Email Auto-fill** - Email verified through Google
✅ **Session Persistence** - Browser remembers user login
✅ **Browser Detection** - Auto-login on subsequent visits

## Troubleshooting

### "Invalid Client ID" error
- Check your `GOOGLE_CLIENT_ID` environment variable is set correctly
- Ensure Client ID is from Google Cloud Console OAuth credentials

### Redirect URI mismatch
- Go to Google Cloud Console → Credentials
- Edit your OAuth app
- Ensure redirect URIs match exactly (including http/https and trailing slash)

### Sessions not persisting
- Check `SITE_ID = 1` in settings
- Ensure `django.contrib.sites` is in `INSTALLED_APPS`

### "provider_login_url 'google'" error
- Ensure allauth templates are loaded
- Check `{% load socialaccount %}` is in your template (it should be via extends)

## Files Changed

1. **requirements.txt** - Added allauth packages
2. **comepty/settings.py** - Added allauth configuration
3. **comepty/urls.py** - Added allauth URLs
4. **templates/users/login.html** - Added Google login button
5. **templates/users/register.html** - Added Google signup button
