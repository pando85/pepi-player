#!/usr/bin/env python3
""" pepi_player.

Usage:
    pepi-player [-h] [-r] <query>

Options:
    -h --help       Show this screen.
    -r --random     Reproduce random videos from <query> search.
"""

import docopt
import pathlib
import pytube
import random
import re
import subprocess
import urllib.parse
import urllib.request


YOUTUBE_URL = "http://www.youtube.com"
VIDEO_FORMAT = "mp4"
VIDEO_PLAYER_COMMAND = "omxplayer -n -1"
TMP_DIRECTORY = '/tmp/pepi_video'


def search_video(query):
    query_string = urllib.parse.urlencode({"search_query": query})
    html_content = urllib.request.urlopen(f"{YOUTUBE_URL}/results?{query_string}")
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    return search_results


def play_video(video_id):
    video_url = f"{YOUTUBE_URL}/watch?v={video_id}"
    pathlib.Path(TMP_DIRECTORY).mkdir(parents=True, exist_ok=True)

    yt = pytube.YouTube(video_url)
    yt.streams.filter(subtype=VIDEO_FORMAT).first().download(TMP_DIRECTORY)
    video_path = f"{TMP_DIRECTORY}/{yt.title}.{VIDEO_FORMAT}"
    player_command = VIDEO_PLAYER_COMMAND.split(' ') + [video_path]
    subprocess.run(player_command)


def main():
    arguments = docopt.docopt(__doc__)
    video_ids = search_video(arguments['<query>'])
    if arguments['--random']:
        for video_id in random.shuffle(video_ids):
            play_video(video_id)
    else:
        play_video(video_ids[0])


if __name__ == "__main__":
    main()
