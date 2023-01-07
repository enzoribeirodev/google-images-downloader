import pyppeteer.errors
from requests_html import HTMLSession
import os


def get_formatted_urls(thing_to_look_for, n_of_imgs):
    base_url = f"https://www.google.com/search?q={thing_to_look_for}&tbm=isch&tbs=isz:l"

    session = HTMLSession()
    response = session.get(base_url)

    if n_of_imgs > 100:
        response.html.render(scrolldown=1000, timeout=12)

    data_ids = [
        div.attrs["data-id"]
        for div in response.html.find("div[class='isv-r PNCib MSM1fd BUooTd']")
    ]

    return [base_url + "&#imgrc=" + data_id for data_id in data_ids][:n_of_imgs]


def fetch(session, url):
    try:
        response = session.get(url)
        response.html.render(sleep=1, timeout=8)
    except pyppeteer.errors.TimeoutError:
        print("Timeout Exceeded. It was not possible to download this image")
        return
    return response.html


def work(s, url):
    response = fetch(s, url)
    print(response, type(response))
    if response:
        high_quality_img_path = response.find(
            "a[class='eHAdSb'] > img[class*='n3VNCb'][src*='http']", first=True
        )
        if high_quality_img_path:
            src = high_quality_img_path.attrs["src"]
            return src
        return
    return


def get_src(s, urls):
    src_gen = (work(s, url) for url in urls)
    return src_gen


def download_images(thing_to_look_for, n_of_imgs):
    img_number = 0
    s = HTMLSession()

    if not os.path.exists(f"{thing_to_look_for} image folder"):
        os.mkdir(f"{thing_to_look_for} image folder")

    os.chdir(f"{thing_to_look_for} image folder")

    for src in get_src(s, get_formatted_urls(thing_to_look_for, n_of_imgs)):
        if src:
            img_number += 1
            response = s.get(src)
            with open(f"{thing_to_look_for}image_{img_number}.png", "wb") as file:
                file.write(response.content)
                print(f"downloading_{thing_to_look_for}_image_{img_number}")
    return


if __name__ == "__main__":
    download_images(
        input("What are you looking for? "),
        int(input("How many images do you want to download [MAX 400]? ")),
    )
