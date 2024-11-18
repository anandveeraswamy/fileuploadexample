from django.shortcuts import render

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import FileUploadForm
from .models import File

# Allowed image MIME types
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif']

# Maximum file size (in bytes)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

# File upload view
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
    return render(request, 'file_manager/upload.html', {'form': form, 'files':files})

# File download view
def download_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    response = HttpResponse(file.content, content_type=file.content_type)
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    return response

def display_image(request, file_id):
    file = get_object_or_404(File, id=file_id)
    return HttpResponse(file.content, content_type=file.content_type)

