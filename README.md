# Voyage Travel Itinerary ✈️


**University of Texas Rio Grande Valley's Senior Project for Fall Semester 2025**
by Leslie Hurtado, Emma Pacheco, Nathan Perez, and Miguel Garcia. 

🌎Travel Itinerary web app utilizing **Flask, JavaScript, CSS, and HTML.**

## Getting Started

- make sure you have python installed, run this command
```
python --version
```

To clone this project locally,
<details>
<summary>Windows</summary>
  
```bash
git clone https://github.com/lahg1103/SeniorProject.git
cd seniorproject
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python app.py
```
  
</details>
<details>
<summary>MacOS</summary>
  
```bash
git clone https://github.com/lahg1103/SeniorProject.git
cd seniorproject
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
  
</details>

# Contributing to the Repository:


Always, make sure you pull from the working branch, and make sure that your virtual environment is active.
Make sure your requirements are up to date.
```bash
pip install -r requirements.txt
```

## Working With the Database (Development ONLY)

We are working with Flask-SQLAlchemy which is a wrapper for SQLite. This requires Flask-Migrate and Flask-SQLAlchemy libraries in order for this to work.
To get started from scratch, you'll need to have your keys in order.

### How to Generate Secret Keys
```bash
python
import secrets
print(secrets.token_hex(32))
```
#### copy the output

### Create .env file
```bash
touch .env
```
#### Add the following (replace 'YOUR-SECRET-KEY' with the token you generated earlier):
```python
FLASK_SESSION_KEY='YOUR-SECRET-KEY'
```

### Inside app.py under if __name__ == '__main__':
#### Uncomment the following lines before running
```python
    # with app.app_context():
    #     db.create_all()
```
#### Run app.py
```bash
python app.py
```
#### You should see a new folder 'instances/' in the root directory holding your database.

## Updating the Database Schema

Next, we want to make sure you have the most updated database schema available. This is where Flask-Migrate comes in.
The versions of the database are under the migrations directory in the root.

#### Get the latest by running this command

```bash
flask db upgrade
```