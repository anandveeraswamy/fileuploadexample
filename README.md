
# Django File Upload Project

This guide walks you through setting up a Django project for file uploads and image retrieval, with validation for file type and size. Follow these steps to set up and run the project.

---

## **1. Set Up Your Django Project**

```bash
mkdir fileupload
cd fileupload
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install django psycopg2
```

---

## **2. Start a Django Project**

```bash
django-admin startproject file_app .
```

---

## **3. Configure PostgreSQL Permissions**

Run the following commands using `pgAdmin` or `psql`:

```sql
-- Replace 'library_pm6c' with your database name
-- Replace 'library_pm6c_user' with your PostgreSQL username
\c library_pm6c  -- Connect to the database

ALTER ROLE library_pm6c_user SET client_encoding TO 'utf8';
ALTER ROLE library_pm6c_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE library_pm6c_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE library_pm6c TO library_pm6c_user;
```

---

## **4. Set Up PostgreSQL Database in `settings.py`**

Install the `dj-database-url` library:

```bash
pip install dj-database-url
```

Modify your `settings.py`:

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://<username>:<password>@localhost:5432/<dbname>'
    )
}
```

Replace `<username>`, `<password>`, and `<dbname>` with your database credentials or use your Render database URL.

---

## **5. Environment Variable for Deployment**

Store your Render PostgreSQL database URL as an environment variable and configure `settings.py`:

```python
DATABASES = {
    'default': dj_database_url.config(
        default= os.environ['RENDER_DATABASE_URL']
    )
}
```

---

## **6. Create a New Django App**

```bash
python manage.py startapp file_manager
```

---

## **7. Add `file_manager` to `INSTALLED_APPS`**

Update `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'file_manager',
]
```

---

## **8. Define the File Model**

Add the following model to `file_manager/models.py`:

```python
from django.db import models

class File(models.Model):
    name = models.CharField(max_length=255)
    content = models.BinaryField()
    content_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

---

## **9. Apply Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## **10. Create File Upload Form**

Add the following form to `file_manager/forms.py`:

```python
from django import forms
from django.core.exceptions import ValidationError

ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif']
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

class FileUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']

        if uploaded_file.content_type not in ALLOWED_IMAGE_TYPES:
            raise ValidationError('Invalid file type. Only image files are allowed.')

        if uploaded_file.size > MAX_FILE_SIZE:
            raise ValidationError(f'File size exceeds {MAX_FILE_SIZE // (1024 * 1024)} MB.')

        return uploaded_file
```

---

## **11. Create Views**

Add the following views to `file_manager/views.py`:

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import FileUploadForm
from .models import File

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            File.objects.create(
                name=uploaded_file.name,
                content=uploaded_file.read(),
                content_type=uploaded_file.content_type,
            )
            messages.success(request, 'File uploaded successfully!')
            return redirect('upload_file')
    else:
        form = FileUploadForm()

    files = File.objects.all().order_by('-id')[:5]
    return render(request, 'file_manager/upload.html', {'form': form, 'files': files})

def download_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    response = HttpResponse(file.content, content_type=file.content_type)
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    return response

def display_image(request, file_id):
    file = get_object_or_404(File, id=file_id)
    return HttpResponse(file.content, content_type=file.content_type)
```

---

## **12. Create Templates**

### Upload Form Template (`file_manager/templates/file_manager/upload.html`):

```html
<!DOCTYPE html>
<html>
<head>
    <title>Upload Image</title>
</head>
<body>
    {% if messages %}
    <div class="messages">
        {% for message in messages %}
            <div class="alert {% if message.tags %}alert-{{ message.tags }}{% endif %}">
                {{ message }}
            </div>
        {% endfor %}
    </div>
    {% endif %}
    <h1>Upload an Image</h1>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Upload</button>
    </form>

    <h2>Uploaded Images</h2>
    {% for file in files %}
        <div>
            <h3>{{ file.name }}</h3>
            <img src="/file/{{ file.id }}" alt="{{ file.name }}" style="max-width: 200px;">
        </div>
    {% endfor %}
</body>
</html>
```

---

## **13. Configure URLs**

### Add Routes in `file_manager/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('file/<int:file_id>/', views.display_image, name='display_image'),
]
```

### Include App URLs in `file_app/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('file_manager.urls')),
]
```

---

## **14. Run the Server**

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/upload/](http://127.0.0.1:8000/upload/) to test the application.

---

## **15. Features to Test**

- Upload valid image files (JPEG, PNG, GIF) under 5 MB.
- Uploaded images are listed (latest 5 only).
- Download or view uploaded images.
- Let me know if you have any questions

