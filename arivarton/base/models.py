from django.db import models

from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.snippets.models import register_snippet

from django.core.validators import RegexValidator


@register_snippet
class Location(models.Model):
    country = models.CharField(max_length=54, blank=True)
    city = models.CharField(max_length=90, blank=True)
    description = models.CharField(max_length=180)
    coordinates = models.CharField(max_length=36,
                                   help_text="Comma separated lat/long. \
                                              (Ex. 64.144367, -21.939182) \
                                              Right click Google Maps and select 'What\'s Here'",
                                   validators=[
                                       RegexValidator(
                                           regex=r'^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$',
                                           message='Lat Long must be a comma-separated numeric \
                                                    lat and long.',
                                           code='invalid_lat_long'),
                                   ],
                                   blank=True)


class CustomImage(AbstractImage):
    location = models.ForeignKey('Location', null=True, blank=True, on_delete=models.SET_NULL)
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
