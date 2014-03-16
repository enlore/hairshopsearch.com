$(document).on('ready', function () {
    /* Nail thumb */
    $('.thumb-container').nailthumb()


    /* Modal gallery view */
    var $gallery        = $('.gallery')
        , $galleryModal = $('#gallery-modal')
        , $galleryImg   = $('#gallery-image')
        , $galleryNext  = $('#gallery-next')
        , $galleryPrev  = $('#gallery-prev')

    $gallery.on('click', 'img', function (e) {
        $nextImg = $(this).parents('.col-sm-3').next().find('img')
        $galleryNext.data('next', $nextImg.attr('src'))

        $galleryPrev.data('prev', $(this).parents('.col-sm-3').prev().find('img').attr('src'))
        $galleryImg.attr('src', $(this).attr('src'))

        $galleryModal.modal()
    })

    $galleryNext.on('click', function (e) {
        console.log(e)
    })

    $galleryPrev.on('click', function (e) {
        console.log(e) 
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
