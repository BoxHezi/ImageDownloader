from bs4 import BeautifulSoup
import urllib.request
import re
import os
import json

keyword = input("Enter the keyword of images: ")
# dl_amount = input("Enter the amount of images you want to download: ")

query = re.sub("\s+", "+", keyword.strip())

# header to prevent 403
header = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 "
                  "Safari/537.36"}

url = "https://www.google.com/search?q=" + query + "&newwindow=1&tbm=isch"

soup_url = urllib.request.urlopen(urllib.request.Request(url, headers=header))
soup = BeautifulSoup(soup_url, "html.parser")

# declare an array for images
image_array = []

for image in soup.find_all("div", {"class": "rg_meta"}):
    image_link, image_type = json.loads(image.text)["ou"], json.loads(image.text)["ity"]
    image_array.append((image_link, image_type))

print("Total of " + str(len(image_array)) + " images found!")

# root directory of the project
root_dir = "images"

if not os.path.exists(root_dir):
    os.mkdir(root_dir)

# directory for the current query
query_dir = os.path.join(root_dir, keyword)

if not os.path.exists(query_dir):
    os.mkdir(query_dir)

for i, (image_link, image_type) in enumerate(image_array):
    try:
        request_url = urllib.request.Request(image_link, headers=header)
        raw_image = urllib.request.urlopen(request_url).read()

        # display current download
        print("\nDownloading " + image_type + " " + str(i + 1))
        print(image_link)

        # download images
        if image_type == "":
            image_type = "jpg"

        file = open(os.path.join(query_dir, query + " (" + str(i + 1)) + ")." + image_type, "wb")
        file.write(raw_image)
        file.close()

    # catch exception
    except Exception as e:
        print(e)

print("Done\n")
