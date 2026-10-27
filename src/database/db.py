from src.database.config import supabase
import bcrypt

def hash_pass(password: str) -> str:
    # Hash the password using bcrypt.
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def check_pass(password: str, hashed: str) -> bool:
    # Check if the provided password matches the hashed password.
    return bcrypt.checkpw(password.encode(), hashed.encode())

def check_teacher_exists(username: str) -> bool:
    # Check if a teacher with the given username exists in the database.
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0

def create_teacher(username: str, password: str, name: str) -> bool:
    # Insert the new teacher into the database.
    data = {"username": username, "password": hash_pass(password), "name": name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data

def teacher_login(username: str, password: str) -> bool:
    # Check if the teacher exists and the password matches.
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher["password"]):
            return teacher
    return None

def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data