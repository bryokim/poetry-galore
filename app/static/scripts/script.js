$(document).ready(function () {
  $("TEXTAREA").on("input", function () {
    this.style.height = "auto";
    this.style.height = this.scrollHeight + "px";
  });

  $(".toggle-password").click(function () {
    $(this).toggleClass("fa-eye fa-eye-slash");
    let input = $($(this).attr("toggle"));
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
      <button type="button" class="update-comment-button btn-outline-success" name="update">Save</button>
      </div>`
    );

    $("BUTTON.update-comment-button").on("click", function () {
      newComment = $(`INPUT#${commentId}-1`).val();

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
    });

    $(`INPUT#${commentId}-1`).on("keypress", function (event) {
      if (event.which === 13) {
        $("BUTTON.update-comment-button").trigger("click");
      }
    });
  });

  selectedThemes = [];

  $(".theme-btn").on("click", function () {
    $(this).toggleClass("active");
    themeId = $(this).attr("id");

    poemIds = [];
    for (const element of $("DIV.poem-container")) {
      poemIds.push(element.getAttribute("id"));
    }

    if ($(this).hasClass("active")) {
      selectedThemes.push(themeId);

      $.ajax({
        type: "POST",
        url: `http://127.0.0.1:5000/api/v1/search_by_theme`,
        data: `{"themeIds": ${JSON.stringify(
          selectedThemes
        )}, "poemIds": ${JSON.stringify(poemIds)}}`,
        headers: {
          "Content-Type": "application/json",
        },
        success: function (data) {
          for (let id of data) {
            $(`DIV#${id}`).hide();
          }
        },
      });
    } else {
      selectedThemes = selectedThemes.filter((id) => id !== themeId);

      $.ajax({
        type: "POST",
        url: `http://127.0.0.1:5000/api/v1/search_by_theme`,
        data: `{"themeIds": ${JSON.stringify(
          selectedThemes
        )}, "poemIds": ${JSON.stringify(poemIds)}}`,
        headers: {
          "Content-Type": "application/json",
        },
        success: function (data) {
          validPoemIds = poemIds.filter((id) => !data.includes(id));
          for (let id of validPoemIds) {
            $(`DIV#${id}`).show();
          }
        },
      });
    }
  });
});
