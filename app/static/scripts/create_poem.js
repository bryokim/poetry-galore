$(document).ready(function () {
  $("BUTTON#next-btn").on("click", function (e) {
    if (!$("INPUT#title").val() || $("INPUT#title").val().length < 3) {
      e.stopPropagation();
      e.preventDefault();

      $("INPUT#title").addClass("is-invalid");
    } else if (
      !$("TEXTAREA#poem_body").val() ||
      $("TEXTAREA#poem_body").val().length < 3
    ) {
      e.stopPropagation();
      e.preventDefault();

      $("INPUT#title").removeClass("is-invalid");
      $("TEXTAREA#poem_body").addClass("is-invalid");
    } else {
      $("INPUT#title").removeClass("is-invalid");
      $("TEXTAREA#poem_body").removeClass("is-invalid");

      $("DIV.first-page").hide();
      $("DIV.second-page").removeClass("d-none");
      $("BUTTON#prev-btn").removeClass("d-none");
      $("BUTTON#post-btn").removeClass("d-none");
      $("BUTTON#next-btn").hide();
    }
  });

  $("BUTTON#prev-btn").on("click", function () {
    $("DIV.first-page").show();
    $("DIV.second-page").addClass("d-none");
    $("BUTTON#prev-btn").addClass("d-none");
    $("BUTTON#post-btn").addClass("d-none");
    $("BUTTON#next-btn").show();
  });

  $("DIV.theme-checkbox").on(
    "change",
    'input[type="checkbox"]',
    function (event) {
      const themesInput = $("INPUT#themes");
      const selectedThemes = themesInput.val();

      if ($(this)[0].checked) {
        if (selectedThemes && selectedThemes.endsWith(",")) {
          themesInput.val(`${selectedThemes} ${$(this).val()}`);
        } else if (selectedThemes && selectedThemes.endsWith(", ")) {
          themesInput.val(`${selectedThemes}${$(this).val()}`);
        } else if (selectedThemes) {
          themesInput.val(`${selectedThemes}, ${$(this).val()}`);
        } else {
          themesInput.val(`${$(this).val()}`);
        }
      } else {
        let newText = themesInput
          .val()
          .replaceAll(new RegExp(`\\b(${$(this).val()}(, *)?)\\b`, "g"), "");

        newText = newText.endsWith(", ")
          ? newText.substring(0, newText.length - 2)
          : newText;

        themesInput.val(newText);
      }
      event.stopPropagation();
    }
  );

  const selectedCategory = $("SELECT").attr("data-selected");
  Array.from($("OPTION")).forEach((option) => {
    if (option.value === selectedCategory) {
      option.selected = true;
    }
  });

  const themes = $("INPUT#themes").val().split(", ");
  Array.from($("INPUT.form-check-input")).forEach((input) => {
    if (themes.includes(input.value)) {
      input.checked = true;
    }
  });

  $("BUTTON#poem-load-btn").on("click", function (event) {
    $("INPUT#poem-file").trigger("click");
  });

  $("INPUT#poem-file").on("change", function (event) {
    const reader = new FileReader();
    const file = event.target.files[0];

    reader.addEventListener("load", (event) => {
      const result = event.target.result;
      $("TEXTAREA#poem_body").val(result);
      $("INPUT#title").val(file.name);
    });

    let allowedExtensions = /(\.doc|\.txt)$/i;
    let allowedSize = 1_000_000;

    if (file && !allowedExtensions.exec(file.name)) {
      alert("Invalid file type");
      return;
    }
    if (file && file.size > allowedSize) {
      alert("Big file");
      return;
    }
    reader.readAsText(file);
  });

  $("#show-create-category").on("click", (event) => {
    $("DIV#create-category-container").removeClass("d-none");
    event.stopPropagation();
    event.preventDefault();
  });

  function createCategory(data) {
    return new Promise((resolve, reject) => {
      $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/api/v1/categories",
        data: data,
        headers: {
          "Content-Type": "application/json",
        },
        success: function (data) {
          resolve(data);
        },
        error: function (error) {
          reject(error);
        },
      });
    });
  }

  $("BUTTON#create-category").on("click", (event) => {
    const name = $("INPUT#new-category").val();

    createCategory(`{ "name": "${name}" }`)
      .then((data) => {
        $("SELECT#category").append(
          `<option value=${name} id="${name}-1">${name}</option>`
        );
        $(`OPTION#${name}-1`)[0].selected = true;
      })
      .catch((error) => {
        console.log(error.responseJSON.error);
      });

    $("DIV#create-category-container").addClass("d-none");
  });

  $(`INPUT#new-category`).on("keypress", function (event) {
    if (event.which === 13) {
      $("BUTTON#create-category").trigger("click");
      event.stopPropagation();
      event.preventDefault();
    }
  });
});
