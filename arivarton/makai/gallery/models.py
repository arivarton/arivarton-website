from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import Tag, TaggedItemBase

from arivarton.makai.routes.models import RoutePage

class GalleryIndex(RoutablePageMixin, Page):
    intro = models.CharField(max_length=250)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    subpage_types = ['GalleryPage']

    # Defines a method to access the children of the page (e.g. GalleryPage
    # objects). On the demo site we use this on the HomePage
    def get_gallery_pages(self):
        route_pages = []
        for page in RoutePage.objects.all():
            if page.has_images():
                route_pages.append(page)
        return route_pages


    # Overrides the context to list all child items, that are live, by the
    # date that they were published
    # http://docs.wagtail.io/en/latest/getting_started/tutorial.html#overriding-context
    def get_context(self, request):
        context = super(GalleryIndex, self).get_context(request)
        context['posts'] = GalleryPage.objects.descendant_of(
            self).live().order_by(
                '-date_published')
        return context

    # This defines a Custom view that utilizes Tags. This view will return all
    # related GalleryPages for a given Tag or redirect back to the GalleryIndex.
    # More information on RoutablePages is at
    # http://docs.wagtail.io/en/latest/reference/contrib/routablepage.html
    @route(r'^tags/$', name='tag_archive')
    @route(r'^tags/([\w-]+)/$', name='tag_archive')
    def tag_archive(self, request, tag=None):

        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no gallery pages tagged with "{}"'.format(tag)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)

        posts = self.get_posts(tag=tag)
        context = {
            'tag': tag,
            'posts': posts
        }
        return render(request, 'blog/blog_index_page.html', context)

    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)

    # Returns the child GalleryPage objects for this GalleryPageIndex.
    # If a tag is used then it will filter the posts by tag.
    def get_posts(self, tag=None):
        posts = GalleryPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag)
        return posts

    # Returns the list of Tags for all child posts of this GalleryPage.
    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            # Not tags.append() because we don't want a list of lists
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags


class GalleryPageTag(TaggedItemBase):
    """
    This model allows us to create a many-to-many relationship between
    the GalleryPage object and tags. There's a longer guide on using it at
    http://docs.wagtail.io/en/latest/reference/pages/model_recipes.html#tagging
    """
    content_object = ParentalKey('GalleryPage',
                                 related_name='tagged_items',
                                 on_delete=models.CASCADE)


class GalleryPage(Page):
    intro = models.CharField(max_length=250)
    tags = ClusterTaggableManager(through=GalleryPageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('tags')
    ]
    parent_page_types = ['GalleryIndex']
    subpage_types = []

    @property
    def get_tags(self):
        """
        Similar to the authors function above we're returning all the tags that
        are related to the blog post into a list we can access on the template.
        We're additionally adding a URL to access GalleryPage objects with that tag
        """
        tags = self.tags.all()
        for tag in tags:
            tag.url = '/'+'/'.join(s.strip('/') for s in [
                self.get_parent().url,
                'tags',
                tag.slug
            ])
        return tags
