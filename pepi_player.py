#!/usr/bin/env python3.6
""" pepi_player. Reproduce a list of videos from youtube using a query string

Usage:
    pepi-player [-h] [-r] [-f] [--loop] <query>

Options:
    -h --help       Show this screen.
    -r --random     Shuffle list.
    -f --first      Reproduce first video from list.
    --loop          Reproduce in loop
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
VIDEO_PLAYER_COMMAND = "omxplayer --aspect-mode fill -n -1"
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
    filename = pytube.helpers.safe_filename(yt.title)
    yt.streams.filter(subtype=VIDEO_FORMAT).first().download(TMP_DIRECTORY, filename)
    video_path = f"{TMP_DIRECTORY}/{filename}.{VIDEO_FORMAT}"
    player_command = VIDEO_PLAYER_COMMAND.split(' ') + [video_path]
    subprocess.run(player_command)


def main():
    arguments = docopt.docopt(__doc__)
    video_ids = search_video(arguments['<query>'])

    if arguments['--random']:
        random.shuffle(video_ids)

    if arguments['--first']:
        play_video(video_ids[0])
        exit

    for video_id in video_ids:
        play_video(video_id)

    if arguments['--loop']:
        main()


if __name__ == "__main__":
    main()
