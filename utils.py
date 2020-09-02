import os
import PySimpleGUI as sg
import json
import pickle
import utils
import time

def create_folder(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def create_file(path, file_text):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(file_text)

def setup_folder(username):
    main_folder_path = os.path.realpath(__file__)[:-15]
    
    # creates the necassary files
    base_path = os.path.join(main_folder_path, username)
    create_folder(base_path)  # create the folder
    create_folder(os.path.join(base_path, "media"))  # creates media folder
    create_folder(os.path.join(base_path, "media_backup"))  # creates media_backup folder
    create_folder(os.path.join(base_path, "pickle_data"))  # creates pickle_data folder

    # creates description.txt if it doesn't exist
    description_path = os.path.join(base_path, "description.txt")
    create_file(description_path, "Enter each description/caption on a new line.")

def overnight_scrape(accounts, user_account):
    while not accounts:
        if accounts is None:
            quit()
        accounts = sg.popup_get_text("Accounts cannot be blank.")
 
    accounts_split = accounts.split(",")
 
    if not os.path.exists(f"{user_account}/pickle_data"):  # makes sure the folder exists
        os.mkdir(f"{user_account}/pickle_data")
 
    for account in accounts_split:
        account_data = utils.scraper.scrape(account, 500)
 
        with open(os.path.join(f"{user_account}/pickle_data",  f"{account}.pkl"), "wb") as f:
            pickle.dump(account_data, f)
        
        time.sleep(3600)  # wait for an hour to reset and limiations

def setup_hashtags(hashtags_path):
    WINDOW_TITLE = 'Setup Hashtags'

    sg.theme('Dark')   # Add a touch of color
    # All the stuff inside your window

    layout = [ 
                [sg.Text("Enter how many hashtags you want from each tier:")],
                [sg.Text("Small Hashtags:"), sg.Input(key="-NUM_SMALL-", size=(5,1))],
                [sg.Text("Medium Hashtags:"), sg.Input(key="-NUM_MEDIUM-", size=(5,1))],
                [sg.Text("Large Hashtags:"), sg.Input(key="-NUM_LARGE-", size=(5,1))],
                [sg.Text("")],
                [sg.Text("Enter hashtags here:")],
                [sg.Text("Small Hashtags:"), sg.Input(key="-HASHTAGS_SMALL-")],
                [sg.Text("Medium Hashtags:"), sg.Input(key="-HASHTAGS_MEDIUM-")],
                [sg.Text("Large Hashtags:"), sg.Input(key="-HASHTAGS_LARGE-")],
                [sg.Button("Save", size=(8,2))]
                ]

    # Create the Window
    window = sg.Window(WINDOW_TITLE, layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        # when user click Save
        if event == "Save":
            num_small_hashtags = values["-NUM_SMALL-"]
            num_medium_hashtags = values["-NUM_MEDIUM-"]
            num_large_hashtags = values["-NUM_LARGE-"]

            small_hashtags = values["-HASHTAGS_SMALL-"]
            medium_hashtags = values["-HASHTAGS_MEDIUM-"]
            large_hashtags = values["-HASHTAGS_LARGE-"]

            with open(hashtags_path, "w") as f:
                hashtags = {}

                hashtags["bottom"] = small_hashtags
                hashtags["middle"] = medium_hashtags
                hashtags["top"] = large_hashtags
                hashtags["num_hashtags"] = f"{num_small_hashtags} {num_medium_hashtags} {num_large_hashtags}"

                json.dump(hashtags, f, indent=2)
            
            sg.Popup("Saved!")
            break


        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break


    window.close()

    return None
