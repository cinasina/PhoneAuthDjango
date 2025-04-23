# Django Phone-Based Authentication

A secure and scalable authentication system built with Django and Django REST Framework, designed for phone number-based user registration and login. It supports OTP verification, password setting, and user info completion, with IP-based rate limiting to prevent abuse. This API can be used across various platforms, including web, mobile, and desktop applications.

## Features

- Phone number-based registration and login
- OTP verification for new users
- Password setting and user information collection
- JWT-based authentication (access and refresh tokens)
- IP and phone number-based rate limiting (blocks after 3 failed attempts for 1 hour)
- Secure session management using UUID-based session IDs
- Input validation and user-friendly error messages
- Platform-agnostic: Works for web, mobile, and desktop clients

## Requirements

- Python 3.8+
- Django 4.2+
- Django REST Framework
- django-rest-framework-simplejwt
- Redis (for caching OTPs and session IDs)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/cinasina/PhoneAuthDjango.git
   cd django-phone-auth
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   Create a `.env` file in the project root and add:

   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   REDIS_URL=redis://localhost:6379/0
   ```

5. **Apply migrations**:

   ```bash
   python manage.py migrate
   ```

6. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

## Usage

### API Endpoints

| Endpoint             | Method | Description                       | Payload Example                                         |
|----------------------|--------|-----------------------------------|----------------------------------------------------------|
| /api/register/       | POST   | Register or check phone number    | `{ "mobile_number": "09123456789" }`                    |
| /api/verify-otp/     | POST   | Verify OTP for new users          | `{ "session_id": "uuid", "code": "123456" }`           |
| /api/set-password/   | POST   | Set password for new users        | `{ "session_id": "uuid", "password": "pass1234" }`     |
| /api/user-info/      | POST   | Complete user information         | `{ "session_id": "uuid", "email": "user@example.com", "first_name": "Ali", "last_name": "Ahmadi" }` |
| /api/login/          | POST   | Login with phone and password     | `{ "session_id": "uuid", "password": "pass1234" }`     |

### Example Flow

1. **Register**: Send phone number to `/api/register/`.
    - Existing user: Receive `next_step: "password"`.
    - New user: Receive `next_step: "otp"` and an OTP via SMS.
2. **Verify OTP**: Send OTP to `/api/verify-otp/` to get `next_step: "set_password"`.
3. **Set Password**: Send password to `/api/set-password/` to get `next_step: "user_info"`.
4. **Complete Info**: Send user info to `/api/user-info/` to receive JWT tokens.
5. **Login**: Send phone number and password to `/api/login/` to receive JWT tokens.

## Configuration

### Redis

Configure Redis for caching session IDs and OTPs (default TTL: 120 seconds).

### JWT

Set `SIMPLE_JWT` settings in `settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```

### Rate Limiting

Blocks users after 3 failed attempts (password, OTP, or phone number) for 1 hour.

## Contributing

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For issues or questions, open an issue on GitHub or contact [cina72b@gmail.com](mailto:cina72b@gmail.com).
