# library imports
from configparser import ConfigParser
import PySimpleGUI as sg
import requests
import random
import os
import pickle
import time
import keyboard
from datetime import datetime
import time

# files and classes imports
import scraper
import caption
import uploader



def download_mp4(url, dir, name):
    mp4 = requests.get(url)
    file_name = os.path.basename(name)
    path = os.path.join(dir, file_name)
    with open(path, 'wb') as f:
        for chunk in mp4.iter_content(chunk_size=255):
            if chunk:
                f.write(chunk)


def download_image(url, dir, name):
    img = requests.get(url).content
    file_name = os.path.basename(name)
    path = os.path.join(dir, file_name)
    with open(path, 'wb') as f:
        f.write(img)


def reduce_posts(posts):
    return random.sample(posts[:26], len(posts[:26]))


def main(scrape_account, input_timestamp):
    # input("""Things to do before starting:
# 1) Open chrome on your primary monitor and be logged into Facebook Creator Studios with the account you want (must have bookmarks tab open for it to work).
# 2) Open pressing enter, you have 5 seconds to click on your browser.
# 3) When the program is running, you have a few seconds to click anywhere after the bot opens a new tab.
# 4) Remember that you can't click on anything on your computer while the bot is running, I recommend having a video playing on your second monitor, or something that you don't need to touch.
# 5) To stop the bot, drag your mouse to the top left corner of your main monitor, and that will raise an error to stop the bot (This might take two times to work). """)

    # creates necessary folders if they don't exists
    if not os.path.exists("media_backup"):
        os.mkdir("media_backup")

    if not os.path.exists("pickle_data"):
        os.mkdir("pickle_data")

    # removes all files in media_backup folder
    for file in os.listdir("media_backup"):
        os.remove(os.path.join("media_backup", file))

    # moves all files from media folder to media_backup
    for file in os.listdir("media"):
        if file == ".gitkeep":
            continue
        os.rename(os.path.join("media", file),
        os.path.join("media_backup", file))

    # read and get variables from files
    if not input_timestamp and os.path.exists("last_timestamp.txt"):
        with open("last_timestamp.txt", "r") as f:
            last_timestamp = int(f.read())
    elif not input_timestamp and not os.path.exists("last_timestamp.txt"):
        input_timestamp = sg.popup_get_text("No timestamp found. Please enter a timestamp to continue.")
        while not input_timestamp.isnumberic():
            if input_timestamp is None:
                quit()
            input_timestamp = sg.popup_get_text("Please enter only numbers.")
        input_timestamp = int(input_timestamp)
    else: 
        last_timestamp = input_timestamp

    # initializes config file
    config = ConfigParser()
    config.read("settings.ini")


    username = config['settings']['username']
    post_hours = [int(x) for x in config['settings']['post_hours'].split(',')]  # converts string format into list with integers
    bb_enabled = config['settings']['bookmarks_bar_enabled']
    time.sleep(1)

    load_from_file = "No"
    if os.path.exists(os.path.join("pickle_data", f"{scrape_account}.pkl")):  # checks if file exists to ensure no errors or unnecessary questions are asked
        load_from_file = sg.popup_yes_no("Load from file", "We have found data from that user, do you want to load from that file")
        while not load_from_file:
            if load_from_file is None:
                quit()
            load_from_file = sg.popup_yes_no("Error", "Please press Yes or No. We have found data from that user, do you want to load from that file")

    if load_from_file == "Yes":
        with open(os.path.join("pickle_data",  f"{scrape_account}.pkl"), "rb") as f:
            _data = pickle.load(f)

        time.sleep(5)
    else:
        _data = scraper.scrape(scrape_account, 500)
        
        with open(os.path.join("pickle_data",  f"{scrape_account}.pkl"), "wb") as f:
            pickle.dump(_data, f)

    data = reduce_posts(_data)


    parent_path = "ENTER_FULL_PATH_TO/Instagram Upload Bot/media"

    for x, post in enumerate(data):
        medias = reversed(post["media"])
        file_names = ''
        for y, media in enumerate(medias):
            if ".jpg" in media["media"]:
                download_image(media["media"], parent_path, f"{x} {y}{media['suffix']}")
                file_names += f'"{x} {y}{media["suffix"]}" '
            elif ".mp4" in media["media"]:
                download_mp4(media["media"], parent_path, f"{x} {y}{media['suffix']}")
                file_names += f'"{x} {y}{media["suffix"]}" '
        
        # create a caption using a method which gets: the original caption, the username of the account posting, and the origin poster
        post_caption = caption.get_caption(post["caption"], username, post["op"])  # pass in values short description, your username, and credit respectively, and returns a generated caption
        uploader.uploader(post_caption, file_names, bb_enabled)
    
    to_remove = sg.popup_get_text("Navigate to the first tab and enter how many tabs you deleted (if none, enter 0):")
    while not to_remove.isnumeric() or (0 <= int(to_remove) <= 25):
        if to_remove is None:
            quit()
        to_remove = sg.popup_get_text("Please input a number from 0-25. Navigate to the first tab and enter how many tabs you deleted (if none, enter 0):")
    num_tabs = 25 - int(to_remove)


    """
    variable 'post_hours' is the hours of the day to post
    variable 'timestamp' is the calculated timestamp for the psot
    variable 'current' is set the current hour needed, which is the remainder of the i divided by the length of 'times'
    """
    timestamp = input_timestamp
    dt = datetime.fromtimestamp(timestamp)  # convert that timestamp to an useable datetime object

    # try to find the index of the hour from the timestamp in the configured hours, but if not found, start from the beginning of that day
    try:
        starting_time = post_hours.index(dt.hour) + 1
        print(starting_time)
    except ValueError:
        formatted_time = f"{dt.day}/{dt.month}/{dt.year}"
        timestamp = int(time.mktime(datetime.strptime(formatted_time, "%d/%m/%Y").timetuple()))  # converts the string in the previous line to a timestamp
        starting_time = 0

    for i in range(starting_time, num_tabs+starting_time):
        current = i % len(post_hours)
    
        # if the loop is at the first hour (but not the first time), calculate the time between the last hour and the first
        # 3600 is how many seconds in an hour, to convert it correctly
        if i == 0:  # no need for previous if it's the first time
            timestamp += post_hours[current]*3600
        elif i % len(post_hours) == 0 and i != 0:
            timestamp += (24-post_hours[-1] + post_hours[0])*3600
        else:
            timestamp += (post_hours[current] - post_hours[current-1])*3600
        
        uploader.scheduler(timestamp, bb_enabled)

        time.sleep(1)
        keyboard.press_and_release("ctrl+tab")
        time.sleep(1)


    with open("last_timestamp.txt", "w") as f:
        f.write(str(int(timestamp)))  # convert to int before to remove .0 at the end

if __name__ == '__main__':
    pass
