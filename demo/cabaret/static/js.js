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
        if($this.attr('type') == 'checkbox') {
            val = $this.is(":checked");
        }
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
        // $fig.find('div').get(0).innerHTML = data;
        $fig.find('div').html(data);
        init_svg($fig.find('svg').get(0));
        $('textarea').css({'-webkit-box-shadow': ''});
    }).fail(function () {
        $('textarea').css({'-webkit-box-shadow': 'inset 0 1px 1px rgba(0, 0, 0, 0.075), 0 0 8px rgba(255, 0, 0, 0.6)'});
    });
}

$(function () {
    $('#type').on('change', resend);
    $('#data').on('input', resend);
    $('#style').on('change', resend);
    $('.c-opts:not([type=checkbox])').on('input', resend);
    $('.c-opts[type=checkbox]').on('change', resend);
    $('label.tt').tooltip({ placement: 'right' });
    $('input.tt').tooltip({ placement: 'top' });
    resend();
});
