Import requirements::

    >>> import yafowil.loader
    >>> from yafowil.base import factory

Render map widget with defaults::

    >>> widget = factory('recaptcha', 'recaptcha', props={
    ...     'public_key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    ...     'private_key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    ...     'lang': 'de',
    ...     'theme': 'clean',
    ... })
    >>> pxml('<div>\n' + widget() + '</div>')
    <div>
    <div class="recaptcha" data-lang="de" data-public_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" data-theme="clean" id="recaptcha-recaptcha"> </div>
    <noscript>
       <iframe src="http://www.google.com/recaptcha/api/noscript?k=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" height="300" width="500" frameborder="0">
       </iframe>
       <br/>
       <textarea name="recaptcha_challenge_field" rows="3" cols="40"/>
       <input type="hidden" name="recaptcha_response_field" value="manual_challenge"/>
    </noscript>
    </div>
    <BLANKLINE>

Display renderer is not implemented::

    >>> widget = factory('recaptcha', 'recaptcha', mode='display')
    >>> widget()

Patch from ``recaptcha.client.captcha.submit`` on
``yafowil.widget.recaptcha.widget``::

    >>> class RecaptchaResult(object):
    ...     is_valid = False
    ...     error_code = 'incorrect-captcha-sol'

    >>> recaptcha_result = RecaptchaResult()

    >>> def submit(challenge_field, response_field, private_key, remote_addr):
    ...     return recaptcha_result

    >>> from yafowil.widget.recaptcha import widget
    >>> submit_orgin = widget.submit
    >>> widget.submit = submit

Dummy request::

    >>> class DummyRequest(dict):
    ...     @property
    ...     def request(self):
    ...         return self

Widget extraction::

    >>> widget = factory('recaptcha', 'recaptcha', props={
    ...     'public_key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    ...     'private_key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    ...     'lang': 'de',
    ...     'theme': 'clean',
    ... })
    >>> request = DummyRequest()
    >>> data = widget.extract(request)

    >>> data.errors
    [ExtractionError('The CAPTCHA solution was incorrect.',)]

    >>> recaptcha_result.is_valid = True
    >>> request = DummyRequest()
    >>> request['recaptcha_challenge_field'] = '1234'
    >>> request['recaptcha_response_field'] = 'manual_challenge'
    >>> data = widget.extract(request)

    >>> data.errors
    []

Reset patch::

    >>> widget.submit = submit_orgin
