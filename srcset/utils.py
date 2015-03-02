import os
from StringIO import StringIO

from django.core.files import File
from django.core.files.storage import default_storage

from PIL import Image

from .models import OriginalImage, ResizedImage


def get_sized_image(image, width):
    (orig, c) = OriginalImage.objects.get_or_create(image_file=image.name)
    if width >= image.width:
        return orig
    ratio = width / float(image.width)
    height = int(image.height * ratio + 0.5)
    image.open()
    orig_image = Image.open(image)
    new_image = orig_image.resize((width, height))
    image.close()
    data = StringIO()
    new_image.save(data, orig_image.format)
    split_ext = image.name.rsplit('.', 1)
    if len(split_ext) > 1:
        ext = split_ext[-1]
    else:
        ext = ''
    resized_path = default_storage.save(
        os.path.join('resized_images', image.name, '{}.{}'.format(width, ext)),
        File(data)
    )
    resized = ResizedImage.objects.create(
        original=orig,
        image_file=resized_path
    )
    return resized
