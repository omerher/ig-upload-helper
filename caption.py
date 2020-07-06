import random
import os
import json
import subprocess

class Caption:
    def __init__(self, og_caption, username, og_poster):
        self.caption = og_caption
        self.username = username
        self.poster = og_poster
    
    def get_description(self):
        with open("Instagram/description.txt", "r", encoding="utf-8") as f:
            descriptions = f.read().split("\n")
        
        return random.choice(descriptions)

    def get_credits(self):
        usernames = [username for username in self.caption.split() if "@" in username]

        for username in usernames:
            if username.strip("@") != self.poster:
                return username

        return "unknown (DM for credit)"

    def get_hashtags(self):
        path = os.path.join("Instagram", "hashtags.json")
        tiers = ["bottom", "middle", "top"]
        num_hashtags = {
            "bottom": random.randint(16, 17),
            "middle": random.randint(4, 6),
            "top": random.randint(2, 4)
        }

        hashtag_str = ""

        # opens the file and gets all the hashtags
        with open(path, "r") as f:
            json_f = json.load(f)
            for tier in tiers:
                hashtags = json_f[tier].replace("#", "").split()  # gets the hashtags from tier and converts to list
                scoped_hashtags = []
                while len(scoped_hashtags) <= num_hashtags[tier]:
                    choice = random.choice(hashtags)
                    if choice not in scoped_hashtags:
                        scoped_hashtags.append(choice)
                hashtag_str += " #" + " #".join(scoped_hashtags)

            return hashtag_str[1:]

    def create_caption(self):
        desc = self.get_description()
        credit = self.get_credits()
        hashtags = self.get_hashtags()
        
        caption = f"""{desc}
FOLLOW 👉👉 @{self.username} 👈👈 FOR MORE
__
📸: {credit}
__
This photo is for entertainment purposes only, if the owner would like the photo taken down or if credit was not given please DM @{self.username} and l will sort it out ASAP!
__
{hashtags}
        """

        return caption.strip()

def get_caption(og_caption, username, og_poster):
    cap = Caption(og_caption, username, og_poster)

    return cap.create_caption()

if __name__ == "__main__":
    caption = caption("a", "b", "om")

    subprocess.run(['clip.exe'], input=caption.encode('utf-16'), check=True)