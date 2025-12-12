/* ---------------------- BASE URL ---------------------- */
const BASE_URL = (() => {
  if (window.location.port && window.location.port !== "5000") {
    return "http://127.0.0.1:5000";
  }
  return ""; // backend sur même serveur/port
})();

/* ---------------------- UTILS ---------------------- */
// Décoder un JWT côté frontend
function parseJwt(token) {
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch (e) {
    return null;
  }
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("place_id");
}

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const priceFilter = document.getElementById("price-filter");
  const reviewForm = document.getElementById("review-form");

  /* ------------------------------
        GESTION LOGIN FORM
  ------------------------------ */
  if (loginForm) loginForm.addEventListener('submit', loginUser);

  /* ------------------------------
        INIT FILTRE PRIX
  ------------------------------ */
  if (priceFilter) {
    priceFilter.innerHTML = `
      <option value="All">All</option>
      <option value="10">10</option>
      <option value="50">50</option>
      <option value="100">100</option>
    `;
    priceFilter.addEventListener("change", filterPlaces);
  }

  /* ------------------------------
        FORM REVIEW
  ------------------------------ */
  if (reviewForm) reviewForm.addEventListener("submit", submitReview);

  /* ------------------------------
        AUTHENTIFICATION + FETCH
  ------------------------------ */
  checkAuthentication();
});

