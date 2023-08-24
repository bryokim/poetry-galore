$(document).ready(function () {
  $("TEXTAREA").on("input", function () {
    this.style.height = "auto";

    this.style.height = this.scrollHeight + "px";
  });

  $(".toggle-password").click(function () {
    $(this).toggleClass("fa-eye fa-eye-slash");
    var input = $($(this).attr("toggle"));
    if (input.attr("type") == "password") {
      input.attr("type", "text");
    } else {
      input.attr("type", "password");
    }
  });
});
