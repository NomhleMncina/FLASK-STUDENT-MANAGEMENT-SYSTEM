from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
password = "Password@123"  # sample password
hashed = bcrypt.generate_password_hash(password).decode("utf-8")
print(hashed)