from node.tests import patch
from node.utils import UNSET
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.compat import IS_PY2
from yafowil.tests import YafowilTestCase
from yafowil.tests import fxml
from yafowil.widget.recaptcha import widget as recaptcha_widget
import yafowil.loader


if not IS_PY2:
    from importlib import reload


class DummyRequest(dict):
    @property
    def request(self):
        return self


class RecaptchaResult(object):
    is_valid = False
    error_code = 'incorrect-captcha-sol'


recaptcha_result = RecaptchaResult()


def mock_submit(challenge_field, response_field, private_key, remote_addr):
    return recaptcha_result


class TestRecaptchaWidget(YafowilTestCase):

    def setUp(self):
        super(TestRecaptchaWidget, self).setUp()
        from yafowil.widget.recaptcha import widget
        reload(widget)

    def test_edit_renderer(self):
        # Render map widget with defaults
        widget = factory(
            'recaptcha',
            name='recaptcha',
            props={
                'public_key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
                'private_key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
                'lang': 'de',
                'theme': 'clean',
            })
        self.check_output("""
        <div>
          <div class="recaptcha" data-lang="de"
               data-public_key="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
               data-theme="clean" id="recaptcha-recaptcha">
          </div>
          <noscript>
            <iframe src="http://www.google.com/recaptcha/api/noscript?k=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                    height="300" width="500" frameborder="0">
            </iframe>
            <br/>
            <textarea name="recaptcha_challenge_field" rows="3" cols="40"/>
            <input type="hidden" name="recaptcha_response_field"
                   value="manual_challenge"/>
          </noscript>
        </div>
        """, fxml('<div>\n' + widget() + '</div>'))

    def test_display_renderer(self):
        # Display renderer is not implemented
        widget = factory('recaptcha', 'recaptcha', mode='display')
        self.assertEqual(widget(), None)

    @patch(recaptcha_widget, 'submit', mock_submit)
    def test_extraction(self):
        # Widget extraction
        widget = factory(
            'recaptcha',
            name='recaptcha',
            props={
                'public_key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
                'private_key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
                'lang': 'de',
                'theme': 'clean',
            })

        request = DummyRequest()
        data = widget.extract(request)
        self.assertEqual(
            data.errors,
            [ExtractionError('The CAPTCHA solution was incorrect.')]
        )

        recaptcha_result.is_valid = True
        request = DummyRequest()
        request['recaptcha_challenge_field'] = '1234'
        request['recaptcha_response_field'] = 'manual_challenge'
        data = widget.extract(request)
        self.assertEqual(data.errors, [])


if __name__ == '__main__':
    unittest.main()                                          # pragma: no cover

