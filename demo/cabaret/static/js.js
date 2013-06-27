function resend() {
    var $fig = $('figure'),
        type = $('#type').val(),
        style = $('#style').val(),
        interpolation = $('#interpolation').val(),
        opts = {},
        vals = [];
    $('.c-opts').each(function() {
        var $this = $(this),
            val = $this.val();
        if($this.attr('type') == 'checkbox') {
            opts[$this.attr('id').replace('c-', '')] = $this.is(":checked");
        } else if(val) {
            opts[$this.attr('id').replace('c-', '')] = val;
        }
    });
    if(interpolation) {
        opts.interpolate = interpolation;
    }
    $('.data .controls').each(function () {
        var label = $(this).find('.serie-label').val(),
            values = $(this).find('.serie-value').val(),
            lst = [label, values.split(',').map(function (v) { return parseFloat(v); })];
        if (values !== '') {
            vals.push(lst);
        }
    });
    var t = new Date().getTime();
    $.ajax({
        url: '/svg',
        type: 'POST',
        data: {
            type: type,
            style: style,
            vals: JSON.stringify({vals: vals}),
            opts: JSON.stringify(opts)
        },
        dataType: 'json',
        traditional: true
    }).done(function (data) {
        $('.total-time').html('<label>Total time: </label>' +  (new Date().getTime() - t) + 'ms');
        $('.server-time').html('<label>Generation time:</label> ' + data.time + 'ms');
        // $fig.find('div').get(0).innerHTML = data;
        $fig.find('div').html(data.svg);
        init_svg($fig.find('svg').get(0));
        $('.nav a').css({color: ''});
    }).fail(function () {
        $('.nav a').css({color: 'red'});
    });
}

$(function () {
    $('#type').add('#style').add('#interpolation').on('change', resend);
    $('#data').on('input', resend);
    $('.c-opts:not([type=checkbox])').on('input', resend);
    $('.c-opts[type=checkbox]').on('change', resend);
    $('div.tt').tooltip({ placement: 'top' });
    $('.control-group.data').on('click keypress', '.btn.rem', function () {
        if($('.data .controls').length > 1) {
            $(this).closest('.controls').remove();
        }
    });
    $('.control-group.data').on('click keypress', '.btn.add', function () {
        $(this).siblings('.controls').last().clone().insertBefore($(this)).find('input').val('');
    });
    $('.control-group.data').on('input', 'input', resend);
    resend();
});
