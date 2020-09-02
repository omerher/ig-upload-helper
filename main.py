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

import utils, scraper, caption, uploader


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


def reduce_posts(posts, num_posts):
    return random.sample(posts[:num_posts], len(posts[:num_posts]))


def main(scrape_account, input_timestamp, num_posts, user_account):
    # initializes config file
    config = ConfigParser()
    config.read(os.path.join(user_account, "settings.ini"))

    post_hours = [int(x) for x in config['settings']['post_hours'].split(',')]  # converts string format into list with integers
    bb_enabled = config['settings']['bookmarks_bar_enabled']
    dt_format = config['settings']['date_format'].replace("%%", "%")
    multiple_accounts = config['settings']['multiple_accounts']
    format_24h = config['settings']['24h_format']
    

    input_timestamp_path = os.path.join(user_account, "last_timestamp.txt")
    # read and get variables from files
    if not input_timestamp and os.path.exists(input_timestamp_path):
        with open(input_timestamp_path, "r") as f:
            last_timestamp = int(f.read())
    elif not input_timestamp and not os.path.exists(input_timestamp_path):
        last_timestamp = sg.popup_get_text("No timestamp found. Please enter a timestamp to continue.")
        while not last_timestamp.isnumberic():
            if last_timestamp is None:
                quit()
            last_timestamp = sg.popup_get_text("Please enter only numbers.")
        last_timestamp = int(last_timestamp)
    else: 
        last_timestamp = input_timestamp


    utils.setup_folder(user_account)  # make sure all folders are there

    # removes all files in media_backup folder
    for file in os.listdir(f"{user_account}/media_backup"):
        os.remove(os.path.join(f"{user_account}/media_backup", file))

    # moves all files from media folder to media_backup
    for file in os.listdir(f"{user_account}/media"):
        if file == ".gitkeep":
            continue
        os.rename(os.path.join(f"{user_account}/media", file),
        os.path.join(f"{user_account}/media_backup", file))

    time.sleep(1)

    load_from_file = "No"
    if os.path.exists(os.path.join(f"{user_account}/pickle_data", f"{scrape_account}.pkl")):  # checks if file exists to ensure no errors or unnecessary questions are asked
        load_from_file = sg.popup_yes_no("Load from file", "We have found data from that user, do you want to load from that file")
        while not load_from_file:
            if load_from_file is None:
                quit()
            load_from_file = sg.popup_yes_no("Error", "Please press Yes or No. We have found data from that user, do you want to load from that file")

    if load_from_file == "Yes":
        with open(os.path.join(f"{user_account}/pickle_data",  f"{scrape_account}.pkl"), "rb") as f:
            _data = pickle.load(f)

        time.sleep(5)
    else:
        _data = scraper.scrape(scrape_account, 500)
        
        with open(os.path.join(f"{user_account}/pickle_data",  f"{scrape_account}.pkl"), "wb") as f:
            pickle.dump(_data, f)

    data = reduce_posts(_data, num_posts)


    parent_path = os.path.abspath(f"{user_account}/media")
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
        post_caption = caption.get_caption(post["caption"], user_account, post["op"])  # pass in values short description, your username, and credit respectively, and returns a generated caption
        uploader.uploader(post_caption, file_names, bb_enabled, parent_path, user_account, multiple_accounts)
    
    to_remove = sg.popup_get_text("Navigate to the first tab and enter how many tabs you deleted (if none, enter 0):")
    while not to_remove.isnumeric() or not (0 <= int(to_remove) <= num_posts):
        if to_remove is None:
            quit()
        to_remove = sg.popup_get_text(f"Please input a number from 0-{num_posts}. Navigate to the first tab and enter how many tabs you deleted (if none, enter 0):")
    num_tabs = num_posts - int(to_remove)


    """
    variable 'post_hours' is the hours of the day to post
    variable 'timestamp' is the calculated timestamp for the psot
    variable 'current' is set the current hour needed, which is the remainder of the i divided by the length of 'times'
    """
    timestamp = int(last_timestamp)
    dt = datetime.fromtimestamp(timestamp)  # convert that timestamp to an useable datetime object
    
    # try to find the index of the hour from the timestamp in the configured hours, but if not found, start from the beginning of that day
    try:
        starting_time = post_hours.index(dt.hour) + 1
    except ValueError:
        formatted_time = f"{dt.day}/{dt.month}/{dt.year}"
        timestamp = int(time.mktime(datetime.strptime(formatted_time, dt_format).timetuple()))  # converts the string in the previous line to a timestamp
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
        
        uploader.scheduler(timestamp, bb_enabled, dt_format, format_24h)

        time.sleep(1)
        keyboard.press_and_release("ctrl+tab")
        time.sleep(1)


    with open(f"{user_account}/last_timestamp.txt", "w") as f:
        f.write(str(int(timestamp)))  # convert to int before to remove .0 at the end

if __name__ == '__main__':
    pass
