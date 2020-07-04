import requests
import bs4
from urllib.request import urlopen
import sys
import time


start = time.perf_counter()
page = urlopen(
    'https://animenime.ru/naruto-muzyka-openingi-endingi-ost'
).read()
page = bs4.BeautifulSoup(page, 'lxml')
elements = page.findAll("div", {'class': "track"})


songs = {}  # dict title: source
for el in elements:
    songs[el.span.text] = el.source
links = []
for title, src in songs.items():
    # extracting source song links
    link = ''
    i = 0
    flag = False
    s = 0
    for i in str(src):
        if i == '=':
            flag = True
            continue
        if flag:
            if s > 1:
                break
            if i == '"':
                s += 1
                continue
            link += i
    songs[title] = link
i = 0
for title in songs:
    # i didn't like songs from movies:)
    if ('movie' in songs[title]) or not songs[title]:
        continue
    try:
        i += 1
        song = requests.get(songs[title])
        # sorting songs to directories
        directory = 'naruto_songs\\'
        if 'opening-tv-1' in songs[title]:
            directory += 'openings_season1\\'
        elif 'opening-tv-2' in songs[title]:
            directory += 'openings_season2\\'
        elif 'ending-tv-1' in songs[title]:
            directory += 'endings_season1\\'
        elif 'ending-tv-2' in songs[title]:
            directory += 'endings_season2\\'
        elif 'naruto-ost' in songs[title]:
            directory += 'ost_season1\\'
        elif 'naruto-shippuuden-ost' in songs[title]:
            directory += 'ost_season2\\'
        # creating mp.3 file
        with open(f'{directory}{i} {title}.mp3', 'wb') as f:
            f.write(song.content)
    except Exception as e:
        print(e)
finish = time.perf_counter()
print(
    f"Succesfully downloaded {i} songs in {round(finish - start) // 60} m and {round(finish - start) % 60} s"
)
