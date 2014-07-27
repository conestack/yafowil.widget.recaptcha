from node.utils import UNSET
from yafowil.common import generic_extractor
from yafowil.base import factory
from yafowil.utils import (
    managedprops,
    attr_value,
)
from yafowil.tsf import TSF
from recaptcha.client.captcha import (
    displayhtml,
    submit,
)


_ = TSF('yafowil.widget.recaptcha')


error_messages = dict()
error_messages['invalid-site-private-key'] = _(
    'invalid-site-private-key',
    default='We weren\'t able to verify the private key.')
error_messages['invalid-request-cookie'] = _(
    'invalid-request-cookie',
    default='The challenge parameter of the verify script was incorrect.')
error_messages['incorrect-captcha-sol'] = _(
    'incorrect-captcha-sol',
    default='The CAPTCHA solution was incorrect.')
error_messages['captcha-timeout'] = _(
    'captcha-timeout',
    default='The solution was received after the CAPTCHA timed out.')
error_messages['recaptcha-not-reachable'] = _(
    'recaptcha-not-reachable',
    default='Unable to contact the reCAPTCHA verify server.')


def recaptcha_extractor(widget, data):
    challenge_field = data.request.get('recaptcha_challenge_field')
    response_field = data.request.get('recaptcha_response_field')
    private_key = attr_value('private_key', widget, data)
    remote_addr = data.request.get('HTTP_X_FORWARDED_FOR', '').split(',')[0]
    if not remote_addr:
        remote_addr = data.request.get('REMOTE_ADDR')
    res = submit(challenge_field,
                 response_field,
                 private_key,
                 remote_addr)
    if not res.is_valid:
        raise ExtractionError(error_messages[res.error_code])
    return True


recaptcha_options = """\
<script type="text/javascript">
var RecaptchaOptions = {{
    lang: '{lang}',
    theme: '{theme}'
}};
</script>
"""


@managedprops(*['public_key', 'private_key'])
def recaptcha_edit_renderer(widget, data):
    options = recaptcha_options.format(**{
        'lang': attr_value('lang', widget, data),
        'theme': attr_value('theme', widget, data),
    })
    use_ssl = data.request.get('SERVER_URL', '').startswith('https://')
    error = None
    if data.errors:
        error = data.errors[0]
    public_key = attr_value('public_key', widget, data)
    return options + displayhtml(public_key, use_ssl=use_ssl, error=error)


def recaptcha_display_renderer(widget, data):
    return  ''


factory.register(
    'recaptcha',
    extractors=[recaptcha_extractor, generic_extractor],
    edit_renderers=[recaptcha_edit_renderer],
    display_renderers=[recaptcha_display_renderer])

factory.doc['blueprint']['recaptcha'] = \
"""Add-on blueprint
`yafowil.widget.recaptcha <http://github.com/bluedynamics/yafowil.widget.recaptcha/>`_
"""

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
