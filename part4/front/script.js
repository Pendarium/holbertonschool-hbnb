document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Empêche le rechargement de la page

            // Récupérer les valeurs du formulaire
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                // Requête POST vers l'API login
                const response = await fetch('http://localhost:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    const token = data.access_token; // ou data.token selon ton API

                    // Stocker le JWT dans un cookie
                    document.cookie = `token=${token}; path=/`;

                    // Rediriger vers la page principale
                    window.location.href = 'index.html';
                } else {
                    // Si login échoue
                    alert('Login failed: ' + response.statusText);
                }
            } catch (error) {
                // Gestion des erreurs réseau
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }
});
