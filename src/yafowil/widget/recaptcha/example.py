from yafowil.base import factory
import os


DOC_RECAPTCHA = """
reCAPTCHA
---------

reCAPTCHA widget.

.. code-block:: python

    recaptcha_public_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    recaptcha_private_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    captcha = factory('#field:recaptcha', props={
        'label': 'Verify',
        'public_key': recaptcha_public_key,
        'private_key': recaptcha_private_key,
        'lang': 'de',
        'theme': 'clean',
        'error.position': 'after',
    })
"""

def recaptcha_example():
    form = factory('fieldset', name='yafowil.widget.recaptcha.recaptcha')
    recaptcha_public_key = os.environ['recaptcha_public_key']
    recaptcha_private_key = os.environ['recaptcha_private_key']
    form['captcha'] = factory('#field:recaptcha', props={
        'label': 'Verify',
        'public_key': recaptcha_public_key,
        'private_key': recaptcha_private_key,
        'lang': 'de',
        'theme': 'clean',
        'error.position': 'after',
    })
    return {
        'widget': form,
        'doc': DOC_RECAPTCHA,
        'title': 'reCAPTCHA',
    }


def get_example():
    return [
        recaptcha_example(),
    ]
