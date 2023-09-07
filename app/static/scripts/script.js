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

  // Request for poems not matching the selected theme.
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
  let selectedThemes = [];

  // Hide the invalid poems when a theme is selected.
  // When a theme is unselected, show poems matching remaining themes.
  $(".theme-btn").on("click", function () {
    $(this).toggleClass("active");
    const themeId = $(this).attr("id");

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

  $("BUTTON.like-button").on("click", function (event) {
    const poemId = $(this).attr("data-id");
    const likeIcon = $(`#${poemId}-like`);
    const likeCount = $(`SPAN#${poemId}-like-count`);

    if (likeIcon.hasClass("fa-regular")) {
      $.get(`/api/v1/poems/${poemId}/like`, function (data) {
        likeCount.html(data.likes);
        likeIcon.removeClass("fa-regular").addClass("fa-solid");
        likeIcon.css("color", "#f20202");
      });
    } else {
      likeIcon.css("color", "");
      $.get(`/api/v1/poems/${poemId}/unlike`, function (data) {
        likeCount.html(data.likes);
        likeIcon.removeClass("fa-solid").addClass("fa-regular");
      });
    }
  });

  // $("BUTTON.comment-button").on("click", function() {
  //   $.get()
  // })
});
