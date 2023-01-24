function previewFile() {
  const preview = document.getElementById('preview');
  const file = document.getElementById("finput").files[0];
  const reader = new FileReader();

  reader.addEventListener("load", () => {
    // convert image file to base64 string
    preview.src = reader.result;
  }, false);

  if (file) {
    reader.readAsDataURL(file);
  }
}