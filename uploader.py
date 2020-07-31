import pyautogui
import keyboard
import os
import time
import subprocess
from datetime import datetime

def click(cords):
    x = cords[0]
    y = cords[1]
    pyautogui.click(x, y)

class Uploader:
    def __init__(self, caption, f_names, bb_enabled, path):
        # bb = bookmarks bar
        if bb_enabled == "True":
            bb_difference = 0
        else:
            bb_difference = 35
        
        # coords for all buttons to be pressed
        bb_difference = bb_difference
        self.profile_select = (334, 172-bb_difference)
        self.search_profile = (348, 270-bb_difference)
        self.unselect_all = (495, 730-bb_difference)
        self.first_profile = (273, 328-bb_difference)
        self.view_btn = (811, 730-bb_difference)
        self.create_post_btn = (111, 182-bb_difference)
        self.instagram_feed_btn = (121, 227-bb_difference)
        self.caption_location = (1245, 334-bb_difference)
        self.add_content = (1256, 740-bb_difference)
        self.file_upload = (1270, 786-bb_difference)
        self.address_bar = (748, 47)
        self.file_names_cords = (900, 977)
        
        self.caption = caption
        self.file_names = f_names
        self.path = path
    
    def new_tab(self):
        # open new tab
        url = "https://business.facebook.com/creatorstudio?tab=instagram_content_posts&mode=instagram&collection_id=all_pages&content_table=INSTAGRAM_POSTS"
        os.startfile(url)

        time.sleep(5)
        click(self.profile_select)
        
        time.sleep(1)
        click(self.unselect_all)
        
        time.sleep(1)
        click(self.search_profile)
        time.sleep(0.5)
        keyboard.write("cutelovingdogs")
        
        time.sleep(1)
        click(self.first_profile)
        
        time.sleep(1)
        click(self.view_btn)
        
        # wait and then click Create Post
        time.sleep(3)
        click(self.create_post_btn)

        # wait and then click Instagram Feed
        time.sleep(1)
        click(self.instagram_feed_btn)

        # wait and then enter caption
        time.sleep(1.5)
        click(self.caption_location)
        time.sleep(0.5)
        subprocess.run(['clip.exe'], input=self.caption.encode('utf-16'), check=True) 
        keyboard.press_and_release('ctrl+v')
        
        time.sleep(1)
        click(self.add_content)

        time.sleep(1)
        click(self.file_upload)

        time.sleep(1)
        click(self.address_bar)
        time.sleep(0.4)
        keyboard.write(self.path)
        time.sleep(0.4)
        keyboard.press_and_release("enter")

        time.sleep(1)
        click(self.file_names_cords)
        time.sleep(0.5)
        keyboard.write(self.file_names)
        time.sleep(1)
        keyboard.press_and_release("enter")


def uploader(caption, file_names, bb_enabled, path, username, multiple_accounts):
    # bb = bookmarks bar
    if bb_enabled == "True":
        bb_difference = 0
    else:
        bb_difference = 35
    
    # coords for all buttons to be pressed
    profile_select = (334, 172-bb_difference)
    search_profile = (348, 270-bb_difference)
    unselect_all = (495, 730-bb_difference)
    first_profile = (273, 328-bb_difference)
    view_btn = (811, 730-bb_difference)
    create_post_btn = (111, 182-bb_difference)
    instagram_feed_btn = (121, 227-bb_difference)
    caption_location = (1245, 334-bb_difference)
    add_content = (1256, 740-bb_difference)
    file_upload = (1270, 786-bb_difference)
    address_bar = (748, 47)
    file_names_cords = (900, 977)
    
    
    # open new tab
    url = "https://business.facebook.com/creatorstudio?tab=instagram_content_posts&mode=instagram&collection_id=all_pages&content_table=INSTAGRAM_POSTS"
    os.startfile(url)

    if multiple_accounts == "True":  # need to select only one account for the bot to work
        # click profile selection button
        time.sleep(5)
        click(profile_select)
        
        # click Unselect All
        time.sleep(1)
        click(unselect_all)
        
        # search for the account
        time.sleep(1)
        click(search_profile)
        time.sleep(0.5)
        keyboard.write(username)
        
        # select the first profile
        time.sleep(1)
        click(first_profile)
        
        # click save button
        time.sleep(1)
        click(view_btn)
    
    # click Create Post
    time.sleep(5)
    click(create_post_btn)

    # click Instagram Feed
    time.sleep(1)
    click(instagram_feed_btn)

    # enter caption
    time.sleep(1.5)
    click(caption_location)
    time.sleep(0.5)
    subprocess.run(['clip.exe'], input=caption.encode('utf-16'), check=True) 
    keyboard.press_and_release('ctrl+v')
    
    # click Add Content
    time.sleep(1)
    click(add_content)

    # click From File Upload
    time.sleep(1)
    click(file_upload)

    # click the file explorer address bar and enter path to media
    time.sleep(1)
    click(address_bar)
    time.sleep(0.4)
    keyboard.write(path)
    time.sleep(0.4)
    keyboard.press_and_release("enter")

    # select all photos and press enter
    time.sleep(1)
    click(file_names_cords)
    time.sleep(0.5)
    keyboard.write(file_names)
    time.sleep(1)
    keyboard.press_and_release("enter")

    # wait a second before repeating
    time.sleep(1)


def scheduler(timestamp, bb_enabled, dt_format):
    # bb = bookmarks bar
    if bb_enabled:
        bb_difference = 0
    else:
        bb_difference = 35

    schedule_caret = (1860, 1000-bb_difference)
    schedule_btn = (1591, 904-bb_difference)
    date_cords = (1615, 875-bb_difference)

    dt = datetime.fromtimestamp(timestamp)

    formatted = dt.strftime(dt_format)

    # Takes care of the hour
    hour = dt.hour
    is_pm = False
    if hour == 0:
        hour = 12
    elif hour == 12:
        is_pm = True
    elif hour > 12:
        hour = hour % 12
        is_pm = True

    time.sleep(1.5)
    click(schedule_caret)

    time.sleep(1)
    click(schedule_btn)

    time.sleep(1.5)
    click(date_cords)

    time.sleep(0.75)
    keyboard.write(formatted)
    time.sleep(0.5)
    keyboard.press_and_release("enter")
    time.sleep(0.5)
    keyboard.press_and_release("tab")

    time.sleep(1)
    str_hour = str(hour)
    if len(str_hour) == 1:
        keyboard.write(str_hour)
    else:
        keyboard.write(str_hour[0])
        time.sleep(0.2)
        keyboard.write(str_hour[1])
    time.sleep(1)
    keyboard.press_and_release("tab")

    time.sleep(1)
    keyboard.write(str(dt.minute))
    time.sleep(1)
    keyboard.press_and_release("tab")

    time.sleep(1.5)
    if is_pm:
        keyboard.write("p")
    else:
        keyboard.write("a")
    time.sleep(1)


if __name__ == "__main__":
    pass
