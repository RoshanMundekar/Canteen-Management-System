# Canteen Management System

This is a comprehensive web-based Canteen Management System built using the Django framework. The project is designed to manage various aspects of a canteen, including interactions from students, teachers, canteen staff, and visitors.

## Project Structure

The project (`firstproject`) contains the following main applications:

- `canteenapp`: Handles core canteen-related operations.
- `canteenStaff`: Manages staff duties, schedules, and operations.
- `studentapp`: Provides a portal and features specifically for students.
- `teacherapp`: Provides a portal and features specifically for teachers.
- `visitorsapp`: Manages visitor access and interactions with the canteen.

## Technologies Used

- **Backend:** Python, Django 4.2+
- **Database:** SQLite (default for development)
- **Frontend:** HTML, CSS, JavaScript (via Django Templates)

## Setup Instructions

1. **Clone the repository** (if applicable) and navigate to the project directory:
   ```bash
   cd firstproject
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   Open a web browser and go to `http://127.0.0.1:8000/`.

## Features
- Modular design separating functionality by user type.
- Integrated invoice management.
- Static and media files configuration included.

"# Canteen-Management-System" 
