import os
import random
import string

from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_file(instance, filename):
    name, ext = get_filename_ext(filename)
    letters_str = string.ascii_letters + string.digits
    letters = list(letters_str)
    final_name = f"{''.join(random.choice(letters) for _ in range(10))}{ext}"
    return final_name
