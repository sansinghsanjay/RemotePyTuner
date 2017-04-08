# RemotePyTuner

Its a Python project which can help to Python programmers (or specifically to Data Scientists) to remotely manage the execution of Python programs.



## SERVICES

This project provides following services:

1. You can get the final output of your Python program on your email id.

2. If you didn't get desired output from your program then you can modify your program and send that modified program in reply of received email (in step 1) to execute the modified program.

3. Above two steps could be repeat up to any number of time till you don't stop the execution by sending an email.


## MOTIVATIONS

While participating in Data Science competitions like in Kaggle, participants have to tune their Python or R program a lot just to get very little improvement (mostly less than 0.1%) in accuracies (or in results). Generally, tuning a program requires very little changes in it, like changing learning rate, number of layer, number of neurons, optimization function, changing model (in case of Statistical models), etc.
These programs runs for a long time and then gives an output which might not be as per our expectations. In current scenario, we have to sit for that long time, waiting for output and then we do very small modifications (or tuning) in program and execute it. This time consuming process repeats again and again. So, a better approach is to get final output on your email which we can access on our smartphone and if we don't like the outputs, we can modify (or tune) the program and again execute it on our local machine just by sending an email.



## PLATFORM USED

Developed and tested with Python3 (version 3.5.2) on Ubuntu - 14.04 and Ubuntu - 16.04



## HOW TO USE THIS?

1. Follow this tutorial to install Python gmail API in your system: 
https://developers.google.com/gmail/api/quickstart/python

2. Install that following Python packages on your system:
sys, imaplib, getpass, time, email, smtplib, os

3. This project requires two gmail user id: source_userid@gmail.com and target_userid@gmail.com. source_userid@gmail.com will be used to send the final output of your program to target_userid@gmail.com. Then, you can reply from target_userid@gmail.com to take desired actions on your Python program. For this you have to allow less secure apps to access your source_userid@gmail.com. You can do this by following these steps:
3.i. Click on your profile pic at right top of your gmail account. A pop-up opens, click on "My Account" in that pop-up.
3.ii. A new tab will open. Now click on "Sign-in & Security". 
3.iii. In new page, scroll down to the bottom of page, turn "ON" the "Allow less secure apps" option.  

PERFORM STEP 1, 2 and 3 ONLY ON FIRST USE.

4. Include "import sys" in your Python program.

5. Include the following line in your program after all imports:
sys.path.insert(0, "/path/to/RemotePyTuner/")

6. Include following line just after the line given in step-2:
import email_sender

7. At last of your program (to get the final outputs), add following line:
email_sender.send_status(your_msg_in_string_type)

8. Open terminal and run the following command:
$ cd /path/to/RemotePyTuner/
$ python3 controller.py

9. controller.py will execute and asks for following things:
```python
>> MAIN MENU
>> Enter the path of Python program file : /path/of/your/Python/program
>> Enter source gmail user-id : source_userid@gmail.com
>> Enter password of source gmail account : *#@$!
>> Enter port for communication (to use default, enter 587) : 587
>> Checking login..
>> Login successful
>> Enter target gmail user-id : target_userid@gmail.com
>> Enter subject for email notifications : subject_of_your_choice
>> Choose your platform:
>>		Enter 'p' for 'python3'
>>		Enter 'i' for 'ipython3' (X receiving_mail would not work X)
>> 	Enter your choice : p # Currently there are bugs with 'ipython3' so use 'python3'
```

10. After above steps, your Python program starts executing. Once it gets completed, you will receive an email on your target_userid@gmail.com from your source_userid@gmail.com with subject subject_of_your_choice. The body of this email would be like:
```python
Your
-"-
-"-
Python
-"-
-"-
Program

>>>>>>OUTPUT STATUS<<<<<
your_msg_in_string_type

>>>>>CONTROLS<<<<<
Reply with:
'$q' to quit program
'$r' to re-execute program
'$sq' to save current program and quit
While replying keep CONTROLS between '>EOM<'
```

11. Now there might be following three cases:

  i. You want to quit your Python program execution. In this case, reply in received email with message:
  ```python
  >EOM<
  $q
  >EOM<
  ```

  ii. You want to modify your program and re-execute it. Reply in received email with message like:
  ```python
  Your
  -"-
  -"-
  Modified
  -"-
  -"-
  Python
  -"-
  -"-
  Program
  >EOM<
  $r
  >EOM<
  ```

  All modifications will happen on a shadow copy of file provided by user.

  iii. You are satisfy with the outputs you received on email, so you want to save your modified program in your         /path/of/your/Python/program permanently and quit (or terminate) the program. So, reply would be like:
  ```python
  >EOM<
  $sq
  >EOM<
  ```

12. NOTE: Currently this project don't have any fault tolerance. So, please be careful while using this. Any wrong operation crashes this program. 



## SCOPE OF IMPROVEMENT

1. No fault tolerance and no validation of user input.
2. We cannot execute our program in ipython.
3. Memory management: Because a program and its modified copy will execute in same session. So, there is a need to free memory of all variables before executing modified program.
4. This thing can be extend for other languages, specially for R.
