from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import Group, Permission

from wagtail.core.models import Page, Collection, GroupCollectionPermission
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

    def get_root_collection(self):
        return Collection.objects.get(name='Root')

    def get_main_collection(self):
        main_name = 'Main'
        try:
            main_collection = Collection.objects.get(name='Main')
        except Collection.DoesNotExist:
            root_collection = self.get_root_collection()
            main_collection = root_collection.add_child(name=main_name)

            # Permissions
            groups = ('Moderators', 'Editors')
            for group in groups:
                group = Group.objects.get(name=group)

                # Delete all permissions for root collection
                group.collection_permissions.filter(collection=root_collection).delete()

                # Add permissions for main collection
                GroupCollectionPermission(
                    group=group,
                    collection=main_collection,
                    permission=Permission.objects.get(content_type__app_label='wagtaildocs',
                                                      codename='add_document')
                ).save()
                GroupCollectionPermission(
                    group=group,
                    collection=main_collection,
                    permission=Permission.objects.get(content_type__app_label='wagtaildocs',
                                                      codename='change_document')
                ).save()
                GroupCollectionPermission(
                    group=group,
                    collection=main_collection,
                    permission=Permission.objects.get(content_type__app_label='wagtailimages',
                                                      codename='add_image')
                ).save()
                GroupCollectionPermission(
                    group=group,
                    collection=main_collection,
                    permission=Permission.objects.get(content_type__app_label='wagtailimages',
                                                      codename='change_image')
                ).save()

        return main_collection

    def get_parent_collection(self):
        ''' Set up inital stages for a image collection. '''
        parent_name = self.get_parent_collection_name()
        main_collection = self.get_main_collection()
        try:
            parent_collection = main_collection.get_children().get(name=parent_name)
        except Collection.DoesNotExist:
            parent_collection = main_collection.add_child(name=parent_name)

        return parent_collection

    def get_deleted_parent_collection(self):
        root_collection = self.get_root_collection()
        try:
            deleted_collection = root_collection.get_children().get(name='Deleted')
        except Collection.DoesNotExist:
            deleted_collection = root_collection.add_child(name='Deleted')

        return deleted_collection

    def get_deleted_collection(self):
        collection_name = '%s - %s' % (self.get_parent_collection_name(), self.slug)
        parent_collection = self.get_deleted_parent_collection()
        try:
            deleted_collection = parent_collection.get_children().get(name=collection_name)
        except Collection.DoesNotExist:
            deleted_collection = parent_collection.add_child(name=collection_name)

        return deleted_collection

    def set_collection(self):
        ''' Set the collection when creating or editing a RoutePage.
        Every RoutePage needs a separate collection for images.'''
        parent_name = self.get_parent_collection_name()
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

    def clean_collection(self):
        ''' When deleting page move connected collection to a waste collection. '''
        deleted_collection = self.get_deleted_collection()
        # Setup collection to store deleted collections
        if self.image_collection.get_parent() != deleted_collection:
            self.image_collection.move(deleted_collection, pos='last-child')
