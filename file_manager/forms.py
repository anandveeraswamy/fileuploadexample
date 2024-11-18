from django import forms
from django.core.exceptions import ValidationError

ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif']
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

class FileUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']

        # Check file type
        if uploaded_file.content_type not in ALLOWED_IMAGE_TYPES:
            raise ValidationError('Invalid file type. Only image files are allowed.')

        # Check file size
        if uploaded_file.size > MAX_FILE_SIZE:
            raise ValidationError(f'File size exceeds the limit of {MAX_FILE_SIZE // (1024 * 1024)} MB.')

        return uploaded_file