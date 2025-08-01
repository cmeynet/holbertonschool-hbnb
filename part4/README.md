# 🏡 HBNB - Frontend

This project is a web interface developed in **JavaScript**, **HTML**, and **CSS** that communicates with the **HBNB backend API** (Flask/REST).  
It allows users to:
- **Browse available places**
- **Apply filters** (price)
- **View detailed place information**
- **Log in**
- **Submit reviews** for a place

---

## 📂 Project Structure

```
.
├── add_review.html      # Form to add a review for a place
├── index.html           # Homepage displaying list of places and price filter
├── login.html           # User login page
├── place.html           # Detailed page for a single place (description, price, reviews, etc.)
├── script.js            # Main JavaScript file (API calls, filtering, authentication)
├── style.css            # CSS styles
└── README.md            # Project documentation
```

---

## 🚀 Detailed Features

### 1. **Homepage (`index.html`)**
- Displays a **list of places** fetched from the backend (`GET /api/v1/places/`).
- **Price filtering** via a dropdown menu (`≤ $10`, `≤ $50`, `≤ $100`, or **All**).
- Accessible **to everyone** (even without login).
- Links to each place’s details page (`place.html?id=<id>`).

---

### 2. **Login (`login.html`)**
- Form with **email** and **password** fields.
- Sends credentials to `POST /api/v1/auth/login`.
- On success:
  - Stores the **JWT token** in a cookie (`token`).
  - Redirects to `index.html`.
- On failure:
  - Displays an error message.

⚠️ Some pages are only accessible **after login** (e.g., `add_review.html`).

---

### 3. **Place Details (`place.html`)**
- Shows **complete information** for a selected place:
  - Title
  - Host name
  - Price per night
  - Description
  - Amenities list
- Fetches data from `GET /api/v1/places/:id`.
- May show/hide options depending on authentication status.

---

### 4. **Add a Review (`add_review.html`)**
- Accessible only **after login**.
- Form allows:
  - Writing a review text
  - Giving a rating (`1 to 5`)
- Sends data to `POST /api/v1/reviews/` with the **token** in the header.
- Shows a success or error message.

---

## 🌐 Navigation & Access

| Page               | Local URL                                    | Access Type               | Description |
|--------------------|----------------------------------------------|---------------------------|-------------|
| Homepage           | `http://localhost:8000/index.html`           | Public                    | Places list + price filter |
| Login              | `http://localhost:8000/login.html`           | Public                    | User login form |
| Place Details      | `http://localhost:8000/place.html?id=1`      | Public                    | Information about a place |
| Add Review         | `http://localhost:8000/add_review.html?id=1` | Logged-in users only      | Review submission form |

⚠️ **Notes:**
- If you try to access `add_review.html` without logging in, you will be redirected to `index.html`.
- The `id` in the URL (e.g., `id=1`) is the place ID and should be replaced with the actual ID retrieved from `index.html`.

---

## 📡 Backend Requirements

The **HBNB API** backend must be running locally at:

```
http://127.0.0.1:5000/api/v1/
```

API endpoints used by the frontend:
- `POST /auth/login`
- `GET /places/`
- `GET /places/<id>`
- `POST /reviews/`

---

## ⚙️ Installation & Running

1. **Clone the project**
```bash
git clone https://github.com/your-username/hbnb-frontend.git
cd hbnb-frontend
```

2. **Start the backend**  
(Refer to the backend project documentation.)

3. **Serve the frontend**  
Run from the project root:
```bash
python3 -m http.server 8000
```
Then open:
```
http://localhost:8000/index.html
```

---

## 🔑 Important Notes
- The **JWT token** is stored in a cookie for authentication.
- Private pages automatically redirect to `index.html` if the user is not logged in.
- Filtering is done **client-side** (JavaScript) without making a new API request.

---
