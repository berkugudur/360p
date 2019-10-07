from datetime import datetime
from itertools import dropwhile, takewhile
from shutil import copyfile

import instaloader
import csv
import os

OUTPUT_FILE = "output.csv"
BACKUP_FOLDER = "backup"
DOWNLOAD_FOLDER = "photos"
USERNAMES_FILE = "usernames.csv"

def backup_and_create():
    if not os.path.exists(USERNAMES_FILE):
        sys.exit("{} file is not exists".format(USERNAMES_FILE))

    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)

    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    if os.path.exists(OUTPUT_FILE):
        copyfile(OUTPUT_FILE, "{}/{}_{}".format(BACKUP_FOLDER, datetime.now(), OUTPUT_FILE))

    return open(OUTPUT_FILE, "w+")

def get_usernames():
    usernames = []
    with open(USERNAMES_FILE) as usernames_file:
        rows = csv.reader(usernames_file)
        for row in rows:
            usernames.append(row[0])
    return usernames

def download_post(L, username, profile, post, output):
    row = "{},{},{},{}\n".format(username, profile.followers, post.shortcode, post.likes)
    print("INFO: {}".format(row), end = '')
    output.write(row)
    L.download_post(post, DOWNLOAD_FOLDER)

def download_posts(L, usernames, output):
    SINCE = datetime(2019, 10, 1)
    UNTIL = datetime(2018, 5, 1)
    for username in usernames:
        profile = instaloader.Profile.from_username(L.context, username)
        posts = profile.get_posts()
        print( "INFO: Downloading {}'s contents.".format(username))
        for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
            download_post(L, username, profile, post, output)

def main():
    L = instaloader.Instaloader(quiet=True, filename_pattern="{shortcode}", download_videos=False, download_video_thumbnails=False, download_geotags=False,
                            download_comments=False, save_metadata=False, compress_json=False, post_metadata_txt_pattern="")
    output = backup_and_create()
    download_posts(L, get_usernames(), output)

if __name__ == '__main__':
    main()