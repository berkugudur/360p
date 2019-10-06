from datetime import datetime
from itertools import dropwhile, takewhile

import instaloader
import csv

L = instaloader.Instaloader(quiet=True, filename_pattern="{shortcode}", download_videos=False, download_video_thumbnails=False, download_geotags=False,
                            download_comments=False, save_metadata=False, compress_json=False, post_metadata_txt_pattern="")

SINCE = datetime(2019, 10, 1)
UNTIL = datetime(2018, 5, 1)

usernames = []
output = open("output.csv", "w+")
with open("usernames.csv") as usernames_file:
    rows = csv.reader(usernames_file)
    for row in rows:
        usernames.append(row[0])

for username in usernames:
    profile = instaloader.Profile.from_username(L.context, username)
    posts = profile.get_posts()
    followers = profile.followers
    print( "INFO: Downloading " + username + "'s contents.")
    for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
        row = username + "," + str(followers) + "," + post.shortcode + "," + str(post.likes)
        print("INFO: " + row)
        output.write(row + "\n")
        L.download_post(post, 'photos')