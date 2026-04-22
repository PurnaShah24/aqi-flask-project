function showInlineError(input, message) {
    input.setCustomValidity(message);
    input.reportValidity();
}

function clearInlineError(input) {
    input.setCustomValidity("");
}

const loginForm = document.getElementById("loginForm");
if (loginForm) {
    loginForm.addEventListener("submit", function (event) {
        const username = document.getElementById("username");
        const password = document.getElementById("password");
        clearInlineError(username);
        clearInlineError(password);

        if (username.value.trim().length < 2) {
            event.preventDefault();
            showInlineError(username, "Username must be at least 2 characters.");
            return;
        }

        if (password.value.trim().length < 4) {
            event.preventDefault();
            showInlineError(password, "Password must be at least 4 characters.");
        }
    });
}

const analysisForm = document.getElementById("analysisForm");
if (analysisForm) {
    analysisForm.addEventListener("submit", function (event) {
        const testSizeInput = document.getElementById("test_size");
        clearInlineError(testSizeInput);
        const value = parseFloat(testSizeInput.value);

        if (Number.isNaN(value) || value < 0.1 || value > 0.4) {
            event.preventDefault();
            showInlineError(testSizeInput, "Enter a value between 0.1 and 0.4.");
        }
    });
}
