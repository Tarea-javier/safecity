// Contenido completo para static/js/login.js

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (!loginForm) return;

    loginForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const errorMessage = document.getElementById('error-message');
        
        errorMessage.textContent = '';

        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        try {
            const response = await fetch('/token', {
                method: 'POST',
                body: formData,
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });

            // --- Cambio Clave: Solo verificamos si la respuesta fue exitosa ---
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Login failed. Please check your credentials.');
            }
            
            // Si la respuesta es OK (2xx), el servidor ya estableció la cookie.
            // Simplemente redirigimos al mapa.
            window.location.href = '/map';

        } catch (error) {
            errorMessage.textContent = error.message;
        }
    });
});