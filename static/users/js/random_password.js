document.addEventListener('DOMContentLoaded', function () {
    const passwordInput1 = document.getElementById('id_password1');
    const passwordInput2 = document.getElementById('id_password2');

    if (passwordInput1 && passwordInput2) {
        const generateBtn = document.createElement('button');
        generateBtn.type = 'button';
        generateBtn.textContent = 'Generate Password';
        generateBtn.className = 'button';
        generateBtn.style.marginLeft = '10px';

        // Insert after the first password field's help text or the field itself
        const helpText = passwordInput1.nextElementSibling;
        if (helpText && helpText.classList.contains('help')) {
            helpText.parentNode.insertBefore(generateBtn, helpText.nextSibling);
        } else {
            passwordInput1.parentNode.insertBefore(generateBtn, passwordInput1.nextSibling);
        }

        generateBtn.addEventListener('click', function () {
            const length = 16;
            const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+";
            let password = "";
            for (let i = 0, n = charset.length; i < length; ++i) {
                password += charset.charAt(Math.floor(Math.random() * n));
            }

            passwordInput1.value = password;
            passwordInput2.value = password;

            // Temporarily show the password so it can be copied
            passwordInput1.type = 'text';
            passwordInput2.type = 'text';

            // Optional: revert back to password type after some time or on blur, 
            // but keeping it visible is usually better for "Generate" flow so they can copy it.
            // We can add a small note or alert.
            alert(`Generated password: ${password}`);
        });
    }
});
