import os
import requests
import bs4

show = '' # Name of show goes here

addy = 'https://www.blogtalkradio.com'
showPage = addy + '/' + show + '/'

print('BlogTalkRadio bulk downloader\n')
print('Downloading episodes from ' + showPage + '...')

try:
    os.makedirs(show)
    print('Creating directory...')
except:
    print('Directory \'' + show + '\' already exists, moving on...')

crawling = True
currentPage = 1
while crawling:
    print('\nLoading index page ' + str(currentPage) + '...')
    
    res = requests.get(showPage + str(currentPage))
    res.raise_for_status()
    indexPage = bs4.BeautifulSoup(res.text, features='html.parser')

    buttonList = indexPage.select('.play-button')
    if not buttonList:
        crawling = False
        break

    episodeList = []
    for item in buttonList:
        episodeList.append(item.get('href'))

    for episode in episodeList:
        episodeFile = episode + '.mp3'
        episodeName = episodeFile[1:].replace('/', '-')
        episodeAddy = addy + episodeFile
        episodePath = os.path.join(show, episodeName)
        
        if os.path.isfile(episodePath):
            print(episodeName + ' already exists, moving on...')
            continue
        
        req = requests.get(episodeAddy)
        req.raise_for_status()
        currentFile = open(episodePath, 'wb')
        for part in req.iter_content(100000):
            currentFile.write(part)
        currentFile.close()
        
        print(episodeName + ' completed')
    
    currentPage = currentPage + 1
    
print('\nAll episodes downloaded')
input('Press ENTER to quit...')
