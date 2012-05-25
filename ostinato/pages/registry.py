from django.utils.datastructures import SortedDict
from appregister import NamedRegistry


class ContentRegister(NamedRegistry):
    base = 'ostinato.pages.models.PageContent'
    discovermodule = 'models'

    def setup(self):
        self._registry = SortedDict()

    def get_template_choices(self):
        template_choices = (('', '--------'),)

        for k, v in self.all().iteritems():
            content_name = v.__name__
            template_choices += (
                ('%s.%s' % (v._meta.app_label.lower(), v.__name__.lower()), k),)

        return template_choices


page_content = ContentRegister()

