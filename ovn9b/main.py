import json

def greet():
    print("Welcome! What would you like to do?")
    print("0 - Login")
    print("1 - Sign up")
    print("2 - Exit")
    actopt = int(input("Select An option By Entering It's Corresponding Number: "))
    if actopt == 0:
        login()
    elif actopt == 1:
        signup()
    elif actopt == 2:
        exit
    else:
        print("Invalid Option")
        greet()
    
def login():
    attempts = 3
    while attempts > 0:
        UN = input("Enter your username: ")
        PW = input("Enter your password: ")
        with open("customers.json", "r") as f:
            users = json.load(f)
        for x in users:
            if x["un"] == UN and x["pw"] == PW:
                UID = x["uid"]
                print("Logged in as {}!".format(x["un"]))
                actions()
                return
        attempts -= 1
        print(f"Invalid credentials. You have {attempts} attempt(s) left.")
    print("Too many failed attempts. Exiting...")
    exit

def signup():
    with open("customers.json", "r") as f:
            users = json.load(f)
    while True:
        UN = input("Enter a username: ")
        if any(x["un"] == UN for x in users):
            print("Username Taken! Please choose another one")
            continue
        else:
            TN = input("Enter your phone number: ")
            PW = input("Enter a password: ")
            while True:
                if PW == input("Enter password again for confirmation: "):
                    break
                else:
                    print("Passwords do not match!")
                    return
        break
    with open("customers.json", "w+") as f:
        new_user = {
            "un": UN,
            "tn": TN,
            "pw": PW,
            "uid": len(users) + 1
        }
        users.append(new_user)
        f.seek(0)
        json.dump(users, f, indent=4)
        f.truncate()
        print("Account created succesfully!")
        login()
                        
def actions():
    print("0 - Loan")
    print("1 - Return")
    print("2 - View Account Info")
    print("3 - Exit")
    actopt = int(input("Select An option By Entering It's Corresponding Number: "))
    if actopt == 0:
        loan()
    elif actopt == 1:
        returnmovie()
    elif actopt == 2:
        viewinfo()
    elif actopt == 3:
        exit
    else:
        print("Invalid Option")
        actions()

def loan():
    while True:
        with open("./movies.json", "r") as f:
            data = json.load(f)   
        print("Available Titles:")
        i = 0
        for x in data:
            if x["Available"] == 1:
                print("{} - {}".format(i,x["Title"]))
                i+=1      
        usel = int(input("Choose A Title By Entering It's Corresponding Number: "))
        if usel > i-1:
            print("No movie with that id!")
            continue
        else:
            break
    with open("./movies.json", "w+") as f:
    

greet()