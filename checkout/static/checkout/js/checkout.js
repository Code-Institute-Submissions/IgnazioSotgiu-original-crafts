document.addEventListener("DOMContentLoaded", function() {
    // get stripePublicKey and clientSecret from checkout_page.html
    var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
    var clientSecret = $('#id_client_secret').text().slice(1, -1);

    var stripe = Stripe(stripePublicKey);
    var elements = stripe.elements();

    // code taken from stripe docs and code institute lecture
    var style = {
        base: {
            color: '#000',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            width: '30em',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#dc3545',
            iconColor: '#dc3545'
        }
    };
    var card = elements.create('card', {style: style});
    card.mount('#card-element');

     // checking changes to detect card errors
    card.addEventListener('change', function (event) {
        var displayError = document.getElementById('card-errors');
        if (event.error) {
            html = `
            <span class="text-danger">
            ${event.error.message}
            </span>`;
            $(displayError).html(html);
        } else {
            displayError.textContent = ''; 
        }
    });

    // get payment form values
    var form = document.getElementById('payment-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        card.update({'disabled': true});
        $('#form-post-button').attr('disabled', true);
        var saveAddressDetails = true;
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        var postData = {
            'csrfmiddlewaretoken': csrfToken,
            'client_secret': clientSecret,
            'save_address_details': saveAddressDetails,
            };
        var url = '/checkout/cache_checkout_data/';

        $.post(url, postData).done(function () {
            stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        name: $.trim(form.full_name.value),
                        phone: $.trim(form.phone_number.value),
                        email: $.trim(form.email_address.value),
                        address:{
                            line1: $.trim(form.street_address.value),
                            city: $.trim(form.town_or_city.value),
                            country: $.trim(form.country.value),
                            state: $.trim(form.county.value),
                        }
                    }
                },
            }).then(function(result) {
                if (result.error){
                    var displayError = document.getElementById('card-errors');
                    html = `
                        <span class="text-danger">
                        ${result.error.message}
                        </span>`;
                    $(displayError).html(html);
                    card.update({ 'disabled': false});
                    $('#form-post-button').attr('disabled', false);
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        form.submit();
                    }
                }
            });
        }).fail(function() {
            location.reload();
        });
    });
});