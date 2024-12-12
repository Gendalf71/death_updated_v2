# Death Project

## Overview
This project is a Django-based web application. Below are the steps to set up and run the project.

## Requirements
- Python 3.8 or newer
- pip (Python package installer)

## Setup Instructions
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Unix or MacOS:
     ```bash
     source venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Notes
- The project uses SQLite as the default database.
- Ensure that Django is installed before attempting to run the server.

## Next Steps
Inspect the application logic, verify that all routes are functional, and debug any issues encountered during runtime.

