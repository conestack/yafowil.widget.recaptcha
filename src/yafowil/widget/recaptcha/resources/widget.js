/*
 * yafowil recaptcha widget
 *
 * Requires: reCAPTCHA AJAX API
 * Optional: bdajax
 */

if (typeof(window.yafowil) == "undefined") yafowil = {};

(function($) {

    $(document).ready(function() {
        // initial binding
        yafowil.recaptcha.binder();

        // add after ajax binding if bdajax present
        if (typeof(window.bdajax) != "undefined") {
            $.extend(bdajax.binders, {
                recaptcha_binder: yafowil.recaptcha.binder
            });
        }
    });

    $.extend(yafowil, {

        recaptcha: {

            binder: function(context) {
                $('div.recaptcha', context).each(function() {
                    var elem = $(this);
                    var elem_id = elem.attr('id');
                    var public_key = elem.data('public_key');
                    var theme = elem.data('theme');
                    var lang = elem.data('lang');
                    Recaptcha.create(
                        public_key,
                        elem_id,
                        {
                            theme: theme,
                            lang: lang
                        }
                    );
                });
            },
        }
    });

})(jQuery);
