from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from arivarton.base.models import Location, CustomImage

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


class MakaiLocationAdmin(ModelAdmin):
    model = Location


class MakaiImageAdmin(ModelAdmin):
    menu_label = 'Gallery images'
    model = CustomImage


class MakaiModelAdminGroup(ModelAdminGroup):
    menu_label = 'Makai'
    menu_icon = 'folder'  # change as required
    menu_order = 000  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (MakaiLocationAdmin, MakaiImageAdmin)

modeladmin_register(MakaiModelAdminGroup)
