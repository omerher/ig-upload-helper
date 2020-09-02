import requests
import json
import datetime
import re
import PySimpleGUI as sg

def get_id(username):
    url = "https://www.instagram.com/web/search/topsearch/?context=blended&query=" + username + "&rank_token=0.3953592318270893&count=1"
    response = requests.get(url)
    respJSON = response.json()

    username_id = str(respJSON['users'][0].get("user").get("pk"))
    return username_id

def get_media_type(string):
    if string == "GraphImage":
        return "Photo"
    elif string == "GraphVideo":
        return "Video"
    elif string == "GraphSidecar":
        return "Carousel"

def get_post_info(link):
    try:
        url = f"{link}?__a=1"
        json_data = requests.get(url).json()
    except:
        r = requests.get(link).text
        # find json in the html with regex, get first item from list then from tuple, and remove last semicolon
        x = re.findall('<script type="text\/javascript">' + '([^{]+?({.*graphql.*})[^}]+?)' + '<\/script>', r)[0][0][:-1]
        x = x.split('{"PostPage":[')[1].split(']},"hostname"')[0]  # cut JS text at the beginning and at the end
        json_data = json.loads(x)

    return json_data

def get_post_media(link):
    info = get_post_info(link)

    response = []
    
    # handle different paths for different media type
    if info["graphql"]["shortcode_media"]["__typename"] == "GraphImage":
        media = info["graphql"]["shortcode_media"]["display_url"]
        suffix = ".jpg"
        response.append({'media': media, 'suffix': suffix})
    elif info["graphql"]["shortcode_media"]["__typename"] == "GraphVideo":
        media = info["graphql"]["shortcode_media"]["video_url"]
        suffix = ".mp4"
        response.append({'media': media, 'suffix': suffix})
    elif info["graphql"]["shortcode_media"]["__typename"] == "GraphSidecar":
        for content in info["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]:
            if content["node"]["__typename"] == "GraphImage":
                media = content["node"]["display_url"]
                suffix = ".jpg"
                response.append({'media': media, 'suffix': suffix})
            elif content["node"]["__typename"] == "GraphVideo":
                media = (content["node"]["video_url"])
                suffix = ".mp4"
                response.append({'media': media, 'suffix': suffix})

    return response


class InstagramScaper:
    def __init__(self):
        self.data = []
        self.account = ""

    def get_user_info(self, id, max_id):
        scrape_url = 'https://www.instagram.com/graphql/query/?query_hash=472f257a40c653c64c666ce877d59d2b&variables={"id":' + id + ',"first":12,"after":"' + max_id + '"}'
        r = requests.get(scrape_url)

        return json.loads(r.text)

    def get_user_posts(self, account, num_posts):
        self.account = account
        account_id = get_id(account)
        self.data = []

        max_id = ""
        counter = 0
        while len(self.data) < num_posts:
            counter += 1
            sg.one_line_progress_meter(f"Scraping posts of user {account}...", counter*12, num_posts, f"Scraping posts of user {account}...", orientation='h')
            info = self.get_user_info(account_id, max_id)  # get targeted user's posts

            # parse through all posts
            try:
                posts = [post['node'] for post in info["data"]["user"]["edge_owner_to_timeline_media"]["edges"]]
            except KeyError:
                return {"error": True, "response": "An error has occurred. Please try again later.", "code": 3}
            for post in posts:
                likes = post["edge_media_preview_like"]["count"]
                
                link = "https://instagram.com/p/{}/".format(post['shortcode'])
                
                media_type = get_media_type(post["__typename"])
                
                media = get_post_media(link)
                
                try:
                    caption = post["edge_media_to_caption"]["edges"][0]["node"]["text"]
                except IndexError:
                    caption = ""

                post_dict = {
                    "link": link,
                    "likes": likes,
                    "media_type": media_type,
                    "caption": caption,
                    "media": media,
                    "op": self.account
                                }
                self.data.append(post_dict)
            
            if not info["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]:  # check if more posts are available
                break
            
            max_id = info["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]  # get max id for next batch            
        
        self.data = self.data[:num_posts]  # removes last posts to match number of posts requested
        self.sort_posts()

    def sort_posts(self):
        # reverse = True (Sorts in descending order)
        # key is set to sort using second element of
        # sublist lambda has been used
        sub_li = self.data
        sub_li.sort(key=lambda x: int(x["likes"]), reverse=True)
        self.data = sub_li


def scrape(acc, num_posts):
    scraper = InstagramScaper()
    scraper.get_user_posts(acc, num_posts)
    return scraper.data
