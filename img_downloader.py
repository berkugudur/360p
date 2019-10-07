from datetime import datetime
from itertools import dropwhile, takewhile
from shutil import copyfile

import instaloader
import csv
import os.path

def backup_and_create(path):
    # move last output to backup folder
    if os.path.exists(path):
        copyfile(path, "backup/"+ str(datetime.now()) + "_" + path)
    return open(path, "w+")

def get_usernames(path):
    usernames = []
    with open(path) as usernames_file:
        rows = csv.reader(usernames_file)
        for row in rows:
            usernames.append(row[0])
    return usernames

def download_post(L, username, profile, post, output):
    row = "{},{},{},{}\n".format(username, profile.followers, post.shortcode, post.likes)
    print("INFO: {}".format(row), end = '')
    output.write(row)
    L.download_post(post, 'photos')

def download_posts(L, usernames, output):
    SINCE = datetime(2019, 10, 1)
    UNTIL = datetime(2018, 5, 1)
    for username in usernames:
        profile = instaloader.Profile.from_username(L.context, username)
        posts = profile.get_posts()
        print( "INFO: Downloading " + username + "'s contents.")
        for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
            download_post(L, username, profile, post, output)

def main():
    L = instaloader.Instaloader(quiet=True, filename_pattern="{shortcode}", download_videos=False, download_video_thumbnails=False, download_geotags=False,
                            download_comments=False, save_metadata=False, compress_json=False, post_metadata_txt_pattern="")
    output = backup_and_create("output.csv")
    usernames = get_usernames("usernames.csv")
    download_posts(L, usernames, output)

if __name__ == '__main__':
    main()