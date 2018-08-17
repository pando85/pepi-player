#!/usr/bin/env python3

import pathlib
import pytube
import re
import urllib.request
import urllib.parse

def search_video(query):
    query_string = urllib.parse.urlencode({"search_query" : query})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    return search_results

def main():
    video = search_video('opa')[0]
    directory = '/tmp/pepi_video'
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

    yt = pytube.YouTube(video)
    yt.streams.first().download(directory)


if __name__ == "__main__":
    main()