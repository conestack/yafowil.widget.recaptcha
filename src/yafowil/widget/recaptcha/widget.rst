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
       <textarea name="recaptcha_challenge_field" rows="3" cols="40">
       </textarea>
       <input type="hidden" name="recaptcha_response_field" value="manual_challenge"/>
    </noscript>
    </div>
    <BLANKLINE>
