from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet

from django.core.validators import RegexValidator

class MakaiIndex(Page):
    intro = models.CharField(max_length=250)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    subpage_types = ['gallery.GalleryIndex',
                     'routes.RouteIndex']

@register_snippet
class Sea(models.Model):
    name = models.CharField(max_length=72)

@register_snippet
class Country(models.Model):
    name = models.CharField(max_length=54)

@register_snippet
class City(models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    name = models.CharField(max_length=90)

@register_snippet
class Location(models.Model):
    city = models.ForeignKey('City', blank=True, null=True, on_delete=models.SET_NULL)
    sea = models.ForeignKey('Sea', blank=True, null=True, on_delete=models.SET_NULL)
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
