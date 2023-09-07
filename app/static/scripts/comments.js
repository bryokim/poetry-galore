$(document).ready(function () {
    /**
     * create a new input for updating the comment and update
     * the comment when user presses enter or clicks the save button.
     */
  $(".update-comment").on("click", function () {
    const poemId = $(this).attr("data-poem-id");
    const commentId = $(this).attr("data-comment-id");
    const comment = $(`P#${commentId}`).text();

    $(`LI.comment-item P#${commentId}`).replaceWith(
      `<div id='${commentId}'>
          <input type="text" class="update-comment-input bg-body" id="${commentId}-1" value="${comment.trim()}">
          <button type="button" class="update-comment-button btn-outline-success" name="update">Save</button>
          </div>`
    );

    $("BUTTON.update-comment-button").on("click", function () {
      let newComment = $(`INPUT#${commentId}-1`).val();

      $.get(
        `http://127.0.0.1:5000/poems/${poemId}/comments/${commentId}/update?text=${newComment.trim()}`
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
    });

    $(`INPUT#${commentId}-1`).on("keypress", function (event) {
      if (event.which === 13) {
        $("BUTTON.update-comment-button").trigger("click");
      }
    });
  });
});
