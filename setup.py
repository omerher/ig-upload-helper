import PySimpleGUI as sg
import os
from configparser import ConfigParser

WINDOW_TITLE = 'Instagram Uploader Bot Setup'

sg.theme('Dark')   # Add a touch of color
# All the stuff inside your window

config = ConfigParser()

layout = [ 
            [sg.Text('Enter your own username: '), sg.InputText(size=(30,), key='-USERNAME-') ],
            [sg.Text("")],
            [sg.Text('Enter the hours to post separated by a comma (e.g., 0,7,14)')],
            [sg.Text("where 0 = 12am:"), sg.InputText(size=(25,), key='-POST_HOURS-')],
            [sg.Text("")],
            [sg.Text("Select your local date format: "), sg.DropDown(["MM/DD/YYYY", "DD/MM/YYYY"], key="-DATE_FORMAT-")],
            [sg.Text("")],
            [sg.Checkbox("Check if the bookmarks bar is hidden on websites (not new tab)", default=False, key='-BOOKMARKS_BAR_ENABLED-')],
            [sg.Checkbox("Check if you have multiple accounts connected to Creator Studio.", default=False, key='-MULTIPLE_ACCOUNTS-')],
            [sg.Checkbox("Check if you have 24h format when scheduling in Creator Studio.", default=False, key='-24H_FORMAT-')],
            [sg.Button('Save'), sg.Button('Cancel')]
            ]


# Create the Window
window = sg.Window(WINDOW_TITLE, layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # when user click Save
    if event == 'Save':
        # check that the hours input is correct
        post_hours = values['-POST_HOURS-']
        while not post_hours.replace(',', '').isnumeric():
            if post_hours is None:
                quit()
            post_hours = sg.popup_get_text("Invalid input. Make sure the numbers are separated by a comma.")
        
        username = values['-USERNAME-']
        if not values['-USERNAME-']:
            username = sg.popup_get_text("Username not present. Please input to continue using the program.")
            while not username:
                if username is None:
                    quit()
                username = sg.popup_get_text("Please input your username to continue using the program.")
        
        date_format = {'MM/DD/YYYY': '%%m/%%d/%%Y', 'DD/MM/YYYY': '%%d/%%m/%%Y'}[values["-DATE_FORMAT-"]]  # one-liner to get datetime format
        
        config['settings'] = {}
        settings = config['settings']
        settings['username'] = username
        settings['post_hours'] = post_hours
        settings['bookmarks_bar_enabled'] = str(not values['-BOOKMARKS_BAR_ENABLED-'])
        settings['date_format'] = date_format
        settings['multiple_accounts'] = str(values['-MULTIPLE_ACCOUNTS-'])
        settings['24h_format'] = str(values['-24H_FORMAT-'])

        if not os.path.isdir(username):
            os.mkdir(username)
        with open(f'{username}/settings.ini', 'w') as f:
            config.write(f)
        
        sg.Popup(f'Saved settings to "{username}/settings.ini"!', title=WINDOW_TITLE)
        break

    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break


window.close()
