import PySimpleGUI as sg
from configparser import ConfigParser

WINDOW_TITLE = 'Instagram Uploader Bot Setup'

sg.theme('Dark')   # Add a touch of color
# All the stuff inside your window.

config = ConfigParser(allow_no_value=True)
config.read("settings.ini")

layout = [ 
            [sg.Text('Enter your own username: '), sg.InputText(size=(30,), key='-USERNAME-') ],
            [sg.Text("")],
            [sg.Text('Enter the hours to post separated by a comma (e.g., 0,7,14)')],
            [sg.Text("where 0 = 12am:"), sg.InputText(size=(25,), key='-POST_HOURS-')],
            [sg.Text("")],
            [sg.Text("Select your local date format: "), sg.DropDown(["MM/DD/YYYY", "DD/MM/YYYY"], key="-DATE_FORMAT-")],
            [sg.Text("")],
            [sg.Text("Select the 'media' folder inside 'ig-upload-helper'")],
            [sg.In(key='-FOLDER_PATH-'), sg.FolderBrowse(target='-FOLDER_PATH-')],
            [sg.Text("")],
            [sg.Checkbox("Check if the bookmarks bar is hidden on websites (not new tab)", default=False, key='-BOOKMARKS_BAR_ENABLED-')],
            [sg.Checkbox("Check if you have multiple accounts connected to Creator Studio.", default=False, key='-MULTILPE-ACCOUNTS-')],
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
        if post_hours:
            while not post_hours.replace(',', '').isnumeric():
                if post_hours is None:
                    quit()
                post_hours = sg.popup_get_text("Invalid input. Make sure the numbers are separated by a comma.")
        
        # check if username input isn't blank, otherwise takes from settings file
        if values['-USERNAME-']:
            new_username = values['-USERNAME-']
        else:
            try:
                new_username = config['database']['username']
            except KeyError:
                new_username = sg.popup_get_text("Username not present. Please input to continue using the program.")
                while not new_username:
                    if new_username is None:
                        quit()
                    new_username = sg.popup_get_text("Please input your username to continue using the program.")

        if values['-POST_HOURS-']:
            post_hours = values['-POST_HOURS-']
        else:
            try:
                posts_per_day = config['database']['post_hours']
            except KeyError:
                post_hours = sg.popup_get_text("Post hours not present. Please input to continue using the program.")
                while not post_hours.replace(',', '').isnumeric():
                    if post_hours is None:
                        quit()
                    post_hours = sg.popup_get_text("Invalid input. Make sure the numbers are separated by a comma.")
        
        date_format = {'MM/DD/YYYY': '%%m/%%d/%%Y', 'DD/MM/YYYY': '%%d/%%m/%%Y'}[values["-DATE_FORMAT-"]]  # one-liner to get datetime format
        
        config['settings'] = {}
        settings = config['settings']
        settings['username'] = new_username
        settings['post_hours'] = post_hours
        settings['bookmarks_bar_enabled'] = str(not values['-BOOKMARKS_BAR_ENABLED-'])
        settings['date_format'] = date_format
        settings['folder_path'] = values["-FOLDER_PATH-"]
        settings['multiple_accounts'] = values['-MULTIPLE_ACCOUNTS-']

        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
        
        sg.Popup('Saved settings to "settings.ini"!', title=WINDOW_TITLE)
        break

    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break


window.close()