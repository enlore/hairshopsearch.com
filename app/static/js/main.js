$(document).on('ready', function() {

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

    /* AWS S3 Upload */
    var aws_stuff = {}
    $.ajax({
        url: '/dashboard/photo/save',
        type: 'GET',
    }).done(function (res, stat, jqxhr) {
        aws_stuff.s3_url = res.s3_url
        aws_stuff.policy_64 = res.policy_64
        aws_stuff.aws_key = res.aws_key
        aws_stuff.signature = res.signature

        if (window.FormData)
            fd = new FormData()

        if (fd) {
            fd.append('awsaccesskeyid', aws_stuff.aws_key)
            fd.append('signature', aws_stuff.signature)
            fd.append('policy', aws_stuff.policy_64)
            fd.append('key', 'uploads/${filename}')
            fd.append('acl', 'public-read')
            fd.append('Content-Type', '')
        }

        /* jquery file uploader */
        if (!window.fileupload)
            console.log('No jQuery File Upload')
        else {
            // initialize the uploader
            $('#fileupload').fileupload({
                // ajax style options
                url: aws_stuff.s3_url,
                formData: fd,
                dataType: 'json',
                type: 'POST',
                done: function (e, resp) {
                    // on success, post the s3 key to our app
                    $.ajax({
                            url: '/dashboard/photo/save', 
                            type: 'POST',
                            headers: {'X-CSRFToken': $('meta[name="csrf"]').attr('content')},
                            data: {filename: resp.files[0].name},
                            done: function (res, stat, jqxhr) {
                                console.log('posted!')
                                window.location.reload(true)
                            },
                            always: function (res, stat, jqhxr) { console.log('well something happened') }
                    })
                },
                always: function (evt, resp) { console.log(arguments) }
            })
        }
    }).fail(function (res, stat, jqxhr) {
            console.log(res, stat)
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

