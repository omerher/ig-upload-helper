# IG Upload Helper

IG Upload Helper is a combination of scripts to help you upload content to your Instagram page faster and easier.

## Prerequisites
- **Facebook Creator Studios connected to your Instagram account**. Currently the program only support one connected account and will not work if you have more than one.
- **Chrome installed and set as the default browser**. Currently, this program only works with Chrome (submit an issue with a different browser and I will try to add support for it).
- This has been tested only on **Windows 10** and I don't know if it will work for other operating systems.
- **1080p monitor**. The pixel coordinates won't work for any quality other than 1080p. The size of the monitor doesn't matter.

I will be trying to make this more compatible in the future with more browsers and operating systems. 

## Installation

1. Download [Python](https://www.python.org/downloads/) if it's not installed yet.
2. Download [Git](https://git-scm.com/downloads) if it's not installed yet.
3. Open a CMD window in the folder where you want this code to be (This can be done by writing `cmd` in the address bar and pressing enter).
4. Clone this repository using `git clone https://github.com/omerher/ig-upload-helper.git`.
5. Install virtualenv by entering `pip install virtualenv` into the CMD window.
6. Create an empty virtual environment (this helps ensure that everything will work) by entering `virtualenv venv`. This creates a Python virtual environment called *venv*.
7. Activate that virtual environment by entering `venv\Scripts\activate`.
8. Install all the packages by entering `pip install -r requirements.txt`.

## Setup
1. Go into the Instagram folder and open *description.txt*. Here enter all of the captions that you want to be randomly picked from when creating a caption for a post. Some examples of captions can be ***Tag a friend!***, ***What do you think of this post?***, etc. Each different caption has to be separated by a new line. Save the file when you are done. You can always change this in the future.
2. In that same folder, go into *hashtags.json* (you may need to use [Notepad++](https://notepad-plus-plus.org/downloads/) to edit it). The file should look like [Example #1](https://github.com/omerher/ig-upload-helper/blob/master/README.md#example-1) (if not just copy that into the file). This program uses the staircase hashtags method to get hashtags. Copy the smaller hashtags into `"bottom": "ENTER HERE"`, and the same goes for the other two. They should be in the `#hashtag1 #hashtag2 #hashtag3` format. This will randomize the hashtags from each tier for every post. The file should now look like [Example #2](https://github.com/omerher/ig-upload-helper/blob/master/README.md#example-2) (but longer obviously). If you use completely randomized hashtags from one list just copy them all into one of the tiers and follow these next steps. By default, the program takes 10 hashtags from the bottom tier, 9 from the middle one and 8 from the top tier. You can change these numbers by going into *caption.py* in the main directory and changing lines 30-33 (see [Example #3](https://github.com/omerher/ig-upload-helper/blob/master/README.md#example-3)). Note that if you put this number at a higher value than the number of hashtags in that tier, the program will run for an infinite amount of time, so make sure that the value is lower or equal to the number of hashtags you have in the file.
##### Example #1
```json
{
	"bottom": "",
	"middle": "",
	"top": ""
}
```

##### Example #2
```json
{
	"bottom": "#example1 #example2",
	"middle": "#example3 #example4",
	"top": "#example5 #example6"
}
```

##### Example #3
```python
# change these values to however many hashtags you want the program to take from each tier.
# note that Instagram's max hashtags allowed is 30, so don't go over that number (all combined).
# if you only have hashtags in one tier, put that number to 25-30 and the others to 0.
num_hashtags = {
    "bottom": 10,
    "middle": 9,
    "top": 8
}
```
3. The default caption format is as shown below, with a few changes available.

`{desc}` will randomly select one of your descriptions from *description.txt*. \
`{self.username}`will take your username (you will later set this up) \
`{credit}` will try to take credit from the post, and if it's not found will be set as 'unknown' (this doesn't always work or find the correct credit). \
`{hashtags}` will take a the randomized hashtags you configured in the last step.

```python
caption = f"""
{desc}
FOLLOW 👉👉 @{self.username} 👈👈 FOR MORE
__
📸: {credit}
__
This photo is for entertainment purposes only, if the owner would like the photo taken down or if credit was not given please DM @{self.username} and l will sort it out ASAP!
__
{hashtags}
        """
```
You can change the caption to whatever format you want using thee keywords, or add additional features if you know Python.

4. Go into line 114 in *main.py* and change `parent_path  =  "ENTER_FULL_PATH_TO/Instagram Upload Bot/media"` and change it to the full path of the 'media' folder (e.g., `parent_path  =  "E:/Coding/Instagram Upload Bot/media"`). Make sure to replace and backslash `\` with a regular slash `/`.

5. The final thing to do is run *setup.py*. This is a GUI with settings needed to run the program. To run the file all you have to do is make sure the virtual environment is activated (you should see **(venv)** at the beginning of the line in your CMD window, if it's not activated, check step 7 in Installation), and enter `python setup.py` into the CMD window. Enter all the information in the program and press save.

## Usage

The program uploads posts by controlling your mouse and keyboard. This means that while it is uploading, you can't do anything on your computer than requires your control.

1. Open a CMD window in the main directory (typing `cmd` into the address bar).
2. Activate the virtual environment by entering `venv\Scripts\activate`.
3. Open *start.py* by entering `python start.py`.
4. Enter all of the information into the window. Note that for the first time, you will need to enter the timestamp ([what is a timestamp?](http://unixtimestamp.50x.eu/about.php)) of your last post. To get the timestamp go to [epochconverter](https://www.epochconverter.com/) and enter the date and time of your last post. Make sure that it is set to local time and not GMT.
5. Just press start and wait for the bot to start scraping posts. You can see the progress in the CMD window. There may be some more popup windows asking you to enter information, which you should do.

***Some important notes that should be taken into account***:
 - **The program can only run on your main monitor**.
 - **If you have more than one monitor, Chrome has to be last used on the main monitor.** This is because by default it open a new tab in the last used place, and if it's on a different monitor it won't work.
 - **Chrome has to be in full screen for it to click in the correct places.** 
 - **Your file picker window has to be in full screen before starting the program** (there is no full screen button so just double click the top of the window). You can go to any site where there is a file upload button or go to this site [https://ps.uci.edu/~franklin/doc/file_upload.html](https://ps.uci.edu/~franklin/doc/file_upload.html) (it won't be 100% full screen but it's okay).
 - **To stop the bot when it's uploading posts, drag your mouse to the top left corner of your main monitor**. This will throw an error and stop the program. **To stop it when it's doing something else like scraping posts click on the CMD window and press `Ctrl + C`** or pressing the X button in any of the GUI windows.
 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
