$(document).on('ready', function() {
        /* Ink File Picker */
        filepicker.setKey('ATqxZ7zONQgaSqWFtAAFOz')

        var store_options = {}
            ,picker_options = {}

        store_options.location = "S3"

        /* pick and store a bunch */
        $('#pick-files').click(function() {
            filepicker.pickMultiple(picker_options, function(InkBlobs) {
                for (var j=0; j < InkBlobs.length; j++) {
                    console.log('multi: ' + InkBlobs[j].url)

                    filepicker.store(InkBlobs[j],
                        function (InkBlob) {
                            console.log('stored: ' + InkBlob.filename)
                            console.log('s3 key: ' + InkBlob.key)

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


        /* pick and store a one */
        $('#pick-one').click(function () {
            filepicker.pickAndStore(picker_options, store_options,
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
                    ,function (FPError) {
                        console.log(FPError)
                    })
        })

    var $sticker = $("#left-sticker")
        ,x = $sticker.offset().left

        $sticker.css({'left': -x - 1 })

    var $profile_header = $('.profile-header h3'),
        mover_color = '#3DAA98'

        $profile_header.mouseenter( function(e) {
            $(this).css({'background-color': mover_color})
        }).mouseleave(function(e) {
            $(this).css({'background-color': ''})
        })

    var $profile_content = $('.profile-content')

    $profile_header.click(function(e) {
        console.log(e.target)
        $(this).toggleClass('active')
    })
})
