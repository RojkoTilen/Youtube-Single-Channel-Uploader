from os import walk
from color_matcher import ColorMatcher
from color_matcher.io_handler import load_img_file, save_img_file, FILE_EXTS
from color_matcher.normalizer import Normalizer
from PIL import Image
import os
import time
from moviepy.editor import *
import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
import os
from selenium import webdriver
import numpy as np
import json
from os import walk
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
import random
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.ui as ui
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from Google import Create_Service
from mutagen.mp3 import MP3
import requests
import socket

CLIENT_SECRET_FILE = 'ony_cred.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
import patreon
access_token = '5FRCteYGTzWk4ho2CekJUnBEF5251Tb_D8pjj3m-AkI'
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)


def get_list_of_file_names(dir_with_path):
    f = []
    file_dict = {}
    mp3_array = []
    patreon_dict = {}
    for (dirpath, dirnames, filenames) in walk(dir_with_path):
        f.extend(filenames)
        break
    for name in f:
        if ".png" in name:
            file_name = dir_with_path + "\\" + name
            file_dict["background"] = file_name
        elif ".mp4" in name:
            file_name = dir_with_path + "\\" + name
            file_dict["video"] = file_name
        elif ".mp3" in name:
            file_name = dir_with_path + "\\" + name
            mp3_array.append(file_name)

    file_dict["music"] = mp3_array
    return file_dict

def get_mp3_lengths(mp3_arr):
    length_arr = []
    time_dict = {}

    for key in mp3_arr:
        audio = MP3(key)
        audio_time_string = datetime.timedelta(seconds=int(audio.info.length))

        print(audio_time_string)

        length_arr.append(audio_time_string)

    length_arr_override = length_arr

    for i in range(0, len(length_arr)):
        if i == 0:
            time_dict[str(datetime.timedelta(seconds=0))] = str(length_arr[i])
            continue
        time_dict[str(length_arr_override[i-1])] = str(length_arr_override[i-1]+length_arr_override[i])
        length_arr_override[i] = length_arr_override[i-1]+length_arr_override[i]

    print(time_dict)
    description = """"""
    stamp_array = []

    for key in time_dict:
        timestamp = key.split(':', 1)[1]
        stamp_array.append(timestamp)
        description = description + timestamp + "\n"

    print("description")

    print(stamp_array)

    return stamp_array

def url_shortener(url):
    parameters = {"url": url}
    headers_dict = {
        'content-type': 'application/x-www-form-urlencoded',
        'x-rapidapi-host': 'url-shortener-service.p.rapidapi.com',
        'x-rapidapi-key': 'ee94345ecamshcc45f2ef587e60ep1d4f6bjsn67c823e0d0a0'
    }

    response = requests.post("https://url-shortener-service.p.rapidapi.com/shorten", data=parameters,headers=headers_dict)

    print(response.json())
    jsonres = response.json()
    print("response STRING URL TEST")
    print(jsonres["result_url"])

    return jsonres["result_url"]

def get_patreon_links(mp3_array):

    parsed_name_arr = []

    for file_name in mp3_array:
        splt_char = "\\"
        temp = file_name.split(splt_char)
        res = splt_char.join(temp[4:])

        splt_char = "("
        temp = res.split(splt_char)
        parsed_name = splt_char.join(temp[:1])
        parsed_name_arr.append(parsed_name)

    driver.get("https://www.patreon.com/login")

    time.sleep(40)

    username = driver.find_element_by_id('email')
    username.send_keys("onymusicgroup@gmail.com")
    time.sleep(3)

    password = driver.find_element_by_id('password')
    password.send_keys("070222677Kurac")
    time.sleep(3)

    wait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="renderPageContentWrapper"]/div[1]/div/div/div[1]/div/div[1]/form/div[5]/button'))).click()
    print("-- LOGIN BUTTON ")
    time.sleep(5)

    patreon_link_dict = {}

    for mp3_name in parsed_name_arr:
        time.sleep(5)

        wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="reactTarget"]/div/div[1]/div[2]/div/div/nav/div[1]/div/a'))).click()

        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="search-posts"]').send_keys(mp3_name)
        driver.find_element_by_xpath('//*[@id="search-posts"]').send_keys(Keys.ENTER)

        time.sleep(10)

        driver.execute_script("window.scrollTo(0, 800)")
        time.sleep(5)


        wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="renderPageContentWrapper"]/div[1]/div[5]/div/div/div/div[4]/div/div/ul/li/div/div/div/div/div[2]/div[1]/div[2]/span/a'))).click()
        time.sleep(5)

        patreon_link_dict[mp3_name] = url_shortener(driver.current_url)

        wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="reactTarget"]/div/div[1]/div[2]/div/div/nav/a'))).click()
        time.sleep(5)


    driver.quit()

    print(patreon_link_dict)

    return patreon_link_dict


