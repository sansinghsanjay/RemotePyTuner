# author
__author__ = "Sanjay Singh"
__email__ = "san.singhsanjay@gmail.com"

# libraries
import sys
import imaplib
import getpass
import email
import time
from email.header import decode_header

# importing package files
import controller

# global variables
all_msgID = []
total_msg = 0
keep_waiting = True
M = ''
msg_payload = ''
local_program_file = "local_program_file.py"

# function for updating local_program_file
def update_local_program_file():
    global local_program_file
    f = open(local_program_file, "w")
    f.write(controller.program)
    f.close()

# cleaning received email (removing previous replies from email body)
def get_clean_msg():
    global msg_payload
    program = ''
    chunks = msg_payload.split(">EOM<")
    controller.program = chunks[0]
    chunks = chunks[1].split("\n")
    msg = ""
    for i in range(len(chunks)):
        if(chunks[i].strip() == str(">EOM<")):
            break
        msg = msg + chunks[i].strip() + "\n"
    msg_payload = msg.strip()
    if(msg_payload == '$r'):
        update_local_program_file()

# function for reading new msg
def new_msg():
    global all_msgID, total_msg, keep_waiting, M, msg_payload
    try:
        # for selecting INBOX
        typ, data = M.select("INBOX")
        # getting all mails inside INBOX
        rv, data = M.search(None, "ALL")
        # iterating one by one over all mails in INBOX
        for num in data[0].split():
            # getting response and data
            rv, data = M.fetch(num, '(RFC822)')
            # getting email content
            email_content = data[0][1]
            msg = email.message_from_bytes(email_content)
            # getting email subject
            msg_subject = str(decode_header(msg['Subject'])[0][0])
            # getting Message-ID
            msg_id = msg['Message-ID']
            # appending msg id
            if(msg_id not in all_msgID):
                all_msgID.append(msg_id)
                print(">> Subject: " + msg_subject + " <" + str(time.ctime()) + ">")
                # getting mail text body
                msg_payload = str(msg.get_payload()).strip()
                # removing undesired things (like previous replies)
                get_clean_msg()
                print(">> Message Received: " + msg_payload)
                # finish waiting for new email
                keep_waiting = False
        # getting total number of msgs
        total_msg = len(all_msgID)
    except Exception as e:
        print(">> Process Failed.. <" + str(time.ctime()) + "> " + str(e))

# function for reading mailbox
def read_mailbox():
    global all_msgID, total_msg, keep_waiting, M
    try:
        # for selecting INBOX
        typ, data = M.select("INBOX")
        # getting all mails inside INBOX
        rv, data = M.search(None, "ALL")
        # iterating one by one over all mails in INBOX
        for num in data[0].split():
            # getting response and data
            rv, data = M.fetch(num, '(RFC822)')
            # getting email content
            email_content = data[0][1]
            msg = email.message_from_bytes(email_content)
            # getting Message-ID
            msg_id = msg['Message-ID']
            # appending msg id
            if(msg_id not in all_msgID):
                all_msgID.append(msg_id)
        # getting total number of msgs
        total_msg = len(all_msgID)
        print(">> Message List Initialized <" + str(time.ctime()) + ">")
    except Exception as e:
        print(">> Process Failed.. <" + str(time.ctime()) + "> " + str(e))

# function for checking INBOX
def check_mail():
    global all_msgID, total_msg, keep_waiting, M
    try:
        # for selecting INBOX
        typ, data = M.select("INBOX")
        # getting all mails inside INBOX
        rv, data = M.search(None, "ALL")
        # checking for initial read of mailbox
        if(len(all_msgID) == 0):
            # read available msgs
            read_mailbox()
        if(len(data[0].split()) > total_msg):
            print(">> Received New Message! <" + str(time.ctime()) + ">")
            new_msg()
        if(len(data[0].split()) < total_msg):
            print(">> Re-initializing Message List <" + str(time.ctime()) + ">")
            all_msgID = []
            read_mailbox()
    except Exception as e:
        print(">> Process Failed.. <" + str(time.ctime()) + ">" + str(e))

# main function
def main_function():
    global all_msgID, total_msg, keep_waiting, M, msg_payload
    # initializing global variables
    all_msgID = []
    total_msg = 0
    keep_waiting = True
    M = ''
    msg_payload = ''
    try:
        # reading params files
        params = open("params.txt", "r").read()
        # separating params
        params = params.split(",")
        source_userid = params[0]
        password = params[1]
        target_userid = params[2]
        subject = params[3]
        # gmail email api
        M = imaplib.IMAP4_SSL('imap.gmail.com')
        # making login
        M.login(source_userid, password)
        # checking mailbox (INBOX)
        print(">> Receiving Email: Running...")
        while(keep_waiting == True):
            check_mail()
            if(keep_waiting == False):
                break
            time.sleep(10)
    except imaplib.IMAP4.error:
        print(">> LOGIN FAILED!!! <" + str(time.ctime()) + ">")
