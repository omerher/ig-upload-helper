import json 
with open("Instagram/hashtags.json", "r") as f:
        file_hashtags = json.load(f)
        for hashtag_tier in file_hashtags:
            print(file_hashtags[hashtag_tier])