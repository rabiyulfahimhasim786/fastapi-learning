import os
import uuid
import sqlite3
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse

app = FastAPI()

security = HTTPBasic()

# Create SQLite3 database connection
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

# Initialize database schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    filename TEXT NOT NULL,
    url TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    image_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(image_id) REFERENCES images(id) ON DELETE CASCADE
)
''')

conn.commit()

# Define models
class User:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

class Image:
    def __init__(self, id, user_id, filename, url):
        self.id = id
        self.user_id = user_id
        self.filename = filename
        self.url = url

class Comment:
    def __init__(self, id, user_id, image_id, text):
        self.id = id
        self.user_id = user_id
        self.image_id = image_id
        self.text = text

# Helper functions
def get_user_by_email(email):
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    row = cursor.fetchone()
    if row:
        return User(row[0], row[1], row[2], row[3])
    else:
        return None

def get_user_by_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_by_email(credentials.username)
    if user and user.password == credentials.password:
        return user
    else:
        raise HTTPException(status_code=401, detail='Invalid email or password')

def get_image_by_id(image_id):
    cursor.execute('SELECT * FROM images WHERE id = ?', (image_id,))
    row = cursor.fetchone()
    if row:
        return Image(row[0], row[1], row[2], row[3])
    else:
        return None

# Implement user registration route
@app.post('/api/register')
def register(username: str, email: str, password: str):
    user = get_user_by_email(email)
    if user:
        raise HTTPException(status_code=400, detail='Email already registered')
    else:
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        conn.commit()
        return {'message': 'User registered successfully'}

# Implement user login route
@app.post('/api/login')
def login(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_by_credentials(credentials)
    return {'message': 'Logged in successfully', 'user': user.__dict__}

# # Implement image upload route
# @app.post('/api/images')
# @app.post('/api/images')
# def upload_image(file: UploadFile = File(...), user: User = Depends(get_user_by_credentials)):
#     extension = file.filename.split('.')[-1]
#     filename = f'{uuid.uuid4()}.{extension}'
#     url = f'/uploads/{filename}'
#     with open(f'uploads/{filename}', 'wb') as f:
#         f.write(file.file.read())
#     cursor = conn.cursor()
#     cursor.execute('INSERT INTO images (user_id, filename, url) VALUES (?, ?, ?)', (user.id, filename, url))
#     conn.commit()
#     image_id = cursor.lastrowid
#     return {'message': 'Image uploaded successfully', 'image_id': image_id}