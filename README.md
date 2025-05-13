
# Feedback Generator
## Django + Celery + PostgreSQL + Docker Project

This project is a Django REST API integrated with Celery for asynchronous task processing and PostgreSQL for persistent storage. Redis is used as the message broker. Docker and Docker Compose handle containerization and orchestration. Flower is used to monitor background tasks.

---
## 📦 Technologies Used

- **Django** 5.2.1
- **Celery** 5+
- **Redis** (as broker)
- **PostgreSQL** 16
- **Docker & Docker Compose**
- **Poetry** (for dependency management)
- **Flower** (for monitoring Celery)

---

## 🛠️ Requirements

- Docker
- Docker Compose

---

## 📁 Project Structure
```
.
├─ config/
│  └─ redis.conf
├─ myproject/
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ celery.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ reports/
│  ├─ migrations/
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ serializers.py
│  ├─ tasks.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
├─ .env
├─ AUTH
├─ docker-compose.yml
├─ Dockerfile
├─ manage.py
├─ PING
├─ poetry.lock
├─ pyproject.toml
└─ README.md
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ompodey/Software-Developer-IIT-Madras-celery-assignment
cd Software-Developer-IIT-Madras-celery-assignment 
```
### 2. Create a .env File (if not present)

```bash
POSTGRES_DB=assignment
POSTGRES_USER=21f2000968
POSTGRES_PASSWORD=mypassword
SECRET_KEY=your-super-secret-key
``` 
 - ### ⚠️ Security Note
    The included `.env` file contains development credentials   **for evaluation purposes only**. In a production environment:
    1. These values should be rotated
    2. The file should be added to `.gitignore`
    3. Also Debugg = True

### 3. Build and Start the Application
```bash
docker-compose up --build
```
### 4. Apply the Dabase migrations 

```bash
docker-compose exec web poetry run python manage.py makemigrations reports

docker-compose exec web poetry run python manage.py migrate
```
- ### ⚠️ Caution
    may require rebuilt if DB not working in some cases :
    ```bash
    docker-compose down
    docker-compose up --build
    ```
### 5. Access the Application
 - Django App 🔗: http://localhost:8000
 - Flower Dashboard🔗: http://localhost:5555

---
# 📝 API Documentation

## 📡 Endpoints

### 1. Generate HTML Report
**`POST /assignment/html`**

**Request:**
```json
{
  "student_id": "string (required)",
  "namespace": "string (optional)",
  "events": [
    {
      "unit": "string/number (required)",
      "type": "string (optional)",
      "created_time": "datetime (optional)"
    }
  ]
}
```
| Status | Code    | Response                |
| :-------- | :------- | :------------------------- |
| `Accepted` | `202` | {"task_id": "b2531b04-fb51-4677-9b5a-e87023718185"} |
| `Success` | `200` |{"task_id": "b2531b04-fb51-4677-9b5a-e87023718185"} |
| `Failed` | `404/405` | {"error": "message", "details": {}} |

- Example
- ![image](https://github.com/user-attachments/assets/ad2b19ef-dfef-4953-a7f1-5d77eeb48150)

### 2. Check HTML Report Status
**`GET /assignment/html/<task_id>`**

**Responses:**
| Status | Code    | Response                |
| :-------- | :------- | :------------------------- |
| `Accepted` | `202` | {"status": "PENDING", "student_id": "...", "created_at": "..."} |
| `Success` | `200` |HTML content|
| `Failed` | `404/405` | {{"status": "FAILURE", "error": "..."} |

- Example
- ![image](https://github.com/user-attachments/assets/48dae4e3-5cb2-4101-94a2-4cc7f9f2d2a1)
- ![image](https://github.com/user-attachments/assets/ca46794d-1f7d-483c-8e46-a636f791974a)



### 3. Generate PDF Report
**`POST /assignment/pdf`**
(Same request format as HTML endpoint)

**Responses:**
| Status | Code    | Response                |
| :-------- | :------- | :------------------------- |
| `Accepted` | `202` | {"task_id": "uuid", "status": "Processing started"} |
| `Success` | `200` |{"Success"}|
| `Error` | `404/405` | {{"status": "FAILURE", "error": "..."} |


- Example
- ![image](https://github.com/user-attachments/assets/d5c8fba0-945c-4757-90c6-b24f64699ee0)



### 4. Check PDF Report Status
**`POST /assignment/pdf`**
(Same request format as HTML endpoint)

**Responses:**
| Status | Code    | Response                |
| :-------- | :------- | :------------------------- |
| `RUNNING` | `202` | {"task_id": "uuid", "status": "Processing started"} |
| `Success` | `200` |pdf download|
| `Error` | `404/405` | {{"status": "FAILURE", "error": "..."} |

- Example
- ![image](https://github.com/user-attachments/assets/b876acd1-51cc-4fdb-a779-7881c7f0bf87) ![image](https://github.com/user-attachments/assets/c4e8c23f-abe3-4c2e-9dfc-a37db9cb231b)




---
# 7. Using Docker Compose
- Docker Compose sets up the following services:

- web: Django application

- db: PostgreSQL database

- redis: Celery broker

- celery: Celery worker

- flower: Celery dashboard
Run everything using:
```bash
docker-compose up --build
```
---
# 8. Assumptions & Design Decisions
- PostgreSQL is chosen over SQLite to support large data operations.

- Docker containers are used to isolate services for consistency.

- Flower is included for task monitoring.

- Redis acts as a message broker for Celery.

- Django SECRET_KEY is loaded from the .env file to enhance security.

---
# 9. Extra Points Implemented
- Retries on failure: Celery tasks configured with retry logic.

- Query optimization: Optimized ORM queries for bulk inserts and selects.

- Error handling: Comprehensive validation and custom error responses added to APIs.
