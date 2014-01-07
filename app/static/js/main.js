$(document).on('ready', function() {

    /* Nail thumb */
    $('.gallery-container').nailthumb()
    $('#avatar-container').nailthumb({width: 325, height: 300})
    /* Gallery init and config */
    $.Elastislide.defaults = {
        orientation: 'horizontal', 
        minItems: 3,
        start: 0,
        easing: 'ease-in-out',
        onClick: function (el, position, evt) { return false },
        onReady: function () { return false },
        onBeforeSlide: function () { return false },
        onAfterSlide: function () { return false }
    }

    $gallery = $('#elastigallery') 
    $gallery_view = $('#gallery-view')

    $gallery.elastislide()

    $gallery.on('click', function (e) { 
            console.log(e.target)
            $gallery_view.find('img').attr({src: e.target.src})
    })

    // turn the profile section headers blue on hover and click
    var $profile_header = $('.profile-header h3')
        , mover_color = '#3DAA98'

    $profile_header.mouseenter( function(e) {
        $(this).css({'background-color': mover_color})
    }).mouseleave(function(e) {
        $(this).css({'background-color': ''})
    })

    $profile_header.click(function(e) {
        console.log(e.target)
        $(this).toggleClass('active')
    })

    // placeholder text on index search form
    var selectors = [$('#service'), $('#zip_code')]

    // on focus, set value to ''
    for (var i = 0; i < selectors.length; i++) {
        selectors[i].val(selectors[i].data('placeholder'))

        selectors[i].focusin(function () {
            $(this).val('')
            console.log('focus in')
        }).focusout(function () {
            console.log($(this).val())
            if ($(this).val() === '') {
                $(this).val($(this).data('placeholder'))
                console.log('focus out')
            }
        })
    }

    // register form confirm password validation
    var $pwd_confirm    = $('#password_confirm')
        , $pwd          = $('#password')
        , $reg_form     = $('#register_form')

    $reg_form.on('submit', function (e) {
        if ($pwd.val() !== $pwd_confirm.val()) {
            console.log('not the same')
            return false
        }
    })

})

