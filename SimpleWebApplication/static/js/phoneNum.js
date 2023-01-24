var wtf_phone_field = document.getElementById('phone');
    wtf_phone_field.style.position = 'absolute';
    wtf_phone_field.style.top = '-9999px';
    wtf_phone_field.style.left = '-9999px';
    wtf_phone_field.parentElement.insertAdjacentHTML('beforeend', '<div><input type="tel" id="_phone"></div>');
var fancy_phone_field = document.getElementById('_phone');
    var fancy_phone_iti = window.intlTelInput(fancy_phone_field, {
        separateDialCode: true,
        utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/16.0.4/js/utils.js",
    });
    fancy_phone_iti.setNumber(wtf_phone_field.value);
    fancy_phone_field.addEventListener('blur', function() {
    wtf_phone_field.value = fancy_phone_iti.getNumber();
});
