function resend() {
    var $fig = $('figure'),
        // $embed = $fig.find('embed'),
        type = $('#type').val(),
        data = $('#data').val(),
        style = $('#style').val(),
        opts = {};
    $('.c-opts').each(function() {
        var $this = $(this),
            val = $this.val();
        if(val) {
            opts[$this.attr('id').replace('c-', '')] = val;
        }
    });
    $.ajax({
        url: '/svg',
        type: 'POST',
        data: {
            type: type,
            style: style,
            vals: '{' + data + '}',
            opts: JSON.stringify(opts)
        },
        dataType: 'html'
    }).done(function (data) {
        $fig.find('svg').remove();
        $fig.prepend(data);
        $('textarea').css({'-webkit-box-shadow': ''});
    }).fail(function () {
        $('textarea').css({'-webkit-box-shadow': 'inset 0 1px 1px rgba(0, 0, 0, 0.075), 0 0 8px rgba(255, 0, 0, 0.6)'});
    });

    // $embed.remove();
    // $fig.prepend(
    //     $('<embed>')
    //         .attr({
    //             src: src,
    //             type: 'image/svg+xml'
    //         })
    // );
}

$(function () {
    $('figure figcaption').append(
        $('<button>')
            .text('⟳')
            .click(function() {
                var $fig, $embed, w, h, src;
                $fig = $(this).closest('figure');
                $embed = $fig.find('embed');
                w = $embed.width();
                h = $embed.height();
                src = $embed.attr('src');
                $embed.remove();
                $fig.prepend(
                    $('<embed>')
                        .attr({
                            src: src,
                            type: 'image/svg+xml',
                            width: w,
                            height: h
                        })
                );
            })
    );
    $('#type').on('change', resend);
    $('#data').on('input', resend);
    $('#style').on('change', resend);
    $('.c-opts').on('input', resend);
    resend();
});
