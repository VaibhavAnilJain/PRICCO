$(document).ready(function () {
    $('#RegisterStaticModal, #LoginStaticModal, #NewPasswordStaticModal').modal('show');

    $('#LoginPasswordShowHide a').on('click', function (event) {
        event.preventDefault();

        if ($('#LoginPasswordShowHide input').attr('type') == 'text') {
            $('#LoginPasswordShowHide input').attr('type', 'password');
            $('#LoginPasswordShowHide i').addClass('bi-eye-slash');
            $('#LoginPasswordShowHide i').removeClass('bi-eye');
        }
        else if ($('#LoginPasswordShowHide input').attr('type') == 'password') {
            $('#LoginPasswordShowHide input').attr('type', 'text');
            $('#LoginPasswordShowHide i').removeClass('bi-eye-slash');
            $('#LoginPasswordShowHide i').addClass('bi-eye');
        }
    });

    $('#RegisterPasswordShowHide a').on('click', function (event) {
        event.preventDefault();

        if ($('#RegisterPasswordShowHide input').attr('type') == 'text') {
            $('#RegisterPasswordShowHide input').attr('type', 'password');
            $('#RegisterPasswordShowHide i').addClass('bi-eye-slash');
            $('#RegisterPasswordShowHide i').removeClass('bi-eye');
        }
        else if ($('#RegisterPasswordShowHide input').attr('type') == 'password') {
            $('#RegisterPasswordShowHide input').attr('type', 'text');
            $('#RegisterPasswordShowHide i').removeClass('bi-eye-slash');
            $('#RegisterPasswordShowHide i').addClass('bi-eye');
        }
    });

    $('#NewPasswordShowHide a').on('click', function (event) {
        event.preventDefault();

        if ($('#NewPasswordShowHide input').attr('type') == 'text') {
            $('#NewPasswordShowHide input').attr('type', 'password');
            $('#NewPasswordShowHide i').addClass('bi-eye-slash');
            $('#NewPasswordShowHide i').removeClass('bi-eye');
        }
        else if ($('#NewPasswordShowHide input').attr('type') == 'password') {
            $('#NewPasswordShowHide input').attr('type', 'text');
            $('#NewPasswordShowHide i').removeClass('bi-eye-slash');
            $('#NewPasswordShowHide i').addClass('bi-eye');
        }
    });

    $('input[name="customRadioInline"]').on('change', function (event) {
        event.preventDefault();

        if ($(this).val() == 'Email') {
            $('#NewPasswordEmailShowHide').show();
            $('#NewPasswordPhoneShowHide').hide();
        }
        else {
            $('#NewPasswordPhoneShowHide').show();
            $('#NewPasswordEmailShowHide').hide();
        }
    })

    setTimeout(function () {
        $('.AccessoriesOutputsAlert, .GroceriesOutputsAlert').alert('close');
    }, 8000);
})
