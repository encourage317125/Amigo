# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Standard Library
from django.utils.six import BytesIO

# Third Party Stuff
from PIL import Image
from versatileimagefield.datastructures import FilteredImage
from versatileimagefield.registry import versatileimagefield_registry


class FadeImageFilter(FilteredImage):

    """
    Returns a 0.3 alpha version of image on top of a white backgroud.
    """

    def process_image(self, image, image_format, save_kwargs={}):
        imagefile = BytesIO()
        # set the opacity of photo to 0.3
        image.putalpha(76)  # 255*0.3
        bg = Image.new('RGB', image.size, (255, 255, 255))
        bg.paste(image, image)
        bg.save(imagefile, **save_kwargs)
        return imagefile

# Registering the FadeImageFilter to be available on VersatileImageField
# via the `fade` attribute
versatileimagefield_registry.register_filter('fade', FadeImageFilter)
