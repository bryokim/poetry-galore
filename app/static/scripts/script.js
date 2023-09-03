$(document).ready(function () {
  // $("TEXTAREA").on("input", function () {
  //   this.style.height = "auto";
  //   this.style.height = this.scrollHeight + "px";
  // });

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

  function searchByTheme(data) {
    return $.ajax({
      type: "POST",
      url: `http://127.0.0.1:5000/api/v1/search_by_theme`,
      data: data,
      headers: {
        "Content-Type": "application/json",
      },
      success: function (data) {
        for (let id of data) {
          $(`DIV#${id}`).hide();
        }
      },
    });
  }
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

      searchByTheme(
        `{"themeIds": ${JSON.stringify(
          selectedThemes
        )}, "poemIds": ${JSON.stringify(poemIds)}}`
      ).done(function (data) {
        for (let id of data) {
          $(`DIV#${id}`).hide();
        }
      });
    } else {
      selectedThemes = selectedThemes.filter((id) => id !== themeId);

      searchByTheme(
        `{"themeIds": ${JSON.stringify(
          selectedThemes
        )}, "poemIds": ${JSON.stringify(poemIds)}}`
      ).done(function (data) {
        validPoemIds = poemIds.filter((id) => !data.includes(id));
        for (let id of validPoemIds) {
          $(`DIV#${id}`).show();
        }
      });
    }
  });

  function checkValidity(url) {
    return new Promise((resolve, reject) => {
      $.ajax({
        url: url,
        type: "GET",
        success: function (data) {
          if (data.error) reject(data);
          else resolve(data);
        },
        error: function (error) {
          reject(error);
        },
      });
    });
  }

  $("INPUT#new-username-input").on("input", function () {
    newUsername = $(this).val();
    usernameInput = $(this);

    if (!newUsername || !newUsername.trim()) {
      usernameInput
        .removeClass("is-valid was-validated")
        .addClass("is-invalid");
    } else {
      checkValidity(`/api/v1/users/validate/username/${newUsername}`)
        .then((data) => {
          usernameInput
            .removeClass("is-valid was-validated")
            .addClass("is-invalid");
        })
        .catch((error) => {
          usernameInput
            .removeClass("is-invalid")
            .addClass("is-valid was-validated");
        });
    }
  });

  $("INPUT#new-username-input").on("blur", function () {
    if (!$(this).val()) {
      $(this).removeClass("is-valid is-invalid");
    }
  });

  $("BUTTON.update-username-btn").on("click", function (event) {
    if (!$("INPUT#new-username-input").hasClass("was-validated")) {
      event.preventDefault();
      event.stopPropagation();
    }
  });

  $("INPUT#new-email-input").on("input", function () {
    newEmail = $(this).val();
    emailInput = $(this);

    if (!newEmail || !newEmail.trim()) {
      emailInput.removeClass("is-valid was-validated").addClass("is-invalid");
    } else {
      checkValidity(`/api/v1/users/validate/email/${newEmail}`)
        .then((data) => {
          emailInput
            .removeClass("is-valid was-validated")
            .addClass("is-invalid");
        })
        .catch((error) => {
          emailInput
            .removeClass("is-invalid")
            .addClass("is-valid was-validated");
        });
    }
  });

  $("INPUT#new-email-input").on("blur", function () {
    if (!$(this).val()) {
      $(this).removeClass("is-valid is-invalid");
    }
  });

  $("BUTTON.update-email-btn").on("click", function (event) {
    if (!$("INPUT#new-email-input").hasClass("was-validated")) {
      event.preventDefault();
      event.stopPropagation();
    } else {
      $("INPUT#current-email").val($("INPUT#new-email-input").val());
    }
  });

  $("BUTTON.like-button").on("click", function (event) {
    poemId = $(this).attr("data-id");
    likeIcon = $(`#${poemId}-like`);
    likeCount = $(`SPAN#${poemId}-like-count`);

    likeIcon.toggleClass("fa-regular fa-solid");

    if (likeIcon.hasClass("fa-solid")) {
      $.get(`/api/v1/poems/${poemId}/like`, function (data) {
        console.log(data);
        likeCount.html(data.likes);
      }).done(function () {
        likeIcon.css("color", "#f20202");
      });
    } else {
      likeIcon.css("color", "");
      $.get(`/api/v1/poems/${poemId}/unlike`, function (data) {
        likeCount.html(data.likes);
      });
    }
  });

  // $("BUTTON.comment-button").on("click", function() {
  //   $.get()
  // })
});
