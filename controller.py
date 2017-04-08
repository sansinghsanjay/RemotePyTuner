# author
__author__ = "Sanjay Singh"
__email__ = "san.singhsanjay@gmail.com"

# libraries
import os
from getpass import getpass
import smtplib
import time
import sys

# importing PyProgramController files
import receiving_mail

# global parameters
global local_program_file, program_file, program, source_userid, password, target_userid, subject, port, msg_payload

# creating duplicate copy of program file
def create_local_program_file():
    global local_program_file, program_file, program
    if(program_file[0] == "'"):
        program_file = program_file[1 : len(program_file) - 1]
    program = open(program_file, "r").read()
    f = open(local_program_file, "w")
    f.write(program)
    f.close()

# function for checking user-id and password
def check_login():
    try:
        print(">> Checking login...")
        # sending status
        server = smtplib.SMTP('smtp.gmail.com:' + str(port))
        server.ehlo()
        server.starttls()
        server.login(source_userid, password)
        print(">> Login successful")
    except Exception as e:
        print(">> Login Failed.. <" + str(time.ctime()) + "> " + str(e))
        sys.exit()

# function to temporarily save global variables
def save_params():
    # opening a text file in write mode
    temp = open("params.txt", "w")
    # writing params
    temp.write(source_userid + "," + password + "," + target_userid + "," + subject + "," + port)
    # closing text file
    temp.close()

if __name__ == "__main__":
    # accessing global variables
    global local_program_file, program_file, source_userid, password, target_userid, subject, port, msg_payload
    local_program_file = "local_program_file.py"

    # MAIN MENU
    take_order = True
    while(take_order == True):
        print(">> MAIN MENU")
        program_file = input(">> Enter the path of Python program file : ")
        source_userid = input(">> Enter source gmail user-id : ")
        password = getpass(">> Enter password of source gmail account : ")
        port = input(">> Enter port for communication (to use default, enter 587) : ")
        # checking login status
        check_login()
        target_userid = input(">> Enter target gmail user-id : ")
        subject = input(">> Enter subject for email notifications : ")
        # temporarily saving params (user-id, password)
        save_params()
        # asking for platform (python3 or ipython3)
        print(">> Choose your platform : ")
        print(">> \t\tEnter 'p' for 'python3'")
        print(">> \t\tEnter 'i' for 'ipyhton3' (X receiving_mail would not work X)")
        ide = input(">> \tEnter your choice : ")
        # if choosed platform is 'p' or 'i' then continue else ask again
        if(ide == 'p' or ide == 'i'):
            take_order = False
        else:
            print(">> Invalid choice. Try Again...")
            time.sleep(2)
            os.system("clear")
    # to keep number of executions
    nbr_exec = 1
    # creating local program file
    create_local_program_file()
    # executing user program
    while(True):
        print("")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<")
        print(">>>>>>>>>>>>>>>>>>Exceution " + str(nbr_exec) + "<<<<<<<<<<<<<<<<<<<<<")
        if(ide == 'i'):
            os.system("ipython3 -i " + local_program_file)
        if(ide == 'p'):
            os.system('python3 ' + local_program_file)
            # waiting for next instructions
            receiving_mail.main_function()
            # getting msg Received
            msg_payload = str(receiving_mail.msg_payload)
            # received response says to quit program
            if(msg_payload.strip() == '$q'):
                print(">> Quitting...")
                break
            # received response says to re-execute program
            if(msg_payload.strip() == '$r'):
                print(">> Re-executing user-program...")
                time.sleep(2)
                print("")
            # received response says to save user-program and quit
            if(msg_payload.strip() == '$sq'):
                print(">> Saving recently updated program...")
                program = open(local_program_file, "r").read()
                f = open(program_file, "w")
                f.write(program)
                f.close()
                print(">> Program saved")
                print(">> Quitting...")
                break

        nbr_exec = nbr_exec + 1

    # deleting temporary params file
    os.remove("params.txt")

    # deleting temporary program file
    os.remove(local_program_file)
