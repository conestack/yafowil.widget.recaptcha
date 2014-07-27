import os
from yafowil.base import factory


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


def register():
    import widget
    factory.register_theme('default', 'yafowil.widget.recaptcha',
                           resourcedir, js=js)
