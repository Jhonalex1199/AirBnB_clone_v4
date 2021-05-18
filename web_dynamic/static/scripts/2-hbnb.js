$(document).ready(function () {
    const amenities = {};
    $('input:checkbox').change(function () {
      if ($(this).is(':checked')) {
        amenities[$(this).data('id')] = $(this).data('name');
      } else {
        delete amenities[$(this).data('id')];
      }
      let tex = '';
      if (!(Object.values(amenities).length)) {
        $('.amenities h4').replaceWith('<h4>&nbsp;</h4>');
      } else {
        tex = Object.values(amenities).join(', ');
        $('.amenities h4').html(tex);
      }
    });

    $.ajax({
        url: 'http://localhost:5001/api/v1/status/',
        success: function (data) {
        console.log(data);
          if (data.status === 'OK') {
            $('div#api_status').addClass('available');
          } else {
            $('div#api_status').removeClass('available');
          }
        },
        error: function (error) {
          console.log('error', error);
        }
      });
  });
