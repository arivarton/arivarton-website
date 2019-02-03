from wagtail.core import hooks

from arivarton.makai.routes.models import RoutePage

def create_or_modify_collection(page, page_class):
    ''' Create a image collection for a page. '''
    if isinstance(page, page_class):
        page.set_collection()

@hooks.register('after_create_page')
def after_create_page(request, page):
    # Add new collection with page name
    create_or_modify_collection(page, RoutePage)

@hooks.register('after_edit_page')
def after_edit_page(request, page):
    # Edit image collection name
    create_or_modify_collection(page, RoutePage)

@hooks.register('after_delete_page')
def after_delete_page(request, page):
    # Delete image collection for page
    page.clean_collection()
