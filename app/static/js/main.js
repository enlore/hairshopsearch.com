$(document).on('ready', function() {
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

    var $ph_masque = $('#sticker-masque')
        ,$jumbotron = $('#profile-jumbotron')
        ,jumbotron_bottom = $jumbotron.height() + $jumbotron.offset().top

        $(window).scroll(function(e) {
            var sticker_bottom_edge = $sticker.offset().top + $sticker.width()
                ,masque_width = $sticker.width() - (sticker_bottom_edge - jumbotron_bottom - 30)

            if ( sticker_bottom_edge >= (jumbotron_bottom + 30)) {
                $ph_masque.css({
                    'width': masque_width
                })
                console.log(masque_width)
            }

            if ( sticker_bottom_edge < (jumbotron_bottom + 30 )) {
                $ph_masque.css({'width': $sticker.width() + 20})
            }
        })

})
