 $(document).ready(function() {

      let price = parseFloat($(this).find('#price').text().replace('$', ''));
      let qty = parseInt($(this).find('#qty').text());
      let result = price * qty;
      $(this).find('.result').text('$' + result.toFixed(2));

  });
