$(document).on('ready', function() {

    $.Elastislide.defaults = {
        orientation: 'horizontal', 
        minItems: 5,
        start: 0,
        easing: 'ease-in-out',
        onClick: function (el, position, evt) { return false },
        onReady: function () { return false },
        onBeforeSlide: function () { return false },
        onAfterSlide: function () { return false }
    }
    $('#elastigallery').elastislide()

    /* blah */
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
            fd.append('success_action_redirect', 'http://localhost:9016/dashboard/profile')
        }

        /* jquery file uploader */
        if (!window.fileupload)
            console.log('No jQuery File Upload')
        else {
            //var csrf_token = $('meta[name="csrf"]').attr('content')
            $('#fileupload').fileupload({
                url: aws_stuff.s3_url,
                formData: fd,
                dataType: 'json',
                type: 'POST',
                //headers: {'X-CSRFToken': csrf_token},
                done: function (e, data) {
                    console.log(typeof(e))
                },
                always: function (evt, resp) {
                    console.log(resp.jqXHR.getResponseHeader('location'))
                }
            })
        }
    }).fail(function (res, stat, jqxhr) {
        console.log(stat)
    })

    var $avatar_upload_form = $('#upload-avatar')

    $avatar_upload_form.on('submit', function (e) {
        e.preventDefault()
        var csrf_token = $('meta[name="csrf"]').attr('content')
        // send image data to amazon and retain key on success
        $.ajax({
            url     : aws_stuff.s3_url,
            type    : 'POST',
            data    : $avatar_upload_form.balls
        })

        // send new s3 key to our app
        $.ajax({
            url     : '/dashboard/photo/save',
            headers : {'X-CSRFToken': csrf_token},
            type: 'post',
            data: { payload: 'BUTTS BUTTS BUTTS'}
        }).done(function (response, textStatus, jqXHR) {
            console.log(textStatus)
        }).fail(function (response, textStatus, jqXHR) {
            console.log(textStatus)
        }).always(function (response, textStatus, jqXHR) {
            console.log('always cb status code: %s', textStatus)
        })

        console.log('post ajax')
    })

        /* Ink File Picker */
        /*
        filepicker.setKey('ATqxZ7zONQgaSqWFtAAFOz')

        var store_options = {}
            , picker_options = {}

        store_options.location = "S3"

        $('#pick-files').click(function() {
            filepicker.pickMultiple(picker_options, function(InkBlobs) {
                for (var j=0; j < InkBlobs.length; j++) {
                    console.log('multi: ' + InkBlobs[j].url)

                    filepicker.store(InkBlobs[j],
                        function (InkBlob) {
                            console.log('s3 key: ' + InkBlob.key)

                            var csrf_token = $('meta[name="csrf"]').attr('content')
                            $.ajax({
                                url     : '/dashboard/gallery/photo/save',
                                headers : {'X-CSRFToken': csrf_token},
                                type: 'post',
                                data: { photo_key: InkBlob.key }
                            }).done(function (response, textStatus, jqXHR) {
                                console.log(response)

                            }).fail(function (response, textStatus, jqXHR) {
                                console.log(response)
                            })

                        },
                        function (FPError) {
                            console.log('oh shit: ' + FPError)
                        },
                        function (progress) {
                            console.log(progress + '% complete!')
                        })
                }
            })
        })


        $('#pick-one').click(function () {
            filepicker.pickAndStore(picker_options, store_options,
                    // fp pickAndStore callback
                    function (InkBlobs) {
                        console.log(JSON.stringify(InkBlobs))

                        var csrf_token = $('meta[name="csrf"]').attr('content')
                        for (var i=0; i < InkBlobs.length; i++) {
                            request = $.ajax({
                                url: '/dashboard/photo/save',
                                headers: { 'X-CSRFToken': csrf_token },
                                type: 'post',
                                data: { photo_key: InkBlobs[i].key }
                            })

                            request.done(function (response, textStatus, jqXHR) {
                                console.log(response.status)
                                console.log(textStatus)
                            })

                            request.fail(function (response, textStatus, jqXHR) {
                                console.log(response.status)
                                console.log(textStatus)
                            })
                        }
                    }
                    // fp on error callback
                    , function (FPError) {
                        console.log(FPError)
                    })
        })
    */

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

