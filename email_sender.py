# author
__author__ = "Sanjay Singh"
__email__ = "san.singhsanjay@gmail.com"

# libraries
import smtplib
import time
from email.mime.text import MIMEText

# importing package files
import controller

# global constant
global program, local_program_file

# function to read program of local file
def get_local_file_program():
    global program, local_program_file
    local_program_file = "local_program_file.py"
    program = open(local_program_file, "r").read()

# function for sending program status
def send_status(msg):
    global program
    # reading params files
    params = open("params.txt", "r").read()
    # getting program from local_program_file
    get_local_file_program()
    # separating params
    params = params.split(",")
    source_userid = params[0]
    password = params[1]
    target_userid = params[2]
    subject = params[3]
    port = params[4]
    # adding control information in msg
    msg = program + "\n>>>>>>OUTPUT STATUS<<<<<\n" + msg + "\n\n>>>>>CONTROLS<<<<<\nReply with:\n'$q' to quit program\n'$r' to re-execute program\n'$sq' to save current program and quit"
    msg = msg + "\nWhile replying keep CONTROLS between '>EOM<'"

    # creating a text/plain message
    email_body = MIMEText(msg)

    # making email body
    email_body['Subject'] = subject
    email_body['From'] = source_userid
    email_body['To'] = target_userid

    # sending status
    server = smtplib.SMTP('smtp.gmail.com:' + str(port))
    server.ehlo()
    server.starttls()
    server.login(source_userid, password)
    server.send_message(email_body)
    server.quit()
    print(">> Status Sent <" + str(time.ctime()) + ">")
