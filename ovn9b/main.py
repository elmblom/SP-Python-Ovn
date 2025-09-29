import json

class colors:
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    magenta = '\033[95m'
    cyan = '\033[96m'
    end = '\033[0m'

def greet():
    print(f"{colors.cyan}Welcome! What would you like to do?{colors.end}")
    print(f"{colors.blue}1 - Login{colors.end}")
    print(f"{colors.blue}2 - Sign up{colors.end}")
    print(f"{colors.blue}3 - Exit{colors.end}")
    actopt = int(input(f"{colors.yellow}Select An option By Entering It's Corresponding Number: {colors.end}"))
    if actopt == 1:
        login()
    elif actopt == 2:
        signup()
    elif actopt == 3:
        exit
    else:
        print(f"{colors.red}Invalid Option{colors.end}")
        greet()
    
def login():
    global userid
    attempts = 3
    while attempts > 0:
        UN = input(f"{colors.cyan}Enter your username: {colors.end}")
        PW = input(f"{colors.cyan}Enter your password: {colors.end}")
        with open("customers.json", "r") as f:
            users = json.load(f)
        for x in users:
            if x["un"] == UN and x["pw"] == PW:
                userid = x["uid"]
                print(f"{colors.green}Logged in as {x['un']}!{colors.end}")
                actions()
                return
        attempts -= 1
        print(f"{colors.red}Invalid credentials. You have {attempts} attempt(s) left.{colors.end}")
    print(f"{colors.red}Too many failed attempts. Exiting...{colors.end}")
    exit

def signup():
    with open("customers.json", "r") as f:
            users = json.load(f)
    while True:
        UN = input(f"{colors.cyan}Enter a username: {colors.end}")
        if any(x["un"] == UN for x in users):
            print(f"{colors.red}Username Taken! Please choose another one{colors.end}")
            continue
        else:
            TN = input(f"{colors.cyan}Enter your phone number: {colors.end}")
            PW = input(f"{colors.cyan}Enter a password: {colors.end}")
            while True:
                if PW == input(f"{colors.cyan}Enter password again for confirmation: {colors.end}"):
                    break
                else:
                    print(f"{colors.red}Passwords do not match!{colors.end}")
                    return
        break
    with open("customers.json", "w+") as f:
        new_user = {
            "un": UN,
            "tn": TN,
            "pw": PW,
            "uid": len(users),
            "loans": []
        }
        users.append(new_user)
        f.seek(0)
        json.dump(users, f, indent=4)
        f.truncate()
        print(f"{colors.green}Account created succesfully!{colors.end}")
        login()
                        
def actions():
    print(f"{colors.blue}1 - Loan{colors.end}")
    print(f"{colors.blue}2 - Return{colors.end}")
    print(f"{colors.blue}3 - Exit{colors.end}")
    actopt = int(input(f"{colors.yellow}Select An option By Entering It's Corresponding Number: {colors.end}"))
    if actopt == 1:
        loan()
    elif actopt == 2:
        returnmovie()
    elif actopt == 3:
        exit
    else:
        print(f"{colors.red}Invalid Option{colors.end}")
        actions()

def loan():
    while True:
        with open("./movies.json", "r") as f:
            data = json.load(f)   
        print(f"{colors.magenta}Available Titles Are Green:{colors.end}")
        i = 0
        for x in data:
            if x["Available"] == 1:
                print("{}{} - {} by {} released {}{}".format(colors.green, i, x["Title"],x["Director"],x["Year"], colors.end))
            else:
                print("{}{} - {} by {} released {}{}".format(colors.red, i, x["Title"],x["Director"],x["Year"], colors.end))
            i+=1      
        usel = int(input(f"{colors.yellow}Choose A Title By Entering It's Corresponding Number: {colors.end}"))
        if usel >= i:
            print(f"{colors.red}No movie with that id!{colors.end}")
            continue
        elif data[usel]["Available"] == 0:
            print(f"{colors.red}That title is not available!{colors.end}")
            continue
        else:
            break
    with open("./movies.json", "r+") as f: 
        data = json.load(f)
        movie_title = data[usel]["Title"]
        data[usel]["Available"] = 0
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    with open("./customers.json", "r+") as f:
        customers = json.load(f)
        customers[userid]["loans"].append(usel)
        f.seek(0)
        json.dump(customers, f, indent=4)
        f.truncate()
    
    print(f"{colors.green}Successfully loaned: {movie_title}!{colors.end}")
    actions()
    
        
def returnmovie():
    with open("./customers.json", "r") as f:
        customers = json.load(f)
        loans = customers[userid]["loans"]
    
    while True:
        if len(loans) == 0:
            print(f"{colors.yellow}No loaned titles{colors.end}")
            actions()
            break
        with open("./customers.json", "r+") as f:
            customers = json.load(f)
            loans = customers[userid]["loans"]
        with open("./movies.json", "r+") as f:
            data = json.load(f)
            print(f"{colors.magenta}Loaned Movies:{colors.end}")
            for x in loans:
                print("{}{} - {} by {} released {}{}".format(colors.yellow, x, data[x]["Title"],data[x]["Director"],data[x]["Year"], colors.end))
            retsel = int(input(f"{colors.yellow}Enter the number corresponding to the movie you want to return: {colors.end}"))
            if retsel in loans:
                data[retsel]["Available"] = 1
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                f.close()
                with open("./customers.json", "r+") as f:
                    loans.remove(retsel)
                    customers[userid]["loans"] = loans
                    f.seek(0)
                    json.dump(customers, f, indent=4)
                    f.truncate()
                    print(f"{colors.green}Thank you for returning that title!{colors.end}")
                    if input(f"{colors.cyan}Would you like to return more titles? 0/1{colors.end}") == "1":
                        continue
                    else:
                        actions()
                        break
            else:
                print(f"{colors.red}You don't have a loaned title with that id!{colors.end}")
                continue
                
greet()