from passlib.hash import bcrypt

plain_password = ""
hashed = bcrypt.hash(plain_password)
print("Hashed password:", hashed)
