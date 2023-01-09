#SensitiveInformation is another 'PY' file that contains sensitive information.

# Selenium Web Kit  
import csv
import glob
from xml.etree.ElementTree import tostring
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec 
from selenium.webdriver.common.by import By


# Imports
import time # Time kit
import os, os.path  # OS kit
from os.path import join
import sys  # Sys for system exit
from tkinter import *   # Python GUI library
from tkinter import messagebox  # Error message box
from pathlib import Path
import SensitiveInformation
from urllib.parse import urlparse #for slicing the domain from the URL


cwd = os.getcwd()   # Get current working directory
sleepDuration = 3   # Seconds to sleep between actions

# _________________________________User Interface________________________________

# GUI class
class App(Frame):   # Object oriented class structure to avoid global variables
    def __init__(self, title, geometry, master):
        Frame.__init__(self, master)    # Initialize base class

        # Intialize GUI settings
        self.master = master
        self.master.title(title)
        self.master.geometry(geometry)
        self.master.resizable(False, False)

        self.uservar = StringVar()  # Variable to store Dashboard username
        self.passvar = StringVar()  # Variable to store Dashboard password
        self.namevar = StringVar() # Variable to store analyst's name

        # Title
        self.title = Label(text="GnomeFree ION", font=("Helvetica", 16))
        self.title.place(x=90, y=10)
        self.instruc = Label(text="Please enter Username, Password and Name:", font=("Arial", 10))
        self.instruc.place(x=75, y=45)

        # Username field           
        self.userlbl = Label(master, text="Username", font=("Arial", 10))
        self.userlbl.place(x=164, y=80)
        self.usertxt = Entry(master, textvariable=self.uservar)
        self.usertxt.place(x=135, y=100)
        self.usertxt.focus()

        # Password field
        self.passlbl = Label(master, text="Password", font=("Arial", 10))
        self.passlbl.place(x=164, y=130)
        self.passtxt = Entry(master, show='*', textvariable=self.passvar)
        self.passtxt.place(x=135, y=150)

        # Name field
        self.namelbl = Label(master, text="Name", font=("Arial", 10))
        self.namelbl.place(x=164, y=180)
        self.nametxt = Entry(master, textvariable=self.namevar)
        self.nametxt.place(x=135, y=200)

        # Login button
        def login_attempt(event=None):
            if len(app.usertxt.get()) != 0 and len(app.passtxt.get()) != 0 and len(app.nametxt.get()) != 0:
                root.destroy()
            else:
                messagebox.showerror("Error", "Please enter all fields")

        self.lgnbtn = Button(root, text="Run", font=("Arial", 10), bg="red", command=login_attempt)
        self.lgnbtn.place(x=170, y=230, height=35, width=50)
        root.bind('<Return>', login_attempt)
                
        # GUI window close handling
        def close_GUI():
            root.destroy()
            sys.exit()

        # Exit program if GUI window is closed
        root.protocol('WM_DELETE_WINDOW', close_GUI) 

# Run GUI in main
root = Tk()

# root.iconbitmap(cwd + "\\rsa_logo.ico")
app = App("GnomeFree", '450x300', root) # Call App class
root.mainloop() # Run GUI loop

# _______________________Pull Freenome table from Dashboard______________________

# Find Chrome path
target_file = "chrome.exe"  # Target file search is looking for chrome

for root, dirs, files in os.walk('C://'):   # Search whole C drive
    if target_file in files:
        chrome_path = join(root, target_file)   # Save filepath to var
        break

# Set driver options
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.binary_location = chrome_path
options.add_argument('--disable-blink-features=AutomationControlled')
# options.page_load_strategy = "none"
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)

# Function to click Web Elements
def webClicker(xpathOfElement, sleep):
    time.sleep(sleep)
    actionForJS = browser.find_element(by=By.XPATH, value=xpathOfElement)
    actionForJS.click()

# Navigate to Dashboard
browser.get(SensitiveInformation.navDict['Dashboard'])

# Login to Dashboard
WebDriverWait(browser, int(30)).until(ec.presence_of_element_located((By.NAME, 'username')))    # Wait for page to load
time.sleep(3)

# Enter username
actionForJS = browser.find_element(by=By.NAME, value=('username'))
actionForJS.send_keys(SensitiveInformation.username)
time.sleep(3)

# Enter password
actionForJS = browser.find_element(by=By.NAME, value=('password'))  
actionForJS.send_keys(SensitiveInformation.password)

webClicker(SensitiveInformation.clickDict['Login Button'], sleepDuration*3)

# Navigate to "Search Bar"
WebDriverWait(browser, int(30)).until(ec.presence_of_element_located((By.XPATH, SensitiveInformation.loaderDict['Search Bar'])))

browser.get(SensitiveInformation.navDict['Search Bar'])

# Click on Buttons in order to download CSV file    
for key, val in SensitiveInformation.clickDict.items():
    if key == 'Login Button':continue
    webClicker(val, sleepDuration)

#_______________________Extract relevant values from CSV________________________

time.sleep(sleepDuration*4)

# Gets latest file in folder (latest file is: files[0])
files_path = os.path.join(SensitiveInformation.downloadsFolderClean, '*')
files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True) 

# create a dictionary
csvDictionary = {}

# Set the file paths
csvFilePath = Path(files[0])
     
# Open a csv reader called DictReader
with open(csvFilePath, encoding='utf-8') as csvFile:
    csvReader = csv.DictReader(csvFile)
         
    # Convert each row into a dictionary and add it to data
    for rows in csvReader:
        # Set the primary key
        key = rows['Element ID']
        csvDictionary[key] = rows

# Recursive function that iterates over dict, yields values containing TLDarr[i]
def dictIterator(dict_obj):
    # Iterate over all key-value pairs of dict argument
    for key, value in dict_obj.items():
        # Check if value is of dict type
        if isinstance(value, dict):
            # If value is dict then iterate over all its values
            for pair in  dictIterator(value):
                yield (key, value)
        else:
            # Yields the paths of values containing TLDarr[i]
            if SensitiveInformation.TLDarr[i] in value:
                yield (key, value)
                # print(value)

# Iterate dict for every one of the TLDs and store resuls in dict for each TLD

resultsDict = {}
#for jumping up through the choosen "tld"


for i in range(len(SensitiveInformation.TLDarr)):
    resultsDict[SensitiveInformation.TLDarr[i]]={}
    jump=0
    for pair in dictIterator(csvDictionary):
        # print(pair)
        resultsDict[SensitiveInformation.TLDarr[i]][jump]= pair
        jump=jump+1

print(resultsDict[SensitiveInformation.TLDarr[0]])
# Print results         


    


# ---------------------------------------

# # Navigate to FreeNom API
browser.get(SensitiveInformation.navDict['F'])
str=''
#Now we are going to enter all of the information we have
#for the 5 type of tld:
for j in range (len(SensitiveInformation.TLDarr)):
    #for all the cases in the choosen 'tld'
    for i in range (resultsDict[SensitiveInformation.TLDarr[j]]):
        #convert tuple type to dict
        for value in resultsDict[SensitiveInformation.TLDarr[j]][i]:
            str=value
        #put customer information
