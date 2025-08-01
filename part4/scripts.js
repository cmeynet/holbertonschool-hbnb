/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

/* Add an event listener for the form submission */
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    /* added an event listener: when the form is submitted,
    the function will be triggered */
      loginForm.addEventListener('submit', async (event) => {
          event.preventDefault(); /* prevent the page from automatically reloading */
          
          const email = document.getElementById('email').value;
          const password = document.getElementById('password').value;

          loginUser(email, password); /* function that will send the identifiers to the API */
      });
  }

  // call populatePriceFilter() only if we are on index.html
  const isIndexPage = document.getElementById('price-filter') !== null;
  if (isIndexPage) {
    populatePriceFilter();
  }

  checkAuthentication();

  const reviewForm = document.getElementById('review-form');
  if (reviewForm) {
    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();

    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const reviewText = document.getElementById('review').value;
      const rating = document.getElementById('rating').value;

      await submitReview(token, placeId, reviewText, rating, reviewForm);
    });
  }
})

/* Make the AJAX request to the API */
async function loginUser(email, password) {
  const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });
  
  /* Handle the API response and store the token in a cookie */
  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } else {
    alert('Login failed: ' + response.statusText);
  }
}

let allPlaces = []; // will contain all locations received from the API
let authToken = null; // will contain the token received from the API

function populatePriceFilter() {
  const filter = document.getElementById('price-filter');
  if (!filter) return; // prevents an error if the element does not exist
  const prices = [10, 50, 100];
  
  // Option "All"
  const allOption = document.createElement('option');
  allOption.value = '';
  allOption.textContent = 'All';
  filter.appendChild(allOption);

  // Add the other prices
  prices.forEach(price => {
    const option = document.createElement('option');
    option.value = price;
    option.textContent = `≤ $${price}`;
    filter.appendChild(option);
  });
}

/* Function to check for the JWT token in cookies and control the visibility of the login link */
function checkAuthentication() {
  const token = getCookie('token');
  authToken = token;

  if (!token) {
    const currentPage = window.location.pathname;
    const allowedPages = ['/index.html', '/login.html', '/']; // les pages publiques
    
    if (!allowedPages.includes(currentPage)) {
      window.location.href = 'index.html';
    }
    return token;
  }

  const loginLink = document.getElementById('login-link');
  const addReviewSection = document.getElementById('add-review');
  
  if (loginLink) loginLink.style.display = 'none';
  if (addReviewSection) addReviewSection.style.display = 'block';
  
  const placeId = getPlaceIdFromURL();

  // Only call the data if it is not add_review.html
  if (window.location.pathname.includes('add_review.html')) {
    return; // Don't load the location data here, handle that in add_review
  }

  if (placeId) {
    fetchPlaceDetails(token, placeId);
  } else {
    // Fetch places data if the user is authenticated
    fetchPlaces(token);
  }
}

function getCookie(name) {
  // Function to get a cookie value by its name
  const value = `; ${document.cookie}`;
  /* Cuts the string at the exact point where the requested cookie begins */
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop().split(';').shift();
  }
  return null;
}

/* Fetch API to get the list of places and handle the response */
async function fetchPlaces(token) {
  const headers = {
    'Content-Type': 'application/json'
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  // Make a GET request to fetch places data
  const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
    method: 'GET',
    headers: headers
  });
  
  // Handle the response and pass the data to displayPlaces function
  if (response.ok) {
    const places = await response.json();
    allPlaces = places; // stores the full list for later filtering
    displayPlaces(places);
  } else {
    console.error("Error retrieving locations:", response.statusText);
  }
}

