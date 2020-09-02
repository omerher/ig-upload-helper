import pickle
import os
import scraper
import time
import PySimpleGUI as sg
import threading
 
 
def scrape_func(accounts, user_account):
    while not accounts:
        if accounts is None:
            quit()
        accounts = sg.popup_get_text("Accounts cannot be blank.")
 
    accounts_split = accounts.split(",")
 
    if not os.path.exists(f"{user_account}/pickle_data"):  # makes sure the folder exists
        os.mkdir(f"{user_account}/pickle_data")
 
    for account in accounts_split:
        account_data = scraper.scrape(account, 500)
 
        with open(os.path.join(f"{user_account}/pickle_data",  f"{account}.pkl"), "wb") as f:
            pickle.dump(account_data, f)
        
        time.sleep(3600)  # wait for an hour to reset and limiations
 

def overnight():
    sg.theme('Dark')   # Add a touch of color
    # All the stuff inside your window.
    accounts = [folder for folder in [os.path.join('.', o)[2:] for o in os.listdir('.') if os.path.isdir(os.path.join('.',o))] if folder not in ['.git', 'venv', '__pycache__', '.vscode', 'utils']]
    if len(accounts) == 0:
        sg.popup_error('No accounts found. Try running setup.py and then start.py again.')
        quit()

    layout = [ 
                [sg.Text("Enter the accounts separated by a comma (e.g., 'instagram,cristiano,jlo')")],
                [sg.InputText(key='-ACCOUNTS-', size=(25,0))],
                [sg.Text("Select your account:"), sg.DropDown(accounts, key='-ACCOUNT-', default_value=accounts[0]), sg.Button('Start'), sg.Button('Cancel')]]
    
    
    # Create the Window
    WINDOW_TITLE = "Scrape multiple users"
    window = sg.Window(WINDOW_TITLE, layout)
    
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
    
        if event == "Start":
            thread = threading.Thread(target=scrape_func, args=(values["-ACCOUNTS-"],values['-ACCOUNT-']))
            thread.start()
    
            sg.Popup("Started scraping! \nDon't close the main window.", title=WINDOW_TITLE)
                
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
    
    window.close()
