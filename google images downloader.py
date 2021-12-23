import requests
from bs4 import BeautifulSoup
import os


thing_to_look_for = input('What are you looking for? ')
num_of_imgs = int(input(f'How many images of {thing_to_look_for} do you want to download? '))
img_number = 0
all_imgs_index = 0

base_url = 'https://www.google.com/search?q={}&rlz=1C1SQJL_' \
         'enBR944BR944&biw=1422&bih=1014&gbv=1&tbm=isch&ei=' \
         'OWbDYYvaN7LX5OUPq4eg0AU&start={}&spytha=N'

formatted_url = base_url.format(thing_to_look_for, '00')
response = requests.get(formatted_url)
soup = BeautifulSoup(response.content, 'html.parser')
all_imgs = soup.find_all('img', {'class': 'yWs4tf'})
imgs_to_be_downloaded = []

if num_of_imgs <= 20:
    imgs_to_be_downloaded = all_imgs[:num_of_imgs]

else:
    for img in all_imgs[:20]:
        imgs_to_be_downloaded.append(img)

    for page in range(20, num_of_imgs, 20):
        formatted_url = base_url.format(thing_to_look_for, page)
        response = requests.get(formatted_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        all_imgs = soup.find_all('img', {'class': 'yWs4tf'})

        for img in all_imgs:
            imgs_to_be_downloaded.append(img)
            if len(imgs_to_be_downloaded) == num_of_imgs:
                break

srcs = [img.get('src') for img in imgs_to_be_downloaded]

if not os.path.exists(f'{thing_to_look_for} image folder'):
    os.mkdir(f'{thing_to_look_for} image folder')

os.chdir(f'{thing_to_look_for} image folder')

for src in srcs:
    img_number += 1
    response = requests.get(src)
    with open(f'{thing_to_look_for}image_{img_number}.png', 'wb') as file:
        file.write(response.content)
        print(f'downloading {thing_to_look_for}image_{img_number}')