/* ----------------------------- LOGIN ----------------------------- */
async function loginUser(event) {
  event.preventDefault();
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  try {
    const response = await fetch(`${BASE_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem("token", data.access_token);

      // Décoder le token pour récupérer l'ID utilisateur
      const payload = parseJwt(data.access_token);
      if (payload && payload.sub) {
        localStorage.setItem("user_id", payload.sub);
        localStorage.setItem("user_name", payload.name || "Utilisateur");
      } else {
        console.error("Impossible de récupérer l'ID utilisateur depuis le token");
      }

      window.location.href = "index.html";
    } else {
      alert('Échec de la connexion : vérifiez vos identifiants');
    }
  } catch (error) {
    console.error('Erreur lors du login:', error);
    alert('Une erreur est survenue. Veuillez réessayer.');
  }
}

/* ----------------------------- AUTHENTIFICATION ----------------------------- */
function checkAuthentication() {
  const token = localStorage.getItem("token");
  const userId = localStorage.getItem("user_id");
  const authButton = document.querySelector(".login-button");

  if (!authButton) return;

  const reviewSection = document.getElementById("add-review");

  if (token && userId) {
    authButton.textContent = "Déconnexion";
    authButton.href = "#";
    authButton.addEventListener("click", (e) => {
      e.preventDefault();
      localStorage.removeItem("token");
      localStorage.removeItem("user_id");
      localStorage.removeItem("user_name");
      location.reload();
    });

    if (reviewSection) reviewSection.style.display = "block";
  } else {
    authButton.textContent = "Login";
    authButton.href = "login.html";

    if (reviewSection) reviewSection.style.display = "none";
  }

  // FETCH DATA
  if (document.getElementById("places-list")) fetchPlaces(token);
  if (document.getElementById("place-details")) {
    const placeId = getPlaceIdFromURL();
    fetchPlaceDetails(placeId, token);
    fetchPlaceReviews(placeId, token);
  }
}

/* ----------------------------- FETCH PLACES ----------------------------- */
async function fetchPlaces(token) {
  try {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await fetch(`${BASE_URL}/api/v1/places/`, { headers });

    if (!response.ok) {
      document.getElementById("places-list").innerHTML = "<p>Impossible de charger les places.</p>";
      return;
    }

    const places = await response.json();
    displayPlaces(places);
  } catch (err) {
    console.error("Erreur réseau lors du fetch des places:", err);
    document.getElementById("places-list").innerHTML = "<p>Impossible de charger les places.</p>";
  }
}

/* ----------------------------- DISPLAY PLACES ----------------------------- */
function displayPlaces(places) {
  const list = document.getElementById("places-list");
  if (!list) return;

  list.innerHTML = "";
  places.forEach(place => {
    const card = document.createElement("div");
    card.className = "place-card";
    card.dataset.price = place.price;

    card.innerHTML = `
      <div class="card-header">
        <h3><a href="place.html?place_id=${place.id}">${place.title}</a></h3>
        <span class="price">${place.price} € / nuit</span>
      </div>
      <p class="description">${place.description || "Pas de description"}</p>
      <a href="place.html?place_id=${place.id}" class="details-button">Voir le lieu</a>
    `;

    list.appendChild(card);
  });
}

/* ----------------------------- FILTRE PRIX ----------------------------- */
function filterPlaces() {
  const selected = document.getElementById("price-filter").value;
  const items = document.querySelectorAll(".place-card");

  items.forEach(item => {
    const price = parseInt(item.dataset.price);
    item.style.display = (selected === "All" || price <= parseInt(selected)) ? "block" : "none";
  });
}

/* ----------------------------- PLACE DETAILS ----------------------------- */
async function fetchPlaceDetails(placeId, token) {
  try {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await fetch(`${BASE_URL}/api/v1/places/${placeId}`, { headers });

    if (!response.ok) {
      document.getElementById("place-details").innerHTML = "<p>Impossible de charger les détails du lieu.</p>";
      return;
    }

    const place = await response.json();
    displayPlaceDetails(place);
  } catch (err) {
    console.error("Erreur réseau:", err);
    document.getElementById("place-details").innerHTML = "<p>Impossible de charger les détails du lieu.</p>";
  }
}

function displayPlaceDetails(place) {
  const details = document.getElementById("place-details");
  if (!details) return;

  details.innerHTML = `
    <h2>${place.title}</h2>
    <p>${place.description || "Pas de description"}</p>
    <p><strong>Prix :</strong> ${place.price} €</p>
    <p><strong>Commodités :</strong> ${place.amenities && place.amenities.length ? place.amenities.join(", ") : "Aucune"}</p>
  `;

  // Afficher le formulaire review uniquement si token + user_id
  const reviewSection = document.getElementById("add-review");
  const token = localStorage.getItem("token");
  const userId = localStorage.getItem("user_id");
  if (reviewSection) reviewSection.style.display = (token && userId) ? "block" : "none";
}

/* ----------------------------- FETCH REVIEWS ----------------------------- */
async function fetchPlaceReviews(placeId, token) {
  try {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await fetch(`${BASE_URL}/api/v1/places/${placeId}/reviews/`, { headers });

    if (!response.ok) {
      console.error("Impossible de charger les reviews");
      return;
    }

    const reviews = await response.json();
    displayPlaceReviews(reviews);
  } catch (err) {
    console.error("Erreur réseau lors du fetch des reviews:", err);
  }
}

function displayPlaceReviews(reviews) {
  const reviewList = document.getElementById("reviews");
  if (!reviewList) return;

  reviewList.innerHTML = "<h3>Avis</h3>";

  if (reviews && reviews.length > 0) {
    reviews.forEach(r => {
      const div = document.createElement("div");
      div.classList.add("review-item");
      div.innerHTML = `<p><strong>${r.user_name || "Utilisateur inconnu"} :</strong> ${r.text}</p>
                       <p>Note : ${r.rating}/5</p>`;
      reviewList.appendChild(div);
    });
  } else {
    reviewList.innerHTML += "<p>Aucun avis pour ce lieu.</p>";
  }
}

/* ----------------------------- AJOUT D'UN REVIEW ----------------------------- */
async function submitReview(event) {
  event.preventDefault();

  const token = localStorage.getItem("token");
  const userId = localStorage.getItem("user_id");
  if (!token || !userId) {
    alert("Vous devez être connecté pour poster un avis.");
    return;
  }

  const textInput = document.getElementById("review-text");
  const ratingInput = document.getElementById("review-rating");

  if (!textInput || !ratingInput) {
    console.error("Formulaire de review introuvable !");
    return;
  }

  const text = textInput.value;
  const rating = parseInt(ratingInput.value);
  const placeId = getPlaceIdFromURL();

  try {
    const response = await fetch(`${BASE_URL}/api/v1/reviews/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ text, rating, place_id: placeId, user_id: userId })
    });

    if (!response.ok) {
      const data = await response.json();
      alert(data.error || "Erreur lors de l'ajout de l'avis");
      return;
    }

    alert("Avis ajouté avec succès !");
    fetchPlaceReviews(placeId, token);
    document.getElementById("review-form").reset();
  } catch (error) {
    console.error("Erreur réseau:", error);
    alert("Impossible de poster l'avis. Vérifiez la console pour plus de détails.");
  }
}
