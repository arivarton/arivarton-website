from django.db import models
from django.core.validators import RegexValidator

from wagtail.core.models import Page, Collection
from wagtail.admin.edit_handlers import FieldPanel

class RouteIndex(Page):
    intro = models.CharField(max_length=250)
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    subpage_types = ['RoutePage']

    def children(self):
        return self.get_children().specific().live()


class RoutePage(Page):
    description = models.TextField(
        help_text='Description of the route.\
                  \n\n- When it started/finished.\
                  \n\n- How it went.\
                  \n\n- Number and names of passengers.\
                  \n\n- Route deviations.\
                  \n\n- Any mishaps?')
    map_url = models.URLField(
        validators=[
            RegexValidator(
                regex=r'^(http)(s)?(://)(www.)?(google.com/maps/d/embed\?mid=)([\w\d-])+$',
                message='Route url must be a valid url to a google route planner map.',
                code='invalid_route_url'
            )
        ]
    )
    image_collection = models.ForeignKey(
        Collection,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Select the image collection for this route.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('map_url')
    ]
    subpage_types = []

    def get_parent_collection_name(self):
        return self.__class__.__name__

    def get_parent_collection(self):
        ''' Set up inital stages for a image collection. '''
        parent_name = get_parent_collection_name()
        try:
            parent_collection = Collection.objects.get(name=parent_name)
        except Collection.DoesNotExist:
            root_collection = Collection.objects.get(name='Root')
            parent_collection = root_collection.add_child(name=parent_name)

        return parent_collection

    def get_deleted_collection(self):
        deleted_collection_name = '_deleted from %s' % self.get_parent_collection_name()
        # Setup collection to store deleted collections
        try:
            deleted_collection = Collection.objects.get(name=deleted_collection_name)
        except Collection.DoesNotExist:
            parent_collection = self.get_parent_collection()
            deleted_collection = parent_collection.add_child(name=deleted_collection_name)

        return deleted_collection

    def set_collection(self):
        ''' Set the collection when creating or editing a RoutePage.
        Every RoutePage needs a separate collection for images.'''
        parent_name = get_parent_collection_name()
        collection_name = '%s - %s' % (parent_name, self.slug)

        # If RoutePage has not been previously created, the parent for all RoutePage collections
        # must be.
        parent_collection = self.get_parent_collection()

        # On edit
        if self.image_collection:
            self.image_collection.name = collection_name
            self.image_collection.save()
        # On create
        else:
            page_collection = parent_collection.add_child(
                name=collection_name
            )
            self.image_collection = page_collection
            self.save()