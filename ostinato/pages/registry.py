from django.utils.datastructures import SortedDict
from appregister import Registry


class ContentRegister(Registry):
    base = 'ostinato.pages.models.PageContent'
    discovermodule = 'models'

    def setup(self):
        self._registry = list()

    def register(self, class_):
 
        if not self.is_valid(class_):
            msg = "Object '%s' is not a subclass of '%s'" % (class_.__name__,
                self.base.__name__)
            raise InvalidOperation(msg)
 
        if self.is_registered(class_):
            msg = "Object '%s' has already been registered" % class_.__name__
            raise AlreadyRegistered(msg)
 
        self._registry.append(class_)
 
        return class_

    def get_template_choices(self):
        template_choices = (('', '--------'),)

        for v in self.all():
            content_type = '%s.%s' % (v._meta.app_label, v.__name__)
            verbose_name = '%s | %s' % (v._meta.app_label, v._meta.verbose_name)
            template_choices += ((content_type.lower(), verbose_name.title()), )

        return template_choices


page_content = ContentRegister()

