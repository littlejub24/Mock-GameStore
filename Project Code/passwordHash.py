import hashlib

# Function to ecnrpyt the passwords using SHA256 in the hashlib Library
    # Takes in the password and returns a hashed version
def hash_password(provided_password):
    h = hashlib.new("SHA256")
    h.update(provided_password.encode())
    password_hash = h.hexdigest()
    return password_hash
   
if __name__ == "__main__":
    # h = hashlib.new("SHA256")
    # correct_password = "MyPassword123567"
    # h.update(correct_password.encode())

    # password_hash = h.hexdigest()
    # print(password_hash)

    # user_input = "MyPassword123567"
    # h = hashlib.new("SHA256")
    # h.update(user_input.encode())
    # input_hash = h.hexdigest()

    # print(h.hexdigest())

    print(hash_password("12345"))
