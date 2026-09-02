# ParkVenue - Smart Parking Management System

![ParkVenue Logo](static/img/logo.png)

A modern, full-featured Django-based parking management platform that connects parking providers with customers looking for convenient parking spaces.

## 🚀 Features

### For Providers
- **Dashboard** - Overview of all managed parking spots
- **Parking Spot Management** - Add, edit, and delete parking locations
- **Reservation Management** - View and approve/decline reservation requests
- **Real-time Availability** - Track available slots in real-time
- **Pricing Control** - Set hourly rates and manage pricing
- **Location Management** - Add GPS coordinates and city information
- **Security Levels** - Configure security features (Basic, Standard, Premium)

### For Finders/Customers
- **Search Functionality** - Find parking by city and location
- **Parking Discovery** - Browse available parking spots with detailed information
- **Bookmarking** - Save favorite parking locations for quick access
- **Reservations** - Book and manage parking reservations
- **Reservation Tracking** - View pending and confirmed reservations

### Common Features
- **User Authentication** - Secure signup and login with OTP verification
- **Password Reset** - Email-based password recovery
- **Profile Management** - Update user information and contact details
- **Role-Based Access** - Different interfaces for Providers and Finders
- **Email Notifications** - OTP verification and password reset emails

## 🏗️ Project Structure

The project follows a modular app architecture with clear separation of concerns:

```
ParkVenue/
├── account/                    # Project configuration
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL router
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
│
├── authentication/             # User auth & account management
│   ├── models.py              # CustomUser model (with roles)
│   ├── views.py               # Auth views (login, signup, OTP, password reset)
│   ├── urls.py                # Auth URL patterns
│   └── util.py                # Email utilities
│
├── provider/                  # Parking provider management
│   ├── models.py              # ParkingSlot model
│   ├── views.py               # Provider dashboard, spot management
│   └── urls.py                # Provider URL patterns
│
├── finder/                    # Customer parking search
│   ├── views.py               # Finder dashboard, search functionality
│   └── urls.py                # Finder URL patterns
│
├── booking/                   # Reservation management
│   ├── models.py              # Reservation model
│   ├── views.py               # Booking and reservation views
│   └── urls.py                # Booking URL patterns
│
├── bookmarks/                 # Saved parking management
│   ├── models.py              # UserParkingBookmark model
│   ├── views.py               # Bookmark views
│   └── urls.py                # Bookmark URL patterns
│
├── acc/                       # Legacy templates & static files
│   └── templates/             # HTML templates
│
├── static/                    # Static files
│   ├── css/
│   │   └── parkvenue.css
│   ├── js/
│   │   └── parkvenue.js
│   └── img/
│
└── manage.py                  # Django management script
```

## 📊 Database Models

### Authentication App
- **CustomUser** - Extended Django User model with roles (provider, finder, admin)

### Provider App
- **ParkingSlot** - Parking location with availability, pricing, and security details

### Booking App
- **Reservation** - User parking reservations with status tracking

### Bookmarks App
- **UserParkingBookmark** - User's saved/favorite parking spots

## 🔧 Technology Stack

- **Backend Framework**: Django 5.0+
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Django's built-in auth with custom User model
- **Email Service**: SMTP (Gmail configured)
- **Server**: Gunicorn + WhiteNoise

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd Parkvenue
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venviroment
   
   # Activate it
   # On Windows:
   venviroment\Scripts\activate
   # On macOS/Linux:
   source venviroment/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files** (optional for development)
   ```bash
   python manage.py collectstatic --noinput
   ```

## 🚀 Running the Project

### Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

### Admin Panel
Access the Django admin at `http://127.0.0.1:8000/admin/` with your superuser credentials.

## 🔑 Key URL Patterns

### Authentication Routes
- `/` - Home/Initial page
- `/account/` - Login
- `/createacc/` - Sign up
- `/choice/` - Select role (Provider/Finder)
- `/otp/` - OTP verification
- `/forgot/` - Forgot password
- `/resetpass/` - Reset password
- `/logout/` - Logout

### Provider Routes
- `/home/` - Provider dashboard
- `/providerinfo/` - Provider profile
- `/proeditinfo/` - Edit profile
- `/addspot/` - Add new parking spot
- `/mannagepark/` - Manage parking spots
- `/parkingreservation/` - View reservations
- `/delete-parking/<id>/` - Delete parking spot
- `/update-reservation/<id>/` - Approve/decline reservation

### Finder Routes
- `/finder/` - Finder dashboard
- `/search-parking/` - Search parking by city
- `/finderreservation/` - View my reservations
- `/reserve/<id>/` - Book a parking spot
- `/cancel-parking/<id>/` - Cancel reservation

### Bookmarks Routes
- `/savedparking/` - View saved parking spots
- `/bookmark-slot/<id>/` - Toggle bookmark

## ⚙️ Configuration

### Email Settings
Configure email in `account/settings.py`:
```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Database
Default: SQLite (`db.sqlite3`)
For production, configure PostgreSQL in settings.

### Time Zone
Currently set to `Asia/Kolkata`. Update in `settings.py` if needed.

## 🧪 Testing

Run Django system checks:
```bash
python manage.py check
```

Check for deployment issues:
```bash
python manage.py check --deploy
```

## 🎨 Frontend Features

- **Responsive Design** - Works on desktop, tablet, and mobile
- **Modern UI** - Professional color scheme and animations
- **User-Friendly** - Intuitive navigation and clear workflows
- **Real-time Interactions** - Dynamic content updates

## 📝 API Routes Summary

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home page |
| `/account/` | GET, POST | Login |
| `/createacc/` | GET, POST | Register |
| `/finder/` | GET | Finder dashboard |
| `/search-parking/` | POST | Search by city |
| `/reserve/<id>/` | GET | Book spot |
| `/savedparking/` | GET | View bookmarks |
| `/home/` | GET | Provider dashboard |
| `/addspot/` | GET, POST | Add parking |
| `/mannagepark/` | GET | Manage spots |

## 🔐 Security Features

- **OTP Verification** - Two-step verification for signup
- **Password Hashing** - Secure password storage with Django's default hasher
- **CSRF Protection** - Built-in Django CSRF middleware
- **SQL Injection Prevention** - Django ORM protects against SQL injection
- **User Authentication** - Role-based access control

## 🚧 Future Enhancements

- [ ] Real-time notifications using WebSockets
- [ ] Payment integration (Stripe, Razorpay)
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced search filters (price range, amenities)
- [ ] Rating and review system
- [ ] Map integration (Google Maps API)
- [ ] Analytics dashboard for providers
- [ ] Automated invoice generation
- [ ] Customer support chat
- [ ] Multi-language support

## 📧 Email Configuration

The project uses Gmail SMTP for sending emails:
1. Enable 2-factor authentication on Gmail
2. Generate an App-specific password
3. Update `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in settings.py

## 🤝 Contributing

To contribute to this project:
1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

This project is provided as-is for educational and commercial use.

## 📞 Support

For issues or questions:
- Check the project documentation
- Review Django's official documentation
- Contact the development team

## 🎯 Project Goals

- Provide an efficient parking solution for urban areas
- Connect parking providers with customers seamlessly
- Reduce time spent searching for parking
- Increase parking utilization rates
- Create a sustainable mobility solution

---

**Last Updated**: September 2, 2026  
**Version**: 1.0.0  
**Status**: Active Development
