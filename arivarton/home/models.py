from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
    ]
    subpage_types = ['makai.MakaiIndex']
    parent_page_types = []

    def main_menu(self):
        menu = self.get_children().live().in_menu()
        for i in menu:
            i.descendants = i.get_descendants().live().in_menu()
        return menu