/* Create HTML elements for each place and append them to the #places-list */
function displayPlaces(places) {
  // Retrieves the section that contains the list of locations
  const container = document.getElementById('places-list');

  // Clear the current content of the places list
  container.innerHTML = '';

  // Iterate over the places data
  places.forEach(place => {
    // For each place, create a div element and set its content
    const placeDiv = document.createElement('div');
    placeDiv.classList.add('place-card'); // class for the style
    placeDiv.setAttribute('price', place.price);

    // Sets the HTML content of the location
    placeDiv.innerHTML = `
      <h3>${place.title}</h3>
      <p class="price">Price per night: $${place.price}</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;
    
    // Append the created element to the places list
    container.appendChild(placeDiv);

    // Add the event listener to the button
    /*const button = placeDiv.querySelector('.details-button');
    if (button) {
      button.addEventListener('click', () => {
        // Redirect to the location details page with the ID in the URL
        window.location.href = `place.html?id=${place.id}`;
        });
      }*/
  });
}

// Implement client-side filtering
document.getElementById('price-filter').addEventListener('change', (event) => {
  // Get the selected price value
  const selectedPrice = parseFloat(event.target.value);
  const placeCards = document.querySelectorAll('.place-card');

  // Iterate over the places and show/hide them based on the selected price
  placeCards.forEach(card => {
    const price = parseFloat(card.getAttribute('price'));

    if (isNaN(selectedPrice) || price <= selectedPrice) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
});

/* Function to extract location ID from query parameters */
function getPlaceIdFromURL() {
  // Extract the place ID from window.location.search
  const queryParams = new URLSearchParams(window.location.search);
  return queryParams.get('id');
}

/* Get location details and manage response */
async function fetchPlaceDetails(token, placeId) {
  // Make a GET request to fetch place details
  // Include the token in the Authorization header
  
  const headers = {
    'Content-Type': 'application/json'
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response =await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
    method: 'GET',
    headers: headers
  });
  
  // Handle the response and pass the data to displayPlaceDetails function
  if (response.ok) {
    const place = await response.json();
    displayPlaceDetails(place);
  } else {
    console.error('Error retrieving location:', response.status, response.statusText);
  } 
}

/* Create HTML elements for location details */
function displayPlaceDetails(place) {
  const container = document.querySelector('#place-details');

  if (!container) return;

  // Clear the current content of the place details section
  container.innerHTML = '';

  // Create elements to display the place details (name, description, price, amenities and reviews)
  const infoDiv = document.createElement('div');
  infoDiv.classList.add('place-info');

  // Title
  const title = document.createElement('h2');
  title.textContent = place.title;
  infoDiv.appendChild(title);

  // Name of the host
  const host = document.createElement('p');
  host.innerHTML = `<strong>Host:</strong> ${place.owner || 'Unknown'}`;

  // Price per night
  const price = document.createElement('p');
  price.innerHTML = `<strong>Price per night:</strong> $${place.price}`;

  // Description
  const description = document.createElement('p');
  description.innerHTML = `<strong>Description:</strong> ${place.description}`;

  // Amenities
  const amenities = document.createElement('p');
  const amenitiesList = place.amenities?.map(a => a.name).join(', ') || 'None';
  amenities.innerHTML = `<strong>Amenities:</strong> ${amenitiesList}`;

  // Append the created elements to the place details section
  infoDiv.appendChild(host);
  infoDiv.appendChild(price);
  infoDiv.appendChild(description);
  infoDiv.appendChild(amenities);
  
  container.appendChild(infoDiv);
}

async function submitReview(token, placeId, reviewText, rating, formElement) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(rating),
                place_id: placeId
            })
        });

        handleResponse(response, formElement);

    } catch (error) {
        alert("Error submitting review: " + error.message);
        return false;
    }
}

function handleResponse(response, formElement) {
  if (response.ok) {
    alert('Review submitted successfully!');
    if (formElement) {
      formElement.reset();
    }
  } else {
    response.json().then(data => {
      const errorMsg = data.error || response.statusText;
      alert('Failed to submit review: ' + errorMsg);
    }).catch(() => {
      alert('Failed to submit review: unknown error.');
    });
  }
}