from yafowil.base import factory
from yafowil.utils import entry_point
import os


resourcedir = os.path.join(os.path.dirname(__file__), 'resources')
js = [{
    'group': 'yafowil.widget.recaptcha.dependencies',
    'resource': 'recaptcha_ajax.js',
    'order': 20,
}, {
    'group': 'yafowil.widget.recaptcha.common',
    'resource': 'widget.js',
    'order': 23,
}]


@entry_point(order=10)
def register():
    from yafowil.widget.recaptcha import widget
    factory.register_theme('default', 'yafowil.widget.recaptcha',
                           resourcedir, js=js)
