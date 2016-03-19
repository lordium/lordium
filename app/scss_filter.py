from django.conf import settings

from django_pyscss.compressor import DjangoScssFilter
from django_pyscss import DjangoScssCompiler

from scss.namespace import Namespace
from scss.types import String

import six

class ScssFilter(DjangoScssFilter):
    def __init__(self, *args, **kwargs):
        super(ScssFilter, self).__init__(*args, **kwargs)

        self.namespace = Namespace()

        self.namespace.set_variable(
            '$static_url',
            String(six.text_type(getattr(settings, 'STATIC_URL', '/static/')))
        )

    # Create a compiler with the right namespace
    @property
    def compiler(self):
        return DjangoScssCompiler(
            namespace=self.namespace
        )