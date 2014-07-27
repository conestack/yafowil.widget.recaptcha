from node.utils import UNSET
from yafowil.common import generic_required_extractor
from yafowil.base import (
    factory,
    fetch_value,
)
from yafowil.utils import (
    cssid,
    cssclasses,
    css_managed_props,
    managedprops,
    attr_value,
    data_attrs_helper,
)


def recaptcha_extractor(widget, data):
    return UNSET


@managedprops(*css_managed_props)
def recaptcha_edit_renderer(widget, data):
    return  ''


def recaptcha_display_renderer(widget, data):
    return  ''


factory.register(
    'recaptcha',
    extractors=[recaptcha_extractor, generic_required_extractor],
    edit_renderers=[recaptcha_edit_renderer],
    display_renderers=[recaptcha_display_renderer])

factory.doc['blueprint']['recaptcha'] = \
"""Add-on blueprint
`yafowil.widget.recaptcha <http://github.com/bluedynamics/yafowil.widget.recaptcha/>`_
"""

factory.defaults['recaptcha.class'] = 'recaptcha'

factory.defaults['recaptcha.required'] = True

factory.defaults['recaptcha.error_class'] = 'error'

factory.defaults['recaptcha.message_class'] = 'errormessage'

#factory.defaults['recaptcha.'] = 47.2667
#factory.doc['props']['recaptcha.'] = """\
#"""
