$(document).ready(function() {
    var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
    var clientSecret = $('#id_client_secret').text().slice(1, -1);

    var stripe = Stripe(stripePublicKey);

    // var submitButton = document.getElementById('submit');
    // var clientSecret = submitButton.getAttribute('data-secret');
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
    var elements = stripe.elements();
    var card = elements.create('card', {
        style: style
    });
    card.mount('#card-element');

    // checking card details for possible errors

    card.on('change', function (e) {
        var displayError = document.getElementById('card-errors');
        if (e.error) {
            displayError.textContent = e.error.message;
            $('#card-errors').addClass('text-danger');
        } else {
            displayError.textContent = '';
            $('#card-errors').removeClass('text-danger');
        }
    })
    var form = document.getElementById('payment-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        card.update({'disabled': true});
        $('#submit').attr('disabled', true);
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.buyer_name.value),
                    deliver_to_name: $.trim(form.deliver_to_name.value),
                    email: $.trim(form.email_adddess.value),
                    address:{
                        street_address: $.trim(form.street_address.value),
                        town_or_city: $.trim(form.town_or_city.value),
                        county: $.trim(form.county.value),
                        country: $.trim(form.country.value),
                        postcode: $.trim(form.zip_postcode.value),
                    }
                }
            },
        })
        .then(function(result) {
            // Handle result.error or result.paymentIntent
            if (result.error){
                console.log(result.error.message)
            } else {
                if (result.paymentIntent.status == 'succeeded') {
                    console.log('payment processed')
                }
            }
        });
    })
})
