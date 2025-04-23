# PhoneAuthDjango

A sample authentication system built with Django and Django REST Framework, demonstrating phone number-based user registration and login. It includes OTP verification, password setup, user info collection, and JWT authentication. This project is suitable for demonstration or learning purposes and can be integrated into various platforms like web or mobile applications.

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
- PostgreSQL (or compatible database)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/cinasina/PhoneAuthDjango.git
   cd PhoneAuthDjango
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

   > You can use `pip-compile` from `pip-tools` to generate `requirements.txt` from `requirements.in`:
   > ```bash
   > pip install pip-tools
   > pip-compile requirements.in
   > ```

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

## Docker Setup

You can run the app using Docker for local development. A basic `Dockerfile` and `docker-compose.yml` are provided.

### Build and Run (Development Mode)

```bash
docker build -t phone-auth .
docker run -p 8000:8000 phone-auth
```

### Using Docker Compose

```bash
docker-compose up --build
```

### Production Deployment

For production, consider using Gunicorn and Whitenoise for static file serving. Example CMD in Dockerfile:

```dockerfile
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
```

You can also configure environment variables via Docker secrets or environment files.

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

## License

This project is licensed under the MIT License. See the LICENSE file for details.

