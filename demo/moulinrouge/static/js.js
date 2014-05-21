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
    }),
    $('<button>')
    .text('📄')
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
          src: src.replace('/svg/', '/table/'),
          type: 'text/html',
          width: w,
          height: h
        })
      );
    }),
    $('<button>')
    .text('📈')
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
          src: src.replace('/table/', '/svg/'),
          type: 'text/html',
          width: w,
          height: h
        })
      );
    })
  );
});
