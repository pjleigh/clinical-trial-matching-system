# IMPORTS
from tkinter.simpledialog import askstring 
from tkinter import *
from tkinter import messagebox
import math

# adding file dir to path to allow local imports for funcs.py
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
import funcs as f

# READ REQUIRED FILES
trials = f.readictrpcsv()
patientdiagnoses = f.readpatientdiagnosistxt()
patientinfo = f.readpatientinfotxt()

def TrialWindow(foundtrial):
   win = Tk()
   win.title('Trial Window')
   win.geometry("800x500")

   # main
   main_frame = Frame(win)
   main_frame.pack(fill=BOTH, expand=1)

   # canvas
   my_canvas = Canvas(main_frame)
   my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

   # scrollbar
   my_scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
   my_scrollbar.pack(side=RIGHT, fill=Y)

   # configure the canvas
   my_canvas.configure(yscrollcommand=my_scrollbar.set)
   my_canvas.bind(
      '<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all"))
   )

   second_frame = Frame(my_canvas, width = 500, height = 3000)
   
   xtrial = 50
   ystart = 50
   yspacing = 0
   textboxwidth = 60

   # Place all trials
   label = Label(second_frame, text = "Trial Information", font = "Helvetica 10 bold")
   label.place(x=xtrial, y=30)

   for i in range(len(foundtrial)-1):
      textboxheight = math.ceil(len(str(foundtrial[i]))/textboxwidth)

      text = Text(second_frame, width=textboxwidth, height=textboxheight, font = "Helvetica 10")
      text.insert(INSERT, f"{foundtrial[i]}")
      text.config(state=DISABLED)
      text.place(x=xtrial, y=(ystart + yspacing*16 + (i*30)))

      yspacing += textboxheight

   my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
   win.mainloop()

def ClinicianWindow():
   win = Tk()
   win.title('Clinician Window')
   win.geometry("800x500")

   # main
   main_frame = Frame(win)
   main_frame.pack(fill=BOTH, expand=1)

   # canvas
   my_canvas = Canvas(main_frame)
   my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

   second_frame = Frame(my_canvas, width = 800, height = 500)

   patientsearchbutton = Button(second_frame, text = "Patient ID Search", command = PatientShow)
   patientsearchbutton.place(x= 100, y= 200)
   studysearchbutton = Button(second_frame, text = "Clinical Study Search", command = StudyShow)
   studysearchbutton.place(x= 500, y= 200)
      
   my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
   win.mainloop()

def PatientWindow(foundpatient):
   win = Tk()
   win.title('Patient Window')
   win.geometry("1000x500")

   # main
   main_frame = Frame(win)
   main_frame.pack(fill=BOTH, expand=1)

   # canvas
   my_canvas = Canvas(main_frame)
   my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

   # scrollbar
   my_scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
   my_scrollbar.pack(side=RIGHT, fill=Y)

   # configure the canvas
   my_canvas.configure(yscrollcommand=my_scrollbar.set)
   my_canvas.bind(
      '<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all"))
   )

   patientnum = foundpatient[-1]

   # list of all eligible trials
   eligibletrials = []

   for i in range(len(trials)):
      foundtrial = f.checkeligibility(patientinfo, patientnum, patientdiagnoses, trials, i)
      if foundtrial:
         eligibletrials.append(foundtrial)

   second_frame = Frame(my_canvas, width = 1000, height = 28*len(eligibletrials)+100)
      
   xtrial = 550
   xpatient = 50
   ystart = 50
   yspacing = 0
   textboxwidth = 60

   # place eligible trial info in frame
   label = Label(second_frame, text = "Eligible Trials", font = "Helvetica 10 bold")
   label.place(x=xtrial, y=30)

   for i in range(len(eligibletrials)):
      button = Button(second_frame, text=eligibletrials[i][1].split(":")[-1], anchor="w", height=1, width=50, font=("bold", 10), command=lambda c=i: TrialWindow(eligibletrials[c]))
      button.place(x=xtrial, y=i*28+50)

   # place all patient info in frame
   label = Label(second_frame, text = "Patient Information", font = "Helvetica 10 bold")
   label.place(x=xpatient, y=30)

   for i in range(len(foundpatient)-1):
      textboxheight = math.ceil(len(str(foundpatient[i]))/textboxwidth)

      text = Text(second_frame, width=textboxwidth, height=textboxheight, font = "Helvetica 10")
      text.insert(INSERT, f"{foundpatient[i]}")
      text.config(state=DISABLED)
      text.place(x=xpatient, y=(ystart + yspacing*16 + (i*30)))

      yspacing += textboxheight

   my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
   win.mainloop()

   # TODO add patient info in there

# Creates New Login and Stores it into CSV File.
def writeLogin():
   createusername = askstring("Input", "New login ID")
   createpassword = askstring("Input", "New password")

   if not f.createlogin(createusername, createpassword):
      messagebox.showerror('Create login error', 'Error: Invalid input or account already exists!')

# Reads existing login and opens clinician window.
def readLogin():
   existusername = askstring("Input", "Login ID")
   existpassword = askstring("Input", "Password")

   if f.findlogin(existusername, existpassword) == True:
      ClinicianWindow()
   else:
      messagebox.showerror('Login error', 'Error: Invalid input or account does not exist!')

def PatientShow():
   username = askstring("Input", "Input your Patient ID")

   #If patient ID is acceptable move to next window where they can search for clinical trials. If data is already in system they can go straigh into searching, if not they can add any patient info to log in and create a profile.
   foundpatient = f.findpatient(patientinfo, username)

   if foundpatient: 
      PatientWindow(foundpatient)
   else:
      messagebox.showerror('Patient search error', 'Error: Invalid input or patient not found!')

def StudyShow():
   trialID = askstring("Input", "Input the trial ID")

   foundtrial = f.findtrial(trials, trialID)

   if foundtrial: 
      TrialWindow(foundtrial)
   else:
      messagebox.showerror('Trial search error', 'Error: Invalid input or trial not found!')

# This defines the patients choices through clinical study searches. They are only allowed to search for those that are available to them, with n o data on other patients.
def patientoption():
   CB1 = Button(Window, text = "Patient ID Search", command = PatientShow)
   CB1.place(x= 200, y= 125)

# This defines the clinician choices through clinical study searches. They are allowed to both match patients with clinical studies as well as match any single clinical study with a plethora of patients. 
def clinicianoption():
   loginbutton = Button(Window, text = "Clinician Login", command = readLogin)
   loginbutton.place(x= 200, y= 350)
   createloginbutton = Button(Window, text = "Create Login", command = writeLogin)
   createloginbutton.place(x= 200, y= 400)

Window = Tk()
Window.title('Clinical Trial Matching System (CTMS)')
Window.geometry("800x500")

text = Text(Window, width=40, height=1, font = "Helvetica 20 bold")
text.insert(INSERT, "Clinical Trial Matching System (CTMS)")
text.config(state=DISABLED)
text.place(x=100, y = 50)

#Patient Button
B = Button(Window, text ="Patient", command = patientoption, font = 500)
B.place(x=100,y=125)

#Clinician Button
B = Button(Window, text ="Clinican", command = clinicianoption, font = 500)
B.place(x=100,y=375)

Window.mainloop()