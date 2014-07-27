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
from recaptcha.client.captcha import (
    displayhtml,
    submit,
)


def recaptcha_extractor(widget, data):
    #info = IRecaptchaInfo(self.request)
    #if info.verified:
    #    return True
    challenge_field = self.request.get('recaptcha_challenge_field')
    response_field = self.request.get('recaptcha_response_field')
    private_key = attr_value('private_key', widget, data)
    remote_addr = self.request.get('HTTP_X_FORWARDED_FOR', '').split(',')[0]
    if not remote_addr:
        remote_addr = self.request.get('REMOTE_ADDR')
    res = submit(challenge_field,
                 response_field,
                 private_key,
                 remote_addr)
    if not res.is_valid:
        raise ExtractionError(res.error_code)
    #info.verified = res.is_valid
    return True


@managedprops(*['public_key', 'private_key'] + css_managed_props)
def recaptcha_edit_renderer(widget, data):
    lang = 'en'
    options = """
    <script type="text/javascript">
    var RecaptchaOptions = {
        lang: '{lang}',
        theme: '{theme}'
    };
    </script>
    """ % {
        'lang': attr_value('lang', widget, data),
        'theme': attr_value('theme', widget, data),
    }
    use_ssl = self.request['SERVER_URL'].startswith('https://')
    #error = IRecaptchaInfo(self.request).error
    error = data.error
    public_key = attr_value('public_key', widget, data)
    return options + displayhtml(public_key, use_ssl=use_ssl, error=error)


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

factory.defaults['recaptcha.public_key'] = ''
factory.doc['props']['recaptcha.public_key'] = """\
reCAPTCHA public key. Used in the JavaScript code that is served to your users.
"""

factory.defaults['recaptcha.private_key'] = ''
factory.doc['props']['recaptcha.private_key'] = """\
reCAPTCHA private key. Used when communicating between your server and our
server. Be sure to keep it a secret.
"""

factory.defaults['recaptcha.lang'] = 'en'
factory.doc['props']['recaptcha.lang'] = """\
Language code.
"""

factory.defaults['recaptcha.theme'] = 'red'
factory.doc['props']['recaptcha.theme'] = """\
Used Theme. Available default themes are 'red' (Default), 'white', 'blackglass'
and 'clean'.
"""
