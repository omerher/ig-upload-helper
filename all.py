import PySimpleGUI as sg
import threading
import os

from start import start
from setup import setup
import utils, overnight

WINDOW_TITLE = 'IG Upload Helper'
x = 600
y = 500

sg.theme('Dark')   # Add a touch of color
# All the stuff inside your window.

base_path = os.path.realpath(__file__)[:-len(os.path.basename(__file__))]

accounts = [account for account in open("accounts.txt", "r").read().split("\n") if account]  # gets all accounts
accounts_visible = False
if len(accounts) > 1:
    accounts_visible = True

barrier = sg.Text("|", font=("Ariel 15"))
barrier_visible = sg.Text("|", font=("Ariel 15"), visible=accounts_visible)

layout = [ 
            [sg.Text("IG Upload Helper", font=("Ariel 14"), justification='center', size=(x,1))],
            [sg.Text("")],
            [sg.Text("First Time (for each account)", font=("Arield 12 bold"))],
            [sg.Button("Setup", size=(8,2)), ],
            [sg.Text("Select account:", visible=accounts_visible), sg.DropDown(accounts, key='-ACCOUNT-', default_value=accounts[0], visible=accounts_visible), barrier_visible, sg.Text("Setup files:"), sg.Button("Descriptions"), sg.Button("Hashtags")],
            [sg.Text("")],
            [sg.Text("Run Bot", font=("Ariel 12 bold"))],
            [sg.Button("Start", size=(8,2))],
            [sg.Text("")],
            [sg.Text("Scrape multiple accounts to use for later:")],
            [sg.Text("Enter the accounts separated by a comma (e.g., 'instagram,cristiano,jlo')")],
            [sg.InputText(key='-ACCOUNTS-', size=(25,0))],
            [sg.Text("Select your account:"), sg.DropDown(accounts, key='-OVERNIGHT_ACCOUNT-', default_value=accounts[0], visible=accounts_visible), sg.Button('Scrape')],
            [sg.Text("")],
            [sg.Button('Cancel', size=(8,2))]
            ]

# Create the Window
window = sg.Window(WINDOW_TITLE, layout, size=(x, y))

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == "Start":
        start()
    
    if event == "Setup":
        username = setup()
    
    if event == "Descriptions":
        accounts = [account for account in open("accounts.txt", "r").read().split("\n") if account]
        if len(accounts) < 1:
            sg.Popup("No accounts added")
            break
        if len(accounts) == 1:
            username = accounts[0]
        else:
            username = values["-ACCOUNT-"]
            
        description_path = os.path.join(base_path, f"{username}/description.txt")
        os.startfile(description_path)
    
    if event == "Hashtags":
        accounts = [account for account in open("accounts.txt", "r").read().split("\n") if account]
        if len(accounts) < 1:
            sg.Popup("No accounts added")
            break
        if len(accounts) == 1:
            username = accounts[0]
        else:
            username = values["-ACCOUNT-"]
        
        hashtags_path = os.path.join(base_path, f"{username}/hashtags.json")
        utils.setup_hashtags(hashtags_path)
    
    if event == "Scrape":
        utils.overnight_scrape(values["-ACCOUNTS-"], values["-OVERNIGHT_ACCOUNT-"])

    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break

window.close()
