from django.db import models
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel

from django.core.validators import RegexValidator

class MakaiIndex(Page):
    intro = models.CharField(max_length=250)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    subpage_types = ['gallery.GalleryIndex',
                     'routes.RouteIndex']


class Sea(models.Model):
    name = models.CharField(max_length=72)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=54)
    country_code = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    name = models.CharField(max_length=90)

    def __str__(self):
        return self.name



class Harbour(models.Model):
    city = models.ForeignKey('City', null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=90)
    website = models.URLField()
    vhf_channel = models.IntegerField()
    contact_person = models.ForeignKey('People', blank=True, null=True, on_delete=models.SET_NULL,
                                       related_name='harbour_manager')

    def __str__(self):
        return self.name


class People(models.Model):
    full_name = models.CharField(max_length=90)
    country = models.ForeignKey('City', null=True, on_delete=models.SET_NULL)
    harbour = models.ForeignKey('Harbour', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.full_name


class EmailAddress(models.Model):
    owned_by = models.ForeignKey('People', on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.email


class PhoneNumber(models.Model):
    owned_by = models.ForeignKey('People', on_delete=models.CASCADE)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    phone_number = models.IntegerField()

    def __str__(self):
        return self.phone_number


class Coordinate(models.Model):
    description = models.CharField(max_length=180, blank=True)
    lat_long = models.CharField(max_length=36,
                                help_text="Comma separated lat/long. \
                                           (Ex. 64.144367, -21.939182) \
                                           Right click Google Maps and select 'What\'s Here'",
                                validators=[
                                    RegexValidator(
                                        regex=r'^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$',
                                        message='Lat Long must be a comma-separated numeric \
                                                 lat and long.',
                                        code='invalid_lat_long'),
                                ])

    def __str__(self):
        return self.lat_long


class Location(models.Model):
    country = models.ForeignKey('Country', blank=True, null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey('City', blank=True, null=True, on_delete=models.SET_NULL)
    harbour = models.ForeignKey('Harbour', blank=True, null=True, on_delete=models.SET_NULL)
    sea = models.ForeignKey('Sea', blank=True, null=True, on_delete=models.SET_NULL)
    coordinate = models.ForeignKey('Coordinate', blank=True, null=True, on_delete=models.SET_NULL)

    def clean(self):
        if not (self.country or
                self.city or
                self.sea or
                self.coordinate or
                self.harbour):
            raise ValidationError('One of the five options must be set.')
        if self.sea and (self.country or self.city or self.harbour):
            raise ValidationError('A sea cannot be in the same location as a country/city/harbour.')
        if self.city:
            self.country = self.city.country
        # Check if model with same values already exists
        filter_on = model_to_dict(self)
        filter_on.pop('id')
        if Location.objects.filter(**filter_on).exists():
            raise ValidationError('This object already exists!')

    def __str__(self):
        if self.city:
            return str(self.city)
        elif self.country:
            return str(self.country)
        elif self.sea:
            return str(self.sea)
        elif self.coordinate:
            return str(self.coordinate)
        elif self.harbour:
            return str(self.harbour)
