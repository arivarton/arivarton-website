from django.views.generic.base import TemplateView
from django.shortcuts import get_list_or_404, get_object_or_404

from wagtail.core.models import Collection

from arivarton.base.models import CustomImage
from arivarton.makai.routes.models import RoutePage


class SpecificGallery(TemplateView):
    template_name = 'gallery/specific_gallery.html'

    def get_context_data(self, **kwargs):
        context = super(SpecificGallery, self).get_context_data(**kwargs)
        root_collection = Collection.objects.get(id=1)
        main_collection = root_collection.get_children().get(name='Main')
        routepage_collection = main_collection.get_children().get(name='RoutePage')
        slug_collection = get_object_or_404(routepage_collection.get_children(),
                                            name=kwargs['route_name_slug'])

        context['images'] = get_list_or_404(CustomImage, collection=slug_collection)
        context['page'] = get_object_or_404(RoutePage, image_collection=slug_collection)

        return context
