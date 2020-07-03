import requests
import bs4
from urllib.request import urlopen


page = urlopen(
    'https://animenime.ru/naruto-muzyka-openingi-endingi-ost'
).read()
page = bs4.BeautifulSoup(page, 'lxml')
elements = page.findAll("div", {'class': "track"})

song_elements = []  # html elements containing song links
titles = []  # song titles
for el in elements:
    song_elements.append(el.source)
    titles.append(el.span.text)
links = []
for el in song_elements:
    # extracting source song links
    link = ''
    i = 0
    flag = False
    s = 0
    for i in str(el):
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
    links.append(link)
for i in range(len(links)):
    if 'movie' in links[i] or not links[i]:  # i didn't like songs from movies:)
        continue
    try:
        song = requests.get(links[i])
        # sorting sngs to directories
        directory = 'naruto_songs\\'
        if 'opening-tv-1' in links[i]:
            directory += 'openings_season1\\'
        elif 'opening-tv-2' in links[i]:
            directory += 'openings_season2\\'
        elif 'ending-tv-1' in links[i]:
            directory += 'endings_season1\\'
        elif 'ending-tv-2' in links[i]:
            directory += 'endings_season2\\'
        elif 'naruto-ost' in links[i]:
            directory += 'ost_season1\\'
        elif 'naruto-shippuuden-ost-1' in links[i]:
            directory += 'ost_season2\\'
        # creating mp.3 file
        with open(f'{directory}{titles[i]}.mp3', 'wb') as f:
            f.write(song.content)
    except Exception as e:
        print(e)
