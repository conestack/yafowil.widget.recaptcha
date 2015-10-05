from recaptcha.client.captcha import submit
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.common import generic_extractor
from yafowil.tsf import TSF
from yafowil.utils import attr_value
from yafowil.utils import cssclasses
from yafowil.utils import cssid
from yafowil.utils import data_attrs_helper
from yafowil.utils import managedprops


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


NO_SCRIPT_TEMPLATE = """
<noscript>
   <iframe src="http://www.google.com/recaptcha/api/noscript?k={public_key}"
           height="300"
           width="500"
           frameborder="0">
   </iframe>
   <br />
   <textarea name="recaptcha_challenge_field"
             rows="3"
             cols="40"></textarea>
   <input type="hidden"
          name="recaptcha_response_field"
          value="manual_challenge" />
</noscript>
"""


def recaptcha_extractor(widget, data):
    request = data.request
    challenge_field = request.get('recaptcha_challenge_field')
    response_field = request.get('recaptcha_response_field')
    private_key = attr_value('private_key', widget, data)
    environ = getattr(request.request, 'environ', None)
    if not environ:
        environ = request.request
    remote_addr = environ.get('HTTP_X_FORWARDED_FOR', '').split(',')[0]
    if not remote_addr:
        remote_addr = environ.get('REMOTE_ADDR')
    res = submit(challenge_field, response_field, private_key, remote_addr)
    if not res.is_valid:
        raise ExtractionError(error_messages[res.error_code])
    return True


@managedprops('public_key', 'private_key', 'theme', 'lang')
def recaptcha_edit_renderer(widget, data):
    recaptcha_attrs = {
        'id': cssid(widget, 'recaptcha'),
        'class': ' '.join([cssclasses(widget, data)]),
    }
    data_attrs = ['theme', 'lang', 'public_key']
    recaptcha_attrs.update(data_attrs_helper(widget, data, data_attrs))
    recaptcha = data.tag('div', ' ', **recaptcha_attrs)
    public_key = attr_value('public_key', widget, data)
    return recaptcha + NO_SCRIPT_TEMPLATE.format(public_key=public_key)


def recaptcha_display_renderer(widget, data):
    pass


factory.register(
    'recaptcha',
    extractors=[recaptcha_extractor, generic_extractor],
    edit_renderers=[recaptcha_edit_renderer],
    display_renderers=[recaptcha_display_renderer])

factory.doc['blueprint']['recaptcha'] = \
"""Add-on blueprint
`yafowil.widget.recaptcha <http://github.com/bluedynamics/yafowil.widget.recaptcha/>`_
"""

factory.defaults['recaptcha.class'] = 'recaptcha'

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
