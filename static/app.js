$('form input[type="file"]').change(event => {
  let file = event.target.files;
  if (file.length === 0) {
    console.log('error')
  } else {
      if(file[0].type == 'image/jpeg') {
        $('img').remove();
        let img = $('<img class="img-fluid">');
        img.attr('src', window.URL.createObjectURL(file[0]));
        $('figure').prepend(img);
      } else {
        alert('File format not supported')
      }
  }
});