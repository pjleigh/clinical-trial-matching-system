from tkinter.simpledialog import askinteger 
from tkinter.simpledialog import askstring 
from tkinter.simpledialog import askfloat 
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
# adding file dir to path to allow local imports
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
import funcs as f

trials = f.readictrpcsv()
patientdiagnoses = f.readpatientdiagnosistxt()
patientinfo = f.readpatientinfotxt()

testtrials = f.readictrpcsv()

Window = Tk()

Window.geometry("500x500")

frame = Frame(Window, width=200, height=200)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

img = ImageTk.PhotoImage(Image.open("GokuGoesHard.jpg"))

label = Label(frame, image = img)
label.pack()

# TODO include ttk.Style and ttk.Font for fanciness

def TrialWindow(foundtrial):
   win = Tk()
   win.geometry("500x500")

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

   second_frame = Frame(my_canvas, width = 500, height = 500)
      
   label = Label(second_frame, text = f"Trial ID: {foundtrial[0]}", font = "Helvetica 10 bold", anchor="nw")
   label.place(x=200, y=30)
   label = Label(second_frame, text = f"Trial ID: {foundtrial[0]}", font = "Helvetica 10 bold", anchor="nw")
   label.place(x=200, y=30)

   # TODO finish putting in trial info as labels

   my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
   win.mainloop()
         
#Creates New Login and Stores it into CSV File.
def writeLogin():
   createusername = askstring("Input", "New login ID")
   createpassword = askstring("Input", "New password")

   if not f.createlogin(createusername, createpassword):
      messagebox.showerror('Create login error', 'Error: Account already exists!')

def readLogin():
   existusername = askstring("Input", "Login ID")
   existpassword = askstring("Input", "Password")

   if f.findlogin(existusername, existpassword) == True:
      ClinicianWindow()
   else:
      messagebox.showerror('Login error', 'Error: Invalid input or account does not exist!')

def ClinicianWindow():
   win = Tk()
   win.geometry("500x500")

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

   second_frame = Frame(my_canvas, width = 500, height = 500)

   patientsearchbutton = Button(second_frame, text = "Patient ID Search", command = PatientShow)
   patientsearchbutton.place(x= 175, y= 375)
   studysearchbutton = Button(second_frame, text = "Clinical Study Search", command = StudyShow)
   studysearchbutton.place(x= 175, y= 400)
      
   my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
   win.mainloop()

def PatientWindow(foundpatient):
   win = Tk()
   win.geometry("2000x1000")

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

   patientID = foundpatient[-1]
   patientnum = f.findpatient(patientinfo, patientID)

   # list of all eligible trials
   eligibletrials = []

   for i in range(len(trials)):
      foundtrial = f.checkeligibility(patientinfo, patientnum, patientdiagnoses, trials, i)
      if foundtrial:
         eligibletrials.append(foundtrial)

   second_frame = Frame(my_canvas, width = 1000, height = 28*len(eligibletrials)+100)
      
   label = Label(second_frame, text = "Eligible Trials", font = "Helvetica 10 bold")
   label.place(x=200, y=30)

   for i in range(len(eligibletrials)):
      button = Button(second_frame, text=eligibletrials[i][1], anchor="w", height=1, width=50, font=("bold", 10), command=lambda c=i: print(eligibletrials[c][1]))
      button.place(x=200, y=i*28+50)

   my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
   win.mainloop()

   # TODO add patient info in there

def PatientShow():
   username = askstring("Input", "Input your Patient ID")
   #If patient ID is acceptable move to next window where they can search for clinical trials. If data is already in system they can go straigh into searching, if not they can add any patient info to log in and create a profile.
   foundpatient = f.findpatient(patientinfo, username)

   if foundpatient: 
      PatientWindow(foundpatient)
   else:
      messagebox.showerror('Patient search error', 'Error: Patient not found!')

def StudyShow():
   trialID = askstring("Input", "Input the trial ID")

   foundtrial = f.findtrial(trials, trialID)

   if foundtrial: 
      TrialWindow(foundtrial)
   else:
      messagebox.showerror('Trial search error', 'Error: Trial not found!')

# This defines the patients choices through clinical study searches. They are only allowed to search for those that are available to them, with n o data on other patients.
def patient():
   CB1 = Button(Window, text = "Patient ID Search", command = PatientShow)
   CB1.place(x= 175, y= 125)

# This defines the clinician choices through clinical study searches. They are allowed to both match patients with clinical studies as well as match any single clinical study with a plethora of patients. 
def clinician():
   loginbutton = Button(Window, text = "Clinician Login", command = readLogin)
   loginbutton.place(x= 175, y= 375)
   createloginbutton = Button(Window, text = "Create Login", command = writeLogin)
   createloginbutton.place(x= 175, y= 400)

#Patient Button
B = Button(Window, text ="Patient", command = patient, font = 500)
B.place(x=100,y=125)

#Clinician Button
B = Button(Window, text ="Clinican", command = clinician, font = 500)
B.place(x=100,y=375)

Window.mainloop()