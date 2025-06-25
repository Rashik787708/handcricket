# Hand Cricket Game with Login System and SQLite
# ------------------------------------------------
# This program allows users to register, login, play hand cricket,
# and track their high scores and number of wins.

import random
import sqlite3

# Connect to SQLite database
con = sqlite3.connect('handcricket.db')
cur = con.cursor()

# Create table if not exists
cur.execute('''
CREATE TABLE if not exists users (
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    gmail varchar(80) not null,
    highscore int not null,
    security_question varchar(500) not null,
    security_answer varchar(500) not null,
    wins int not null
)
''')

# Initialize global variables
sum1 = sum2 = sum3 = sum4 = sum5 = sum6 = sum7 = sum8 = 0
username1 = ''

# Function to reset forgotten password
def forgot_password():
    username = input("Enter Your Username: ")
    cur.execute("SELECT security_question FROM users WHERE username=?", (username,))
    result = cur.fetchone()
    if not result:
        print("Username Not Found.")
        return
    print('Security Question:', result[0])
    security_answer = input("Enter Your Answer: ")
    cur.execute("SELECT * FROM users WHERE username=? AND security_answer=?", (username, security_answer))
    user = cur.fetchone()
    if not user:
        print("Incorrect answer.")
        forgot_password()
        return
    new_password = input("Enter New Password: ")
    confirm_password = input("Confirm New Password: ")
    if new_password != confirm_password:
        print("Passwords Do Not Match.")
        return
    cur.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
    con.commit()
    print("Password Reset Successfully!")

# Function to log in
def login():
    global username1
    username1 = input("Enter Username: ")
    password = input("Enter Password: ")
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username1, password))
    user = cur.fetchone()
    if user:
        print("\t\t\t\t Login Successful!")
        welcome(username1)
        toss()
    else:
        print("Invalid Username Or Password.")

# Welcome user and display score and wins
def welcome(username1):
    print("\t\t\t\t Welcome!", username1)
    cur.execute('SELECT highscore FROM users WHERE username=?', (username1,))
    result1 = cur.fetchall()
    print('\t\t\t\t Your Last High Score:', result1[0][0])
    cur.execute('SELECT wins FROM users WHERE username=?', (username1,))
    result2 = cur.fetchall()
    print('\t\t\t\t Your Total Wins:', result2[0][0])

# Validate email format
def mail(gmail):
    if gmail.count('@') == 1 and gmail.endswith('.com'):
        return 'valid'
    else:
        print('Invalid Email')
        sign_up()

# Create new user account
def sign_up():
    username = input("Enter new username: ")
    password = input("Enter new password: ")
    confirm_password = input("Confirm new password: ")
    gmail = input('Enter Gmail: ').lower().strip()
    mail(gmail)
    sq = input('What Is Your Favorite Colour: ')
    highscore = 0
    win = 0
    if password != confirm_password:
        print("Passwords Do Not Match.")
        sign_up()
        return
    try:
        cur.execute('INSERT INTO users (username,password,gmail,highscore,security_question,security_answer,wins) VALUES (?,?,?,?,?,?,?)',
                    (username, password, gmail, highscore, 'what is your favorite colur', sq, win))
        con.commit()
        print("User Registered Successfully!")
    except sqlite3.IntegrityError:
        print("Username Already Taken.")

# Update wins after user victory
def wins():
    global username1
    cur.execute('UPDATE users SET wins = wins + 1 WHERE username = ?', (username1,))
    con.commit()
    cur.execute('SELECT wins FROM users WHERE username=?', (username1,))
    r1 = cur.fetchall()
    print('\t\t\t\t Your Total Wins:', r1[0][0])

# Update high score if new score is greater
def highscore(sumx):
    global username1
    cur.execute('SELECT highscore FROM users WHERE username=?', (username1,))
    r1 = cur.fetchall()
    if sumx > r1[0][0]:
        cur.execute('UPDATE users SET highscore=? WHERE username=?', (sumx, username1))
        con.commit()
        print('\t\t\t\t Your New High Score:', sumx)
    else:
        print('\t\t\t\t Your Existing High Score:', r1[0][0])

# Main toss function
def toss():
    print('Here Is Toss Choose Odd And Even')
    ch1 = input('Enter Odd or Even: ').lower()
    if ch1 not in ['odd', 'even']:
        print('Invalid Choice')
        toss()
        return
    ch2 = 'even' if ch1 == 'odd' else 'odd'
    print('The Game Is Based On The Score 1-6')
    print('Computer Choice:', ch2)
    tr = int(input('Enter Runs For Toss (1-6): '))
    if not (1 <= tr <= 6):
        print('The Runs Is Wrong')
        toss()
        return
    tr1 = random.randint(1, 6)
    print('Computer Run For Toss:', tr1)
    total = tr + tr1
    if (total % 2 == 0 and ch1 == 'even') or (total % 2 != 0 and ch1 == 'odd'):
        print('You Won The Toss')
        tc = input('Choose Bat Or Bowl: ').lower()
        if tc == 'bat':
            ubat()
        elif tc == 'bowl':
            ubowl()
    else:
        print('Computer Won The Toss')
        tu = random.choice(['bat', 'bowl'])
        print(f'Computer Chose To {tu.capitalize()}')
        if tu == 'bat':
            cbat()
        else:
            cbowls()

# Batting functions (user/computer first innings)
# ... [rest of functions: ubat, ubat1, ubowl, ubowl1, cbat, cbat1, cbowls, cbowls1, superover]
# Will be filled similarly with comments

# Game Start Menu
print('\n\t\t\t\t Welcome to Hand Cricket!\n')
print('''\t\t\t Get ready to experience the thrill of hand cricket like never before!
\t\t\t We're excited to have you join our community of players.
\t\t\t Whether you're a seasoned pro or a newbie,
\t\t\t there's fun and excitement waiting for you.
\t\t\t Gear up, play fair, and show off your best moves. May the best player win!
\t\t\t Enjoy the game,\n\t\t\t The Hand Cricket Team''')

# Main menu loop
while True:
    print('\n1. Create Account')
    print('2. Login')
    print('3. Reset Password')
    print('4. Exit The Game')
    m = input('Enter Your Choice (1/2/3/4): ')
    if m == '1':
        sign_up()
    elif m == '2':
        login()
    elif m == '3':
        forgot_password()
    elif m == '4':
        print('\t\t\t\t Game Ends')
        break
    else:
        print('Invalid Choice. Try Again.')
