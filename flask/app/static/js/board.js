//for dropdown menu
function dropdownFunction(){
    $(".dropdown").click(function() {
      $(this).find(".dropdown-menu").toggleClass("show");
    });

    // Close the dropdown menu when clicking outside of it
    $(document).click(function(e) {
      if (!$(e.target).closest('.dropdown').length) {
        $(".dropdown-menu").removeClass("show");
      }
    });
    $(".dropdown-item").click(function() {
      if ($(this).text().trim() === "Hide") {
        $(this).closest(".post").hide();
        $('.undo-hide').show();
      }
      if ($(this).text().trim() === "Delete") {
        $(this).closest(".post").hide();
        $('.undo-delete').show();
      }
      if ($(this).text().trim() === "Hired") {
        $('#no-hired').hide();
        $('#hired').show();
      }
    });
    $(".undo-text").click(function() {
      $(".post").show();
      $(".undo-hide").hide();
      $(".undo-delete").hide();
    });
    $(".close-back").click(function() {
      $(".undo-hide").hide();
      $(".undo-delete").hide();
    });

    //jQuery thailand
    $.Thailand({
        $district: $('#district'), // input ของตำบล
        $amphoe: $('#amphoe'), // input ของอำเภอ
        $province: $('#province'), // input ของจังหวัด
        $zipcode: $('#zipcode'), // input ของรหัสไปรษณีย์
    });
}

