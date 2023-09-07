$(document).ready(function () {
  /* Send request to server to check whether username or
   email is already registered. */
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

  // Check new username validity as user is typing and style the input accordingly.
  $("INPUT#new-username-input").on("input", function () {
    const newUsername = $(this).val();
    const usernameInput = $(this);

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

  // Remove validity styles if input is empty when it loses focus.
  $("INPUT#new-username-input").on("blur", function () {
    if (!$(this).val()) {
      $(this).removeClass("is-valid is-invalid");
    }
  });

  // Check new email validity as user is typing and style the input accordingly.
  $("INPUT#new-email-input").on("input", function () {
    const newEmail = $(this).val();
    const emailInput = $(this);

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

  // Remove validity styles if input is empty when it loses focus.
  $("INPUT#new-email-input").on("blur", function () {
    if (!$(this).val()) {
      $(this).removeClass("is-valid is-invalid");
    }
  });

  // Don't submit new details if any input is invalid or if the inputs are empty.
  $("BUTTON.update-user-btn").on("click", function (event) {
    const usernameInput = $("INPUT#new-username-input");
    const emailInput = $("INPUT#new-email-input");

    if (usernameInput.val() || emailInput.val()) {
      if (
        usernameInput.hasClass("is-invalid") ||
        emailInput.hasClass("is-invalid")
      ) {
        event.preventDefault();
        event.stopPropagation();
      }
    } else {
      event.preventDefault();
      event.stopPropagation();
    }
  });
});
