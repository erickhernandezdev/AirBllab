# AirBllab — Accommodation & Experience Marketplace

## Description

**AirBllab** is a web platform inspired by modern accommodation and experience marketplaces. Users can browse available accommodations, activities, and services, view detailed listings, manage reservations, and interact with the platform through a responsive interface.

The project evolved from an academic application into a production-deployed project, incorporating software engineering practices such as:

* Modular Django application architecture
* PostgreSQL with multiple database schemas
* Authentication and access control
* Brute-force protection with Django Axes
* Automated testing
* Code coverage
* Static analysis with SonarQube
* Continuous Integration with GitHub Actions
* Docker-based local development
* Production deployment with Render
* Responsive and mobile-oriented UI

## Live Demo

The application is deployed on Render:

**Live Application:** [https://airbllab-demo.onrender.com/](https://airbllab-demo.onrender.com/?utm_source=gemini)

The production environment uses HTTPS and a cloud-hosted PostgreSQL database.

---

## Key Features

### Marketplace

* Browse accommodations, activities, and services
* View detailed information for each listing
* Responsive listing cards and collections
* Availability and reservation management
* Block dates based on existing reservations
* Shopping cart functionality
* Reservation history
* Public user publications

### Authentication & Security

* User registration and login
* Custom Django user model
* Session-based authentication
* Protected views with Django authentication decorators
* Brute-force protection using **Django Axes**
* CSRF protection
* Secure cookies and HTTPS configuration for production
* Environment-based configuration for secrets and database credentials
* HTTP method restrictions on endpoints
* Subresource Integrity (SRI) for external scripts
* Accessibility and security issues continuously reviewed with SonarQube

### Administration

The platform includes a custom administrative interface for managing the marketplace without relying exclusively on Django Admin.

Administrators can:

* Review pending publications
* Approve or reject accommodations
* Record approval/rejection notes
* Review approval history
* Manage registered users
* Inspect publication details

### Responsive UI

The frontend uses standard web technologies without a heavy frontend framework:

* HTML5
* CSS3
* Vanilla JavaScript
* CSS Grid
* Flexbox
* Responsive breakpoints
* Horizontal touch-friendly carousels
* CSS scroll snapping

The interface adapts between desktop and mobile layouts while maintaining the same core functionality.

---

## Architecture

The backend follows Django's modular application structure, separating functionality into independent applications.

```text
airbnb_project/
│
├── apps/
│   ├── admin_panel/       # Administrative functionality
│   ├── cart/              # Shopping cart
│   ├── core/              # Core models and business logic
│   ├── history/           # Reservation history
│   ├── homepage/          # Homepage
│   ├── item_view/         # Listing detail pages
│   ├── listings/          # Listing collections
│   ├── login/             # Authentication
│   ├── my_publications/   # User publications
│   ├── new_proposal/      # New listing proposals
│   └── payment/           # Payment functionality
│
├── airbnb_app/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/
├── static/
├── media/
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── Procfile
```

This structure keeps domain-specific functionality separated and makes the project easier to maintain and extend.

---

## Database Architecture

AirBllab uses **PostgreSQL** as its relational database.

The project separates different areas of the application using PostgreSQL schemas:

```text
django
carts
experiences
experiences_types
invoices
reservations
users
public
```

Django is configured with a PostgreSQL `search_path` so the application can work with these schemas transparently.

### Automated database initialization

The project includes custom Django management commands for local and deployment environments.

```bash
python manage.py create_schemas
python manage.py migrate
python manage.py seed_db
```

These commands allow a new environment to be initialized consistently without manually creating database structures or sample data.

---

## Testing & Code Quality

Testing and static analysis are integrated into the development workflow.

### Automated Tests

The project uses Django's testing framework to validate application behavior.

Tests cover areas such as:

* Authentication
* Views
* Reservations
* Cart functionality
* Application logic
* HTTP responses and redirects

Tests can be executed locally with:

```bash
python manage.py test
```

### Code Quality

**Ruff** is used for Python linting and code formatting:

```bash
ruff check .
ruff format --check .
```

Ruff checks are also integrated into the Git workflow through pre-commit hooks.

### Code Coverage

Coverage is generated during CI using `coverage.py`:

```bash
coverage run manage.py test
coverage xml
```

The generated XML report is consumed by SonarQube to incorporate test coverage into the project's code-quality analysis.

### SonarQube

SonarQube is used for continuous static analysis.

The project has been reviewed for issues involving:

* Code smells
* Security vulnerabilities
* Duplicated code
* Accessibility
* CSS issues
* HTTP method restrictions
* HTML form accessibility
* Database model configuration
* External script security

The goal is not only to make the application functional, but also to continuously improve maintainability and code quality.

---

## CI/CD

The project uses **GitHub Actions** for Continuous Integration.

The workflow runs automatically on pushes to the `demo` branch and on pull requests.

### CI Pipeline

The current pipeline performs the following steps:

```text
GitHub Push / Pull Request
          │
          ▼
     Checkout Code
          │
          ▼
     Setup Python 3.14
          │
          ▼
   Install Dependencies
          │
          ▼
   Start PostgreSQL 18
          │
          ▼
   Configure Test Database
          │
          ▼
      Run Tests
          │
          ▼
   Generate Coverage
          │
          ▼
      SonarQube
```

The CI environment uses a PostgreSQL service container, allowing the test suite to run against PostgreSQL rather than a lightweight development database.

This helps detect integration problems between Django and the actual database engine before changes are merged.

---

## DevOps & Deployment

### Docker

Local development can be reproduced using Docker Compose.

The environment includes:

* Django application container
* PostgreSQL database container
* Persistent PostgreSQL volume
* Shared application configuration

Start the environment with:

```bash
docker compose up -d --build
```

### Production

The application is deployed to **Render** using Gunicorn as the WSGI server.

Production configuration includes:

* HTTPS
* Environment-based secrets
* PostgreSQL
* Gunicorn
* Static file handling
* Production security settings

---

## Tech Stack

| Category          | Technology                        |
| ----------------- | --------------------------------- |
| Language          | Python 3.14                       |
| Backend           | Django 5.2.17                     |
| Database          | PostgreSQL                        |
| ORM               | Django ORM                        |
| Database Driver   | Psycopg 3 (psycopg[binary])       |
| Frontend          | HTML5, CSS3, JavaScript           |
| Authentication    | Django Authentication             |
| Security          | Django Axes, CSRF, secure cookies |
| Testing           | Django Test Framework             |
| Coverage          | coverage.py                       |
| Code Quality      | SonarQube                         |
| CI                | GitHub Actions                    |
| Containers        | Docker & Docker Compose           |
| Production Server | Gunicorn                          |
| Hosting           | Render                            |
| Version Control   | Git & GitHub                      |

---

## Getting Started

### Prerequisites

Install:

* Git
* Docker Desktop
* Docker Compose

Docker is the recommended way to run the project locally.

---

### Option 1 — Docker

Clone the repository:

```bash
git clone https://github.com/erickhernandezdev/AirBllab.git
cd AirBllab/airbnb_project
```

Start the application:

```bash
docker compose up -d --build
```

Initialize the database:

```bash
docker compose exec web python manage.py create_schemas
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_db
```

Open:

```text
http://localhost:8000/
```

### Useful Docker Commands

View application logs:

```bash
docker compose logs -f web
```

Stop the containers:

```bash
docker compose stop
```

Stop and remove the containers:

```bash
docker compose down
```

---

### Option 2 — Native Python Environment

Create a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Configure PostgreSQL and create a `.env` file.

Example:

```env
DEBUG=True

SECRET_KEY=your-secret-key

DB_NAME=airbllab_db
DB_USER=airbnb_admin
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

Initialize the database:

```bash
python manage.py create_schemas
python manage.py migrate
python manage.py seed_db
```

Run the development server:

```bash
python manage.py runserver
```

---

## Environment Variables

The application uses environment variables for configuration and sensitive values.

Typical configuration includes:

```env
DB_NAME=airbllab_db
DB_USER=airbnb_admin
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
DEBUG=True
```

Production credentials should never be committed to the repository.

---

## Author

* **Author:** [Erick Hernández](https://github.com/erickhernandezdev?utm_source=gemini) — *Software Engineer*

---

## License

This project was developed as an academic and portfolio project.
