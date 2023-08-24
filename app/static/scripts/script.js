$(document).ready(function () {
  $("TEXTAREA").on("input", function () {
    this.style.height = "auto";

    this.style.height = this.scrollHeight + "px";
  });
});
