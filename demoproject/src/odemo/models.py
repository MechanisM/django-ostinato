from django.db import models

from ostinato.pages.models import Page, PageContent
from ckeditor.fields import RichTextField


class ContentMixin(models.Model):
    """
    An example of how you would do mixins. A mixin must be an abstract
    model.
    """
    content = models.TextField()

    class Meta:
        abstract = True  # Required for mixins


class CKContentMixin(PageContent):
    """ An Example of using a custom field directly on the model """
    content = RichTextField()

    class Meta:
        abstract = True


### Some inline extra fields for a landing page
from django.contrib import admin

class LandingPageContributors(models.Model):
    landing_page = models.ForeignKey(Page)
    name = models.CharField(max_length=100)

class LandingPageContributorsInline(admin.StackedInline):
    model = LandingPageContributors


# Actual Page Content
class LandingPage(ContentMixin, PageContent):
    intro = models.TextField()

    class ContentOptions:
        template = 'pages/tests/landing_page.html'
        page_inlines = [LandingPageContributorsInline]  # specify page inlines


class BasicPage(ContentMixin, PageContent):

    class ContentOptions:
        template = 'pages/tests/basic_page.html'
        view = 'ostinato.pages.views.CustomView'


class ContactPage(CKContentMixin):

    class ContentOptions:
        template = 'page_templates/contact_page.html'
        view = 'odemo.views.ContactView'


class ListPage(ContentMixin, PageContent):
    """ Example of a page that uses a custom form """

    related_page_group = models.ForeignKey(Page,
        related_name='related_to_listpage')

    class ContentOptions:
        template = 'page_templates/list_page.html'
        form = 'odemo.forms.CustomForm'


