$(document).on('ready', function() {
    /* Nail thumb */
    $('.thumb-container').nailthumb()

    /* Modal gallery view */
    var $gallery        = $('.gallery')
        , $galleryModal = $('#gallery-modal')
        , $galleryImg   = $('#gallery-image')


    $gallery.on('click', 'img', function (e) {
        console.log($(this).attr('src')) 
        $galleryImg.attr('src', $(this)[0].src)
        $galleryModal.modal()
    })

    // register form confirm password validation
    var $pwd_confirm    = $('#password_confirm')
        , $pwd          = $('#password')
        , $reg_form     = $('#register_form')

    $reg_form.on('submit', function (e) {
        if ($pwd.val() !== $pwd_confirm.val()) {
            e.preventDefault()
            console.log('not the same')
            var flash_list = $('<ul/>', {'class': 'flashes'})
              , container = $('<div/>', {'class': 'container'})
            flash_list.append($("<li/>", {'class': 'error', 'text': "Passwords don't match"}))
            flash_list.appendTo(container)

            $('.page-wrap').prepend(container)
            return false
        }
    })

})
