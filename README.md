# IG Upload Helper

IG Upload Helper is a combination of scripts to help you upload content to your Instagram page faster and easier.

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
2. In that same folder, go into *hashtags.json* (you may need to use [Notepad++](https://notepad-plus-plus.org/downloads/) to edit it). The file should look like Example #1 (if not just copy that into the file). This program uses the staircase hashtags method to get hashtags. Copy the smaller hashtags into `"bottom": "ENTER HERE"`, and the same goes for the other two. They should be in the `#hashtag1 #hashtag2 #hashtag3` format. This will randomize the hashtags from each tier for every post. The file should now look like example #2 (but longer obviously). If you use completely randomized hashtags from one list just copy them all into one of the tiers and follow these next steps. By default, the program takes 10 hashtags from the bottom tier, 9 from the middle one and 8 from the top tier. You can change these numbers by going into *caption.py* in the main directory and changing lines 30-33 (see Example #3). Note that if put this number at a higher value than the number of hashtags in that tier, the program will run for an infinite amount of time, so make sure that the value is lower or equal to the number of hashtags you have in the file.
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

3.

## Usage

```python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
