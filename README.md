# Medicine Delivery App

## Features Overview

1. ### Login and Logout:
   **Description:** Users can log in and log out of their accounts.  
   **Functionality:** Provides authentication for accessing personalized features.

2. ### Admin Page:
   **Description:** Admins can manage users, medicines, doctors, and other system aspects.  
   **Functionality:** Allows administrators to perform CRUD operations on system resources.

3. ### Medicine Selection:
   **Description:** Users can browse and select medicines from a list.  
   **Functionality:** Allows users to view available medicines and add them to their shopping cart.

4. ### Updating Profile:
   **Description:** Users can update their personal information.  
   **Functionality:** Enables users to modify their profile details such as contact information or address.

5. ### Shopping Cart:
   **Description:** Users can manage items added for purchase.  
   **Functionality:** Allows users to add, remove, and update quantities of items in their shopping cart.

6. ### Check-in and Check-out:
   **Description:** Users can initiate orders and complete purchases.  
   **Functionality:** Facilitates the process of confirming orders and proceeding to payment.

7. ### Doctor Consultation:
   **Description:** Users can book appointments for consultations with doctors.  
   **Functionality:** Facilitates scheduling of appointments with available doctors.

8. ### Lab Test Scheduling:
   **Description:** Users can view and schedule lab tests.  
   **Functionality:** Allows users to select lab tests, schedule appointments, and view test results.

9. ### Adding Medicine/Doctor/Lab Test (Admin Page):
   **Description:** Admins can add new medicines, doctors, or lab tests to the system.  
   **Functionality:** Enables administrators to input and save new entries into the database.

10. ### Chatbot:
    **Description:** Provides automated assistance and answers user queries.  
    **Functionality:** Offers real-time responses to common inquiries related to products and services.

## API Endpoints Description

| Endpoint                          | Method | Purpose                                     | Usage                                                 |
|-----------------------------------|--------|---------------------------------------------|-------------------------------------------------------|
| /api/login                        | POST   | Authenticates user login.                   | Logging in users to access personalized features.     |
| /api/logout                       | POST   | Logs out the current user session.          | Logging out users to terminate their session.         |
| /api/register                     | POST   | Registers a new user.                       | Creating new user accounts.                           |
| /api/index/display                | GET    | Displays index information.                 | Displaying general index information.                 |
| /api/update                       | PUT    | Updates general information.                | Updating general information.                         |
| /api/medicines                    | GET    | Retrieves list of medicines.                | Displaying available medicines.                       |
| /api/medicines/add_to_cart        | POST   | Adds selected medicine to user's shopping cart. | Adding medicines to the shopping cart.            |
| /api/cart                         | GET    | Retrieves the current user's shopping cart. | Displaying the contents of the shopping cart.         |
| /api/medicines/update_cart        | POST   | Updates quantity of medicine in user's shopping cart. | Modifying quantities of medicines in the cart.   |
| /api/medicines/delete_from_cart   | POST   | Removes selected medicine from user's shopping cart. | Deleting medicines from the shopping cart.       |
| /api/orders                       | GET    | Retrieves list of orders.                   | Displaying user's orders.                             |
| /api/order_tracking               | GET    | Tracks the status of an order.              | Tracking the current status of an order.              |
| /api/checkout                     | POST   | Checks out the shopping cart.               | Finalizing and paying for the items in the cart.      |
| /api/admin/add_medicine           | POST   | Adds a new medicine to the system.          | Allowing admins to add new medicines.                 |
| /api/admin/delete_medicine        | DELETE | Deletes a medicine from the system.         | Allowing admins to delete medicines.                  |
| /api/admin/add_doctor             | POST   | Adds a new doctor to the system.            | Allowing admins to add new doctors.                   |
| /api/admin/delete_doctor          | DELETE | Deletes a doctor from the system.           | Allowing admins to delete doctors.                    |
| /api/admin/add_lab_test           | POST   | Adds a new lab test to the system.          | Allowing admins to add new lab tests.                 |
| /api/admin/delete_lab_test        | DELETE | Deletes a lab test from the system.         | Allowing admins to delete lab tests.                  |
| /api/admin/update_order           | PUT    | Updates the status of an order.             | Allowing admins to update order status.               |
| /api/consultations1               | GET    | Retrieves list of available doctor consultations. | Displaying available doctor consultations.      |
| /api/labtests1                    | GET    | Retrieves list of available lab tests.      | Displaying available lab tests.                       |
| /api/basic_health_screening       | GET    | Retrieves basic health screening tests.     | Displaying basic health screening tests.              |
| /api/labtests/book                | POST   | Books a consultation with a doctor.         | Booking appointments with doctors for consultation.   |
| /api/labtests/schedule            | POST   | Schedules a lab test appointment.           | Scheduling appointments for lab tests.                |
| /api/past_consultation            | GET    | Retrieves past consultations.               | Displaying user's past consultations.                 |
| /api/past_lab_bookings            | GET    | Retrieves past lab bookings.                | Displaying user's past lab bookings.                  |
| /api/chat                         | POST   | Handles user queries and provides automated responses. | Engaging with users through automated chat responses. |
| /api/ask                          | POST   | Answers user queries.                       | Providing answers to user queries.                    |
