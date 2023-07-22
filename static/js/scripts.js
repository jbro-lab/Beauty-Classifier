/*!
 * Start Bootstrap - Personal v1.0.1 (https://startbootstrap.com/template-overviews/personal)
 * Copyright 2013-2023 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-personal/blob/master/LICENSE)
 */
// This file is intentionally blank
// Use this file to add JavaScript to your project
// Get references to the input element and image preview element
const imageInput = document.getElementById("img");
const imagePreview = document.getElementById("imagePreview");

// Add an event listener to the input element
imageInput.addEventListener("change", function () {
  // Check if any file is selected
  if (imageInput.files && imageInput.files[0]) {
    // Get the selected file
    const selectedFile = imageInput.files[0];

    // Create a FileReader object
    const reader = new FileReader();

    // Set up the FileReader onload event
    reader.onload = function (e) {
      // Set the source of the image preview to the selected file's data URL
      imagePreview.src = e.target.result;
    };

    // Read the selected file as a data URL
    reader.readAsDataURL(selectedFile);
  }
});
