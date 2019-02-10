from django.db import models

from wagtail.images.models import Image, AbstractImage, AbstractRendition

from arivarton.makai.models import Location


class CustomImage(AbstractImage):
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=180, null=True, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        'location',
        'description'
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
