from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from arivarton.base.models import CustomImage
from arivarton.makai.models import Country, City, Coordinate, Location, Sea, Harbour

'''
N.B. To see what icons are available for use in Wagtail menus and StreamField block types,
enable the styleguide in settings:
INSTALLED_APPS = (
   ...
   'wagtail.contrib.styleguide',
   ...
)
or see http://kave.github.io/general/2015/12/06/wagtail-streamfield-icons.html
This demo project includes the full font-awesome set via CDN in base.html, so the entire
font-awesome icon set is available to you. Options are at http://fontawesome.io/icons/.
'''

class MakaiSeaAdmin(ModelAdmin):
    menu_icon = 'doc-empty'
    model = Sea

class MakaiCountryAdmin(ModelAdmin):
    menu_icon = 'doc-empty'
    model = Country

class MakaiCityAdmin(ModelAdmin):
    menu_icon = 'doc-empty'
    model = City

class MakaiHarbourAdmin(ModelAdmin):
    menu_icon = 'doc-empty'
    model = Harbour

class MakaiCoordinateAdmin(ModelAdmin):
    menu_icon = 'doc-empty'
    model = Coordinate

class MakaiLocationAdmin(ModelAdmin):
    menu_icon = 'form'
    model = Location

class MakaiImageAdmin(ModelAdmin):
    menu_label = 'Gallery images'
    model = CustomImage

class MakaiLocationsModelAdminGroup(ModelAdminGroup):
    menu_label = 'Makai - Locations'
    menu_icon = 'folder'  # change as required
    menu_order = 000  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (MakaiSeaAdmin,
             MakaiCountryAdmin,
             MakaiCityAdmin,
             MakaiHarbourAdmin,
             MakaiCoordinateAdmin,
             MakaiLocationAdmin)

modeladmin_register(MakaiLocationsModelAdminGroup)
