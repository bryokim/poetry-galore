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

  $(".update-comment").on("click", function () {
    poemId = $(this).attr("data-poem-id");
    commentId = $(this).attr("data-comment-id");
    comment = $(`P#${commentId}`).text();

    $(`LI.comment-item P#${commentId}`).replaceWith(
      `<div id='${commentId}'>
      <input type="text" class="update-comment-input bg-body" id="${commentId}-1" value="${comment.trim()}">
      <button type="button" class="update-comment-button btn-outline-success" onclick="updateComment('${poemId}', '${commentId}', '${commentId}-1')" name="update">Save</button>
      </div>`
    );
  });
});

function updateComment(poemId, commentId, inputId) {
  newComment = $(`INPUT#${inputId}`).val();

  $.get(
    `http://127.0.0.1:5000/api/v1/poems/${poemId}/comments/${commentId}/update?text=${newComment.trim()}`,
    function (data) {
      console.log(data);
    }
  );

  $(`LI.comment-item DIV#${commentId}`).replaceWith(
    `<p
    class="text-secondary font-monospace mb-0"
    data-id="${commentId}"
    id="${commentId}"
  >
    ${newComment.trim()}
  </p>`
  );
}