def make_youtube_n_desc_tags(file_dict, video_id):

    upload_date_time = datetime.datetime(2022, 3, 14, 17, 0, 0).isoformat() + '.000Z'

    full_file_name = file_dict["background"]

    splt_char = "\\"
    temp = full_file_name.split(splt_char)
    res = splt_char.join(temp[4:])

    splt_char = "."
    temp = res.split(splt_char)
    youtube_name = splt_char.join(temp[:1])

    youtube_name_for_tags = youtube_name.replace("(", "")
    youtube_name_for_tags = youtube_name_for_tags.replace(")", "")

    tags_1 = [youtube_name_for_tags.lower()]

    mp3name_link_dict = get_patreon_links(file_dict["music"])
    print("mp3name_link_dict")

    print(mp3name_link_dict)

    timestamp_arr = get_mp3_lengths(file_dir_dict["music"])

    timestamp_description = """"""
    i = 0
    for mp3 in mp3name_link_dict:
        timestamp_description = timestamp_description + timestamp_arr[i] + " " + mp3 + " - " + mp3name_link_dict[mp3] + "\n"
        i = i + 1

    print(timestamp_description)


    if "future bass" in youtube_name.lower() or "dubstep" in youtube_name.lower() or "edm" in youtube_name.lower():
        tags_2 = ["no copyright music", "vlog music", "vlog music no copyright", "royalty free music", "no copyright music vlog", "non copyrighted music", "copyright free music", "no copyright background music", "no copyright music for youtube videos", "vlog music no copyright upbeat", "vlog music background"]
        timestamp_description = """
No Copyright Electronic Background Music For Videos! ✨
⏬ DOWNLOAD HERE : 
""" + timestamp_description + """

📸 Instagram : http://bit.ly/OnyInstagram​

✨ This is an electronic royalty free background no copyright track.

❗ Usage without the purchase of a license is forbidden. You can buy a license with the link above. ❗ 

It is FORBIDDEN to: 

- Add vocals to this track.
- Remix of remake this track.
- Sell this track.
- Use this track without a license.

#nocopyrightmusic #futurebassnocopyrightmusic #edmnocopyrightmusic #vlognocopyrightmusic
        """

        print(timestamp_description)
    elif "technology" in youtube_name.lower() or "abstract" in youtube_name.lower() or "future" in youtube_name.lower():
        tags_2 = ["royalty free music upbeat", "copyright free music upbeat", "sport music no copyright", "corporate music", "background music non copyrighted", "royalty free upbeat music", "upbeat copyright free music", "audiojungle music", "no copyright music fashion", "royalty free music", "no copyright music", "music for travel", "travel music", "event background music", "energetic music no copyright", "Music for youtube", "tropical house no copyright", "corporate no copyright music", "corporate royalty free music"]
        timestamp_description = """
No Copyright Technology Background Music For Videos! ✨
⏬ DOWNLOAD HERE : 
""" + timestamp_description + """

📸 Instagram : http://bit.ly/OnyInstagram​

✨ This is an technology no copyright track.

❗ Usage without the purchase of a license is forbidden. You can buy a license with the link above. ❗ 

It is FORBIDDEN to: 

- Add vocals to this track.
- Remix of remake this track.
- Sell this track.
- Use this track without a license.

#nocopyrightmusic #technologynocopyrightmusic #abstractnocopyrightmusic
        """

        print(timestamp_description)

    elif "electro" in youtube_name.lower() or "cyberpunk" in youtube_name.lower() or "techno" in youtube_name.lower():
        tags_2 = ["cyberpunk music", "cyberpunk no copyright music", "midtempo music", "midtempo no copyright music", "no copyright background music", "sport music no copyright", "sports music no copyright", "royalty free", "sports background music no copyright", "no copyright music sport", "cyberpunk 2077", "royalty free music", "energetic music no copyright", "music for fitness royalty free", "kloud", "hyper no copytight music", "devil in a red dress", "call 911 i'm a killer", "infraction music", "infraction", "copyright free music"]
        timestamp_description = """
No Copyright Cyberpunk Background Music For Videos! ✨
⏬ DOWNLOAD HERE : 
""" + timestamp_description + """

📸 Instagram : http://bit.ly/OnyInstagram​

✨ This is an cyberpunk no copyright track.

❗ Usage without the purchase of a license is forbidden. You can buy a license with the link above. ❗ 

It is FORBIDDEN to: 

- Add vocals to this track.
- Remix of remake this track.
- Sell this track.
- Use this track without a license.

#nocopyrightmusic #cyberpunknocopyrightmusic #technonocopyrightmusic #electronocopyrightmusic
        """

        print(timestamp_description)
    elif "synthwave" in youtube_name.lower() or "80s" in youtube_name.lower():
        tags_2 = ["commercial no copyright music", "free commercial background music no copyright", "free commercial music no copyright", "mokka", "mokkamusic", "premium no copyright music", "80s no copyright music", "80's no copyright music", "new retro wave no copyright", "no copyright music 80s retro synthwave", "retro wave no copyright music", "royalty free vhs music", "stranger things no copyright music", "synthwave no copyright music", "vhs music no copyright", "vhs royalty free music", "night city no copyright music"]
        timestamp_description = """
No Copyright Synthwave Background Music For Videos! ✨
⏬ DOWNLOAD HERE : 
""" + timestamp_description + """

📸 Instagram : http://bit.ly/OnyInstagram​

✨ This is an synthwave no copyright track.

❗ Usage without the purchase of a license is forbidden. You can buy a license with the link above. ❗ 

It is FORBIDDEN to: 

- Add vocals to this track.
- Remix of remake this track.
- Sell this track.
- Use this track without a license.

#nocopyrightmusic #synthwavenocopyrightmusic #80snocopyrightmusic #vintagenocopyrightmusic
        """
    elif "house" in youtube_name.lower():
        tags_2 = ["fashion show music background", "background music for fashion show", "fashion background music no copyright", "copyright free music upbeat", "upbeat royalty free music", "background music no copyright", "no copyright music fashion", "music for fashion show", "fashion house", "royalty free fashion", "fashion background music", "background music for fashion", "royalty free fashion music", "fashion music", "deep house no copyright", "deep house fashion music", "no copyright stylish music", "modeling music"]
        timestamp_description = """
No Copyright House Background Music For Videos! ✨
⏬ DOWNLOAD HERE : 
""" + timestamp_description + """

📸 Instagram : http://bit.ly/OnyInstagram​

✨ This is a house no copyright track.

❗ Usage without the purchase of a license is forbidden. You can buy a license with the link above. ❗ 

It is FORBIDDEN to: 

- Add vocals to this track.
- Remix of remake this track.
- Sell this track.
- Use this track without a license.

#nocopyrightmusic #housenocopyrightmusic #vlognocopyrightmusic #fashionnocopyrightmusic
        """
    elif "lofi" in youtube_name.lower() or "lofi" in youtube_name.lower() or "lo-fi" in youtube_name.lower() or "lo fi" in youtube_name.lower():
        tags_2 = ["royalty free music", "copyright free music", "no copyright music sport", "video game music", "free music", "sports background music no copyright", "commercial background music", "background music", "royalty free music upbeat", "fashion music no copyright", "copyright free music upbeat", "upbeat royalty free music", "background music no copyright", "no copyright music fashion", "lofi hip-hop", "hip-hop no copyright", "boom bap no copyright", "vlog music", "travel music"]
        timestamp_description = """
No Copyright Lofi Background Music For Videos! ✨
⏬ DOWNLOAD HERE : 
""" + timestamp_description + """

📸 Instagram : http://bit.ly/OnyInstagram​

✨ This is a lofi no copyright track.

❗ Usage without the purchase of a license is forbidden. You can buy a license with the link above. ❗ 

It is FORBIDDEN to: 

- Add vocals to this track.
- Remix of remake this track.
- Sell this track.
- Use this track without a license.

#nocopyrightmusic #lofinocopyrightmusic #vlognocopyrightmusic #hiphopnocopyrightmusic
        """
    elif "hip hop" in youtube_name.lower() or "hip-hop" in youtube_name.lower() or "hip" in youtube_name.lower() or "hop" in youtube_name.lower() or "hiphop" in youtube_name.lower() or "vlog" in youtube_name.lower():
        tags_2 = ["commercial no copyright music", "free commercial background music no copyright", "free commercial music no copyright", "mokka", "mokkamusic", "premium no copyright music", "non copyrighted music", "chill background music no copyright", "chill background no copyright music", "chill music no copyright", "chill no copyright music", "disco no copyright music", "disco party music no copyright", "modern disco music no copyright", "vlog no copyright music disco", "stylish funky beat no copyright music"]
        timestamp_description = """
No Copyright Hip Hop Background Music For Videos! ✨
⏬ DOWNLOAD HERE : 
""" + timestamp_description + """

📸 Instagram : http://bit.ly/OnyInstagram​

✨ This is a hip hop no copyright track.

❗ Usage without the purchase of a license is forbidden. You can buy a license with the link above. ❗ 

It is FORBIDDEN to: 

- Add vocals to this track.
- Remix of remake this track.
- Sell this track.
- Use this track without a license.

#nocopyrightmusic #vlognocopyrightmusic #hiphopnocopyrightmusic
        """
    elif "trap" in youtube_name.lower():
        tags_2 = ["no copyright music", "fashion no copyright music", "fitness no copyright music", "workout no copyright music", "gym vlog music no copyright", "no copyright music sport", "fashion music no copyright", "sport music no copyright", "stylish no copyright music", "energetic no copyright music", "sport no copyright music", "no copyright music energetic", "trap no copyright music", "royalty free fashion", "creative commons music", "no copyright stylish music", "inaudio.org", "infraction no copyright music", "infraction"]
        timestamp_description = """
No Copyright Trap Background Music For Videos! ✨
⏬ DOWNLOAD HERE : 
""" + timestamp_description + """

📸 Instagram : http://bit.ly/OnyInstagram​

✨ This is a trap no copyright track.

❗ Usage without the purchase of a license is forbidden. You can buy a license with the link above. ❗ 

It is FORBIDDEN to: 

- Add vocals to this track.
- Remix of remake this track.
- Sell this track.
- Use this track without a license.

#nocopyrightmusic #vlognocopyrightmusic #trapnocopyrightmusic #sportnocopyrightmusic
        """
    elif "pop" in youtube_name.lower() or ("upbeat dance") in youtube_name.lower() or ("dance upbeat") in youtube_name.lower() or "dance" in youtube_name.lower() or "party" in youtube_name.lower():
        tags_2 = ["commercial no copyright music", "free commercial background music no copyright", "free commercial music no copyright", "modern music no copyright", "mokka"]
        timestamp_description = """
No Copyright Pop Background Music For Videos! ✨
⏬ DOWNLOAD HERE : 
""" + timestamp_description + """

📸 Instagram : http://bit.ly/OnyInstagram​

✨ This is a pop no copyright track.

❗ Usage without the purchase of a license is forbidden. You can buy a license with the link above. ❗ 

It is FORBIDDEN to: 

- Add vocals to this track.
- Remix of remake this track.
- Sell this track.
- Use this track without a license.

#nocopyrightmusic #popnocopyrightmusic #dancenocopyrightmusic #summernocopyrightmusic #vlognocopyrightmusic
        """
    elif "percussion" in youtube_name.lower() or "stomp" in youtube_name.lower() or "drums" in youtube_name.lower():
        tags_2 = ["commercial no copyright music", "free commercial background music no copyright", "free commercial music no copyright", "modern music no copyright", "mokka", "mokkamusic", "premium no copyright music", "action sport no copyright music", "sport action no copyright music", "sport action royalty free music", "sport no copyright music", "stomps and claps no copyright music", "percussion no copyright music", "drive drums no copyright music", "claps no copyright music"]
        timestamp_description = """
No Copyright Percussion Background Music For Videos! ✨
⏬ DOWNLOAD HERE : 
""" + timestamp_description + """

📸 Instagram : http://bit.ly/OnyInstagram​

✨ This is a pop no copyright track.

❗ Usage without the purchase of a license is forbidden. You can buy a license with the link above. ❗ 

It is FORBIDDEN to: 

- Add vocals to this track.
- Remix of remake this track.
- Sell this track.
- Use this track without a license.

#nocopyrightmusic #percussionnocopyrightmusic #stompnocopyrightmusic #typographynocopyrightmusic
        """
    elif "corporate" in youtube_name.lower() or "business" in youtube_name.lower():
        tags_2 = ["royalty free music upbeat", "copyright free music upbeat", "sport music no copyright", "corporate music", "background music non copyrighted", "royalty free upbeat music", "upbeat copyright free music", "audiojungle music", "no copyright music fashion", "royalty free music", "no copyright music", "music for travel", "travel music", "event background music", "energetic music no copyright", "Music for youtube", "tropical house no copyright", "corporate no copyright music", "corporate royalty free music"]
        timestamp_description = """
No Copyright Corporate Background Music For Videos! ✨
⏬ DOWNLOAD HERE : 
""" + timestamp_description + """

📸 Instagram : http://bit.ly/OnyInstagram​

✨ This is a corporate no copyright track.

❗ Usage without the purchase of a license is forbidden. You can buy a license with the link above. ❗ 

It is FORBIDDEN to: 

- Add vocals to this track.
- Remix of remake this track.
- Sell this track.
- Use this track without a license.

#nocopyrightmusic #corporatenocopyrightmusic #bussinessnocopyrightmusic
        """
    elif "ambient" in youtube_name.lower() or "documentaries" in youtube_name.lower() or "documentary" in youtube_name.lower():
        tags_2 = ["royalty free music upbeat", "copyright free music upbeat", "sport music no copyright", "corporate music", "background music non copyrighted", "royalty free upbeat music", "upbeat copyright free music", "audiojungle music", "no copyright music fashion", "royalty free music", "no copyright music", "music for travel", "travel music", "event background music", "energetic music no copyright", "Music for youtube", "tropical house no copyright", "corporate no copyright music", "corporate royalty free music"]
        timestamp_description = """
No Copyright Ambient Documentary Background Music For Videos! ✨
⏬ DOWNLOAD HERE : 
""" + timestamp_description + """

📸 Instagram : http://bit.ly/OnyInstagram​

✨ This is a corporate no copyright track.

❗ Usage without the purchase of a license is forbidden. You can buy a license with the link above. ❗ 

It is FORBIDDEN to: 

- Add vocals to this track.
- Remix of remake this track.
- Sell this track.
- Use this track without a license.

#nocopyrightmusic #documentarynocopyrightmusic #ambientnocopyrightmusic
        """
    elif "funk" in youtube_name.lower() or "funky" in youtube_name.lower() or "groove" in youtube_name.lower() or "jazz" in youtube_name.lower() or "groovy" in youtube_name.lower():
        tags_2 = ["commercial no copyright music", "free commercial background music no copyright", "free commercial music no copyright", "mokka", "mokkamusic", "premium no copyright music", "non copyrighted music", "fashion house music no copyright", "fashion house no copyright", "fashion house royalty free", "fashion pop no copyright music", "modern fashion music no copyright", "pop fashion music no copyright", "disco no copyright music", "modern disco music no copyright", "vlog no copyright music disco"]
        timestamp_description = """
No Copyright Funk Documentary Background Music For Videos! ✨
⏬ DOWNLOAD HERE : 
""" + timestamp_description + """

📸 Instagram : http://bit.ly/OnyInstagram​

✨ This is a funk/jazz no copyright track.

❗ Usage without the purchase of a license is forbidden. You can buy a license with the link above. ❗ 

It is FORBIDDEN to: 

- Add vocals to this track.
- Remix of remake this track.
- Sell this track.
- Use this track without a license.

#nocopyrightmusic #jazznocopyrightmusic #funknocopyrightmusic
        """
    elif "rock" in youtube_name.lower() or "indie rock" in youtube_name.lower():
        tags_2 = ["commercial no copyright music", "free commercial background music no copyright", "free commercial music no copyright", "modern music no copyright", "mokka", "mokkamusic", "premium no copyright music", "action sport rock free music", "action sport rock music no copyright", "hard rock no copyright music", "rock no copyright music instrumental", "sport rock no copyright music", "stylish powerful rock background music", "stylish rock background music", "stylish rock music", "stylish rock royalty free music"]
        timestamp_description = """
No Copyright Rock Documentary Background Music For Videos! ✨
⏬ DOWNLOAD HERE : 
""" + timestamp_description + """

📸 Instagram : http://bit.ly/OnyInstagram​

✨ This is a rock/indie rock no copyright track.

❗ Usage without the purchase of a license is forbidden. You can buy a license with the link above. ❗ 

It is FORBIDDEN to: 

- Add vocals to this track.
- Remix of remake this track.
- Sell this track.
- Use this track without a license.

#nocopyrightmusic #rocknocopyrightmusic #indienocopyrightmusic
        """
    elif "cinematic" in youtube_name.lower() or "epic" in youtube_name.lower() or "trailer" in youtube_name.lower():
        tags_2 = ["no copyright music", "cinematic no copyright music", "romantic no copyright music", "action no copyright music", "inspiring no copyright music", "drone no copyright music", "dramatic no copyright music", "documentary no copyright music", "cinematic music no copyright", "epic no copyright background music", "cinematic background music no copyright", "orchestra no copyright", "dramatic music no copyright", "epic background music no copyright", "inaudio.org", "infraction no copyright music", "infraction"]
        timestamp_description = """
No Copyright Cinematic Epic Documentary Background Music For Videos! ✨
⏬ DOWNLOAD HERE : 
""" + timestamp_description + """

📸 Instagram : http://bit.ly/OnyInstagram​

✨ This is a cinematic/trailer no copyright track.

❗ Usage without the purchase of a license is forbidden. You can buy a license with the link above. ❗ 

It is FORBIDDEN to: 

- Add vocals to this track.
- Remix of remake this track.
- Sell this track.
- Use this track without a license.

#nocopyrightmusic #cinematicnocopyrightmusic #trailernocopyrightmusic
        """
    else:
        return

    split_tags = youtube_name_for_tags.lower().split()
    print(split_tags)

    tags = split_tags+tags_1
    print(tags)


    request_body = {
        'videoId': video_id,
        'snippet': {
            'categoryId': "10",
            'title': youtube_name,
            'description': timestamp_description,
            'tags': tags
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': upload_date_time,
            'selfDeclaredMadeForKids': False,
        },
        'notifySubscribers': True
    }

    return request_body


