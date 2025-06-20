# 📄 API Test Report – HBNB Project

## 🧪 Context
Automated tests were conducted using Python’s `unittest` module to validate the functionality of the Flask REST API. The tested resources include: `Users`, `Amenities`, `Places`, and `Reviews`.

---

## 🔹 1. Endpoints Tested

| Resource   | HTTP Method | Endpoint                                      |
|------------|-------------|-----------------------------------------------|
| Users      | `POST`      | `/api/v1/users/`                              |
|            | `GET`       | `/api/v1/users/`                              |
|            | `GET`       | `/api/v1/users/<user_id>`                    |
|            | `PUT`       | `/api/v1/users/<user_id>`                    |
| Amenities  | `POST`      | `/api/v1/amenities/`                         |
|            | `GET`       | `/api/v1/amenities/`                         |
|            | `GET`       | `/api/v1/amenities/<amenity_id>`            |
|            | `PUT`       | `/api/v1/amenities/<amenity_id>`            |
| Places     | `POST`      | `/api/v1/places/`                            |
|            | `GET`       | `/api/v1/places/`                            |
|            | `GET`       | `/api/v1/places/<place_id>`                 |
|            | `PUT`       | `/api/v1/places/<place_id>`                 |
| Reviews    | `POST`      | `/api/v1/reviews/`                           |
|            | `GET`       | `/api/v1/reviews/`                           |
|            | `GET`       | `/api/v1/reviews/<review_id>`               |
|            | `PUT`       | `/api/v1/reviews/<review_id>`               |
|            | `DELETE`    | `/api/v1/reviews/<review_id>`               |
|            | `GET`       | `/api/v1/reviews/places/<place_id>/reviews` |

---

## 🔹 2. Input Data Used

- Objects were dynamically created with valid data such as:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john<UUID>@example.com"
}
```

- Invalid cases tested:
  - Duplicate email (`POST /users/`)
  - Missing or empty fields (`POST`/`PUT` for all resources)
  - Invalid IDs (`GET`, `PUT`, `DELETE` with `invalid-id`)

---

## 🔹 3. Expected vs. Actual Results

| Test Case                                              | Expected Status | Actual Status | Result |
|--------------------------------------------------------|------------------|----------------|--------|
| `GET /users/`                                          | 200              | 200            | ✅      |
| `POST /users/` with duplicate email                    | 400              | 400            | ✅      |
| `POST /users/` with incomplete data                    | 400              | 400            | ✅      |
| `GET /users/invalid-id`                                | 404              | 404            | ✅      |
| `PUT /users/<user_id>` with valid data                 | 200              | 200            | ✅      |
| `PUT /users/invalid-id`                                | 404              | 404            | ✅      |
| `PUT /users/<user_id>` with invalid data               | 400              | 400            | ✅      |
| `GET /places/invalid-id`                               | 404              | 404            | ✅      |
| `POST /reviews/` with missing data                     | 400              | 400            | ✅      |
| `PUT /reviews/invalid-id`                         | 404              | 404            | ✅      |
| `DELETE /reviews/invalid-id`                      | 404              | 404            | ✅      |
| `GET /reviews/places/<invalid-id>/reviews`        | 404              | 404            | ✅      |
| `PUT /reviews/<review_id>` with invalid data             | 400              | **404**        | ❌     |

---

## 🔹 4. Issues Encountered

### ❗ `PUT /reviews/<review_id>` with invalid data returns 404
- **Expected**: `400 Bad Request` (validation error)
- **Actual**: `404 Not Found`
- **Hypothesis**: The backend logic checks `user_id` and `place_id` **before** validating request fields. This causes a 404 even if the `review_id` is valid.
- **Recommended Action**: Improve backend logic to distinguish clearly between `404` (not found) and `400` (bad input).

---

## ✅ Conclusion

- All test cases were executed using `unittest`.
- The API meets expected HTTP status codes in almost all scenarios.
- Only one case (invalid review update) requires improved error handling logic.