  var button = document.getElementById('order');
  if (document.getElementsByClassName('Type2').length > 0) {
    button.disabled = true;
  } else {
    button.disabled = false;
  }
