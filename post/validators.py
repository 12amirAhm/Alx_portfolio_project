from django.core.exceptions import ValidationError

def file_size(value):
    filesize=value.size
    if filesize>320000000:
        raise ValidationError("Sorry Your videos should be Under 40MB")