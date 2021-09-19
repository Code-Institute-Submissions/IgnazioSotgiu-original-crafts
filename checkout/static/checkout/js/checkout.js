document.addEventListener("DOMContentLoaded", function() {
    var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
    var clientSecret = $('#id_client_secret').text().slice(1, -1);

    var stripe = Stripe(stripePublicKey);
    var submitButton = document.getElementById('submit');
    var elements = stripe.elements();

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
            </span>`
            $(displayError).html(html);
        } else {
            displayError.textContent = ''; 
        }
    });
});