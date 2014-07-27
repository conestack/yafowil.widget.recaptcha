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
    <script type="text/javascript">
    var RecaptchaOptions = {
        lang: 'de',
        theme: 'clean'
    };
    </script>
    <script type="text/javascript" src="http://www.google.com/recaptcha/api/challenge?k=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"/>
    <BLANKLINE>
    <noscript>
      <iframe src="http://www.google.com/recaptcha/api/noscript?k=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" height="300" width="500" frameborder="0"/><br/>
      <textarea name="recaptcha_challenge_field" rows="3" cols="40"/>
      <input type="hidden" name="recaptcha_response_field" value="manual_challenge"/>
    </noscript>
    </div>
    <BLANKLINE>
