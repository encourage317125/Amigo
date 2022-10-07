function show_confirmation_popup() {
    $("#android_notification_modal .flipper").addClass('hover');
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            var csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$(document).ready(function(){

    /*==================================================
    =            SMS / CONTACT / NEWSLETTER            =
    ==================================================*/  
    

    $('form.form-sms, form.form-email, form.form-newsletter').submit(function(e) {
        if (e.preventDefault) e.preventDefault();
        else e.returnValue = false;

        var thisForm = $(this).closest('form.form-sms, form.form-email, form.form-newsletter'),
            submitButton = thisForm.find('button[type="submit"]'),
            error = 0,
            apiUrl = '',
            originalError = thisForm.attr('original-error'),
            preparedForm, userNumber, successRedirect, successCallback, formError, formSuccess;

        thisForm.find('.form-error, .form-success').remove();
        submitButton.attr('data-text', submitButton.text());
        thisForm.append('<div class="form-error" style="display: none;">' + thisForm.attr('data-error') + '</div>');
        thisForm.append('<div class="form-success" style="display: none;">' + thisForm.attr('data-success') + '</div>');
        formError = thisForm.find('.form-error');
        formSuccess = thisForm.find('.form-success');
        thisForm.addClass('attempted-submit');

        if (validateFields(thisForm) === 1) {
            formError.fadeIn(200);
            setTimeout(function() {
                formError.fadeOut(500);
            }, 3000);
        } else {

            thisForm.removeClass('attempted-submit');

            // Hide the error if one was shown
            formError.fadeOut(200);
            
            // Create a new loading spinner in the submit button.
            submitButton.html(jQuery('<div />').addClass('form-loading')).attr('disabled', 'disabled');

            if(thisForm.hasClass('form-email')) {
                apiUrl = '/send_email/';
            } else if(thisForm.hasClass('form-sms')) {
                apiUrl = '/send_sms/';
            } else if(thisForm.hasClass('form-newsletter')) {
                apiUrl = '/subscribe_mailchimp/';
            }

            jQuery.ajax({
                type: "POST",
                url: apiUrl,
                data: thisForm.serialize(),
                success: function(response) {
                    // Swiftmailer always sends back a number representing numner of emails sent.
                    // If this is numeric (not Swift Mailer error text) AND greater than 0 then show success message.

                    submitButton.html(submitButton.attr('data-text')).removeAttr('disabled');

                    if ($.isNumeric(response)) {
                        if (parseInt(response) > 0) {
                            // For some browsers, if empty 'successRedirect' is undefined; for others,
                            // 'successRedirect' is false.  Check for both.
                            successRedirect = thisForm.attr('success-redirect');
                            if (typeof successRedirect !== typeof undefined && successRedirect !== false && successRedirect !== "") {
                                window.location = successRedirect;
                            }

                            successCallback = thisForm.attr('success-callback');
                            // For some browsers, if empty `successCallback` is undefined; for others,
                            // `successCallback` is false.  Check for both.
                            if (typeof successCallback !== typeof undefined && successCallback !== false && successCallback !== "") {
                                eval(successCallback);
                            }

                            thisForm.find('input[type="text"]').val("");
                            thisForm.find('textarea').val("");
                            thisForm.find('.form-success').fadeIn(1000);

                            formError.fadeOut(1000);
                            setTimeout(function() {
                                formSuccess.fadeOut(500);
                            }, 5000);
                        } else {
                            // API Error (Twillio SDK Error)
                            formError.text(thisForm.attr('data-apierror')).fadeIn(1000);
                            formSuccess.fadeOut(1000);
                        }
                    }
                    // If error text was returned, put the text in the .form-error div and show it.
                    else {
                        // Show the error with the returned error text.
                        formError.text(response).fadeIn(1000);
                        formSuccess.fadeOut(1000);
                    }
                },
                error: function(errorObject, errorText, errorHTTP) {
                    // Show the error with the returned error text.
                    formError.text(errorHTTP).fadeIn(1000);
                    formSuccess.fadeOut(1000);
                    submitButton.html(submitButton.attr('data-text')).removeAttr('disabled');
                }
            });
        }

        return false;
    });


    $('.validate-required, .validate-email').on('blur change', function() {
        validateFields($(this).closest('form'));
    });

    $('form').each(function() {
        if ($(this).find('.form-error').length) {
            $(this).attr('original-error', $(this).find('.form-error').text());
        }
    });

    function validateFields(form) {
        var name, error;
        var regex = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/;


        $(form).find('.validate-required[type="checkbox"]').each(function() {
            if (!$('[name="' + $(this).attr('name') + '"]:checked').length) {
                error = 1;
                name = $(this).attr('name').replace('[]', '');
                form.find('.form-error').text('Please tick at least one ' + name + ' box.');
            }
        });

        $(form).find('.validate-required, .validate-email, .validate-phone').each(function() {
            $(this).removeClass('field-error');
        })

        $(form).find('.validate-required').each(function() {
            if ($(this).val() === '') {
                $(this).addClass('field-error');
                error = 1;
            }
        });

        $(form).find('.validate-email').each(function() {
            if (!(/(.+)@(.+){2,}\.(.+){2,}/.test($(this).val()))) {
                $(this).addClass('field-error');
                error = 1;
            }
        });

        $(form).find('.validate-phone').each(function() {
            if(!regex.test($(this).val())) {
                $(this).addClass('field-error');
                error = 1;
            }
        });

        if (!form.find('.field-error').length) {
            form.find('.form-error').fadeOut(1000);
        }

        return error;
    }
});


(function ( $ ) {
 
    $.fn.colorScroll = function() {
        return this.each(function() {
        	$t = $(this);
	        var colors = $t.data("colors");
			var colors_array = colors.split(":");
			var numcolors = colors_array.length;

			var RGBs = [];
			for(var i = 0; i < numcolors; i++) {
				RGBs[i] = [];
				var c = colors_array[i].split(",");
				
				RGBs[i][0] = c[0];
				RGBs[i][1] = c[1];
				RGBs[i][2] = c[2];
			}

			var dRGBs = [];
			for(var i = 0; i < (numcolors - 1); i++) {
				dRGBs[i] = [];
				
				dRGBs[i][0] = RGBs[i][0] - RGBs[i+1][0];
				dRGBs[i][1] = RGBs[i][1] - RGBs[i+1][1];
				dRGBs[i][2] = RGBs[i][2] - RGBs[i+1][2];
			}

            function update() {
                var position = $(window).scrollTop() - $t.offset().top;
                var view = $(window).height();
                var height = $t.height();
                var travel = height - view;

                if(position<0 || position>travel) {
                    return;
                }

                var percent = position / travel;
                var level = Math.floor(percent * (numcolors - 1));
                var plevel = percent * (numcolors - 1);
                
                var dlevel = Math.floor(level);
                if(Math.floor(level) == (numcolors - 1)) {
                    dlevel = Math.floor(level) - 1;
                }
                
                if(plevel > 1) {
                    plevel = plevel - dlevel;
                }
                
                var nRed = (RGBs[dlevel][0] - Math.round(dRGBs[dlevel][0] * plevel));
                var nGreen = (RGBs[dlevel][1] - Math.round(dRGBs[dlevel][1] * plevel));
                var nBlue = (RGBs[dlevel][2] - Math.round(dRGBs[dlevel][2] * plevel));
                
                $t.css("background-color", "rgb(" + nRed + "," + nGreen + "," + nBlue + ")");
            }

			$(window).scroll(update);
            $(window).resize(update);
	    });
    };

    $(document).ready(function(){
    	$(".colorScroll").colorScroll();
    })
 
}( jQuery ));