def upload_video(request_body, file_dir_dict):

    print(request_body)
    print(file_dir_dict["video"])
    print(file_dir_dict["background"])

    media_file = MediaFileUpload(file_dir_dict["video"])
    socket.setdefaulttimeout(2000)

    response_upload = service.videos().update(
        part='snippet,status',
        body=request_body
    ).execute()

    response_upload = service.videos().update(
        body={
            "id": "JT8R2vmhavA",
            "snippet": {
                "tags": [
                    "test",
                    "nekaj",
                    "nekaj"
                ]
            }
        }
    ).execute()

    socket.setdefaulttimeout(2000)

    service.thumbnails().set(
        videoId=response_upload.get(request_body["id"]),
        media_body=MediaFileUpload(file_dir_dict["background"])
    ).execute()


if __name__ == "__main__":
    socket.setdefaulttimeout(2000)


    video_id = "sNS5pqd0wp8"

    upload_date_time = datetime.datetime(2022, 3, 14, 17, 0, 0).isoformat() + '.000Z'

    file_dir_dict = get_list_of_file_names("C:\\Ony Music Bots\\youtubebot\\ony_music")

    print(file_dir_dict["video"])
    print(file_dir_dict["background"])

    request_body = make_youtube_n_desc_tags(file_dir_dict, video_id)
    
    upload_video(request_body, file_dir_dict)








