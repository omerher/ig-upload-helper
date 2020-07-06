import PySimpleGUI as sg
from configparser import ConfigParser
import os
from main import main

WINDOW_TITLE = 'Instagram Uploader Bot'

sg.theme('Dark')   # Add a touch of color
# All the stuff inside your window.
layout = [ 
            [sg.Text('Enter the username of the account you want to scrape:'), sg.InputText(key='-SCRAPE_USERNAME-', size=(41,0))],
            [sg.Text("Enter the timestamp of your last post (if nothing is entered, it will be taken from the 'last_timestamp.txt' file):")],
            [sg.InputText(key = '-TIMESTAMP-', size=(11,0)), sg.Button('epochconverter.com')],
            [sg.Button('Start'), sg.Button('Cancel')] ]


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

        main(scrape_username, input_timestamp)

    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break






window.close()