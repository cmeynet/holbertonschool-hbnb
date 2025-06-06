# 🏡 HBnB Project – Technical Blueprint

## 📘 Introduction

The **HBnB Project** is a full-stack web application designed to manage and share listings for temporary housing, including users, places, amenities, and reviews. This technical documentation serves as a **blueprint** for the application’s architecture, guiding development and ensuring coherent system design.

It contains:
- An overview of the high-level layered architecture.
- A detailed view of the domain model and business logic.
- API sequence diagrams with full interaction flow breakdowns.

---

## 🏗️ High-Level Architecture

### 🎯 Diagram Objective

To represent the system's **layered architecture** and illustrate the **facade pattern** that mediates between API requests and business logic.

### 🧱 Package Diagram

![Package Diagram](/part1/Package_Diagram.png)

### 📌 Explanation

**Components:**
- **Presentation Layer**: Provides the public interface via APIs (UserAPI, PlaceAPI, ReviewAPI, AmenityAPI).
- **Business Logic Layer**: Implements core application logic, encapsulated in domain-specific classes.
- **Persistence Layer**: Interfaces with data storage.

**Design Decisions:**
- The **facade pattern** abstracts the complexity of the domain layer, promoting loose coupling and centralized access control.
- Layered architecture improves **separation of concerns**, **maintainability**, and **testability**.

**Integration:**
This structure serves as the foundational blueprint, ensuring a scalable and organized application flow from user input to database persistence.

---

## 🧠 Business Logic Layer

### 🎯 Diagram Objective

To define the **core domain model**, detailing entities, attributes, relationships, and behaviors. It reflects how business rules are implemented and enforced.

### 📊 Class Diagram

![Class Diagram](/part1/Class_Diagram_for_Business_Logic_Layer.png)

### 📌 Explanation

**Entities & Responsibilities:**

- **UserClass**
  - Represents users of the platform.
  - Handles authentication, user registration, email/password validation, and admin privileges.
  - Key methods: `register()`, `update()`, `delete()`, `is_admin()`.

- **PlaceClass**
  - Describes listings (houses, apartments, etc.).
  - Attributes include title, price, location, and description.
  - Linked to a user via `user_id`, establishing ownership.
  - Supports CRUD operations and listing by user.

- **ReviewClass**
  - Captures user feedback on places.
  - Each review is associated with a `user_id` and a `place_id`.
  - Supports creating, deleting, and listing reviews for a place.

- **AmenityClass**
  - Describes available services/features (Wi-Fi, Parking, etc.).
  - Independent entity, can be linked to multiple places.

- **AmenitiesPlace**
  - Manages the **many-to-many** relationship between Places and Amenities.
  - Ensures flexible linkage and decoupled feature management.

**Design Decisions:**
- Use of **UUIDs** ensures unique, secure identification across entities.
- Encapsulation of business rules inside entity classes supports **domain-driven design (DDD)**.
- Explicit junction tables (`AmenitiesPlace`) improve clarity and maintain referential integrity.

**Integration:**
This layer is at the heart of the application, interfacing directly with both the API (via the facade) and the database, enforcing data validation, access control, and application rules.

---

## 🔄 API Interaction Flow

### 🎯 Objective

The sequence diagrams model how requests move across the system from user to database. They visualize the **flow of control and data**, highlight **failure points**, and illustrate **design decisions** such as validation order and response formatting.

---

### 👤 Create User – `POST /users`

![Resgister User Sequence](/part1/Register_User.png)

**Key Components:**
- **API**: Receives the request and checks input format.
- **Business Logic**: Validates logic rules and attempts to create the user.
- **Database**: Handles actual data storage.

**Data Flow:**
1. User submits a registration request.
2. API validates field format.
3. Business logic checks if the email is unique.
4. If valid, the user is stored in the database.

**Design Decisions:**
- Early error handling (400, 409, 500) ensures fast feedback.
- Separation between syntax validation (API) and business rule validation (Logic).

**Architectural Role:**
This diagram ensures that **user creation logic is robust**, with clearly delineated responsibilities for input validation, conflict resolution, and persistence.

---

### 🏠 Create Place – `POST /places`

![Place Creation Sequence](/part1/Place_Creation.png)

**Key Components:**
- **API**: Parses and checks listing input.
- **Business Logic**: Verifies business rules (e.g., unique title).
- **Database**: Saves the new place.

**Data Flow:**
1. API receives listing details.
2. Validates data structure.
3. Business logic ensures title uniqueness and acceptable values.
4. If valid, place is stored and acknowledged with an ID.

**Design Decisions:**
- Validation split ensures **modular error reporting**.
- Early return on failure prevents unnecessary computation.

**Architectural Role:**
Demonstrates how a core resource (`Place`) is created while respecting both business rules and data integrity.

---

### 🔍 Get Places – `GET /places`

![Fetching a List of Places](/part1/Fetching_a_List_of_Places.png)

**Key Components:**
- **API**: Accepts filter parameters.
- **Business Logic**: Applies filters and queries.
- **Database**: Returns matching records.

**Data Flow:**
1. Filters are validated for syntax.
2. Business logic queries the database using criteria.
3. Returns either a list, empty array, or error.

**Design Decisions:**
- Designed to support **search and filtering**, a critical feature.
- Uses graceful fallback (empty list) for no results.

**Architectural Role:**
This sequence supports a **core use case**—retrieving listings—showing how filters propagate and data is returned.

---

### 📝 Post Review – `POST /reviews`

![Review Submission](/part1/Review_Submission.png)

**Key Components:**
- **API**: Validates user input.
- **Business Logic**: Verifies rules (e.g., rating range, unique review per user/place).
- **Database**: Stores the review.

**Data Flow:**
1. User posts a review.
2. API checks fields.
3. Business logic confirms that the review is valid and allowed.
4. On success, review is saved.

**Design Decisions:**
- Centralizes review validation in logic layer.
- Allows flexible extensions (e.g., rating algorithms, spam detection).

**Architectural Role:**
Ensures consistent and validated user feedback, supporting quality control and engagement features.

---

## 🧾 Conclusion

This document provides a complete technical map for HBnB’s design, encompassing:

- **Layered architecture** for scalability and clear role separation.
- **Domain-driven class modeling** for business logic.
- **Detailed interaction flow** for critical API endpoints.
- **Clear validation and error-handling strategy**, respecting both usability and data integrity.

By adhering to these guidelines, developers will have a **clear reference** to implement, extend, and maintain the system effectively.

## 👨‍💻 Authors

- Victoire BOUTIN - [GitHub](https://github.com/Victoire07)
- Clémence MEYNET - [GitHub](https://github.com/cmeynet)