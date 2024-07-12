# Debtor Management System

## Features

- User authentication (registration, login, logout).
- Debtor management (add, view debtors).
- Profile and settings management.

## Technologies Used

- Flask
- Flask-SQLAlchemy
- SQLite
- HTML/CSS/JavaScript

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/debtor-management-system.git
   cd debtor-management-system
   ```

2. Setup virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:

   Create a `.env` file in the root directory with the following variables:

   ```plaintext
   SECRET_KEY=your_secret_key_here
   ```

5. Initialize the database:

   ```bash
   python app.py create_db
   ```

6. Run the application:

   ```bash
   python app.py
   ```

   Access the application at `http://localhost:5000` in your web browser.

## Usage

- Register a new user account.
- Log in with your credentials to access the dashboard.
- Manage debtors, view their details, and update your profile and settings as needed.
- Log out when finished using the system.

## Folder Structure

```
├── app.py                   # Main application file
├── templates/               # HTML templates
│   ├── base.html            # Base template with navigation
│   ├── dashboard.html       # Dashboard page
│   ├── profile.html         # Profile page
│   ├── settings.html        # Settings page
│   ├── add_debtor.html      # Add debtor page
│   ├── view_debtors.html    # View debtors page
│   └── ...                  # Other templates
├── static/                  # Static assets (CSS, JS)
│   ├── styles.css           # CSS styles for the application
│   ├── scripts.js           # JavaScript for interactivity
│   └── ...
├── requirements.txt         # Python dependencies
├── venv/                    # Virtual environment
├── .env                     # Environment variables
└── README.md                # This README file
```

## Contributing

Contributions are welcome! Fork the repository and submit a pull request with your enhancements or bug fixes.

