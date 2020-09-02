import PySimpleGUI as sg
from configparser import ConfigParser
import os
from main import main
import re
import os

def start():
    WINDOW_TITLE = 'Instagram Uploader Bot'

    sg.theme('Dark')   # Add a touch of color
    # All the stuff inside your window.

    accounts = [account for account in open("accounts.txt", "r").read().split("\n") if account]  # gets all accounts
    if len(accounts) == 0:
        sg.popup_error('No accounts found. Try running setup.py and then start.py again.')
        quit()

    layout = [ 
                [sg.Text('Enter the username of the account you want to scrape:'), sg.InputText(key='-SCRAPE_USERNAME-', size=(41,0))],
                [sg.Text("Enter the timestamp of your last post (if nothing is entered, it will be taken from the 'last_timestamp.txt' file):")],
                [sg.InputText(key = '-TIMESTAMP-', size=(11,0)), sg.Button('epochconverter.com')],
                [sg.Text("Enter how many posts you want to posts from the user:"), sg.InputText(key='-NUM_POSTS-', default_text='25', size=(6,0))],
                [sg.Text("Select your account:"), sg.DropDown(accounts, key='-ACCOUNT-', default_value=accounts[0]), sg.Button('Start'), sg.Button('Cancel')] ]


    # Create the Window
    window = sg.Window(WINDOW_TITLE, layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        if event == 'epochconverter.com':
            os.startfile('https://www.epochconverter.com/')

        if event == 'Start':
            scrape_username = values["-SCRAPE_USERNAME-"]
            while not scrape_username:
                if scrape_username is None:
                    quit()
                scrape_username = sg.popup_get_text("Username cannot be blank.")

            input_timestamp = values["-TIMESTAMP-"]
            
            num_posts = values["-NUM_POSTS-"]
            regex = r"\b([1-9]|[1-8][0-9]|9[0-9]|100)\b"
            while not re.search(regex, num_posts):
                if num_posts is None:
                    quit()
                num_posts = sg.popup_get_text("Input must be a number between 1-100.")
            num_posts = int(num_posts)
            
            account = values['-ACCOUNT-']

            main(scrape_username, input_timestamp, num_posts, account)

        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break


    window.close()

if __name__ == "__main__":
    start()