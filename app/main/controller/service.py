import json
from app.main.config import Config
from flask import Blueprint, render_template
import random
from app.main import cache
import os
from dotenv import load_dotenv
from flask import request, jsonify
import os
import requests
import pygeoip
import random
import geoip2.database as geoip
load_dotenv()

main = Blueprint('main', __name__)

path = os.getcwd() + "//gioipDatabase//GeoLite2-Country.mmdb"


@main.route('/')
def index():
    temp = request.remote_addr
    jj = request.headers
    # man = gi.country_name_by_addr('106.210.129.209')
    response = requests.get(
        "http://ip-api.com/json/{}".format('106.210.129.209'))
    js = response.json()
    reader = geoip.Reader(path)
    try:
        country = reader.country(temp)
    except Exception as e:
        country = " the error constyr"
        return(country)
        print("indiad")
    # print(man)
    name = country.country.names['en']
    value = f'ma strigngng  {temp}'

    l = ['india', 'us']
    random.shuffle(l)
    print(l[-1])
    print(type(country))
    # print(jsonify(country))
    val = country.country
    # print(jsonify(val))
    val = country.country.names['en']

    # value = GenerateTemplate(l[-1])
    # print(value)
    return val + "     the location whixh user come"


# @cache.cached(timeout=int(os.getenv("CACHE_TIME")), key_prefix="generateTemplate")
@cache.memoize(timeout=100)
def GenerateTemplate(name):
    return name
    bucket_obj = Config.bucket
    filename = [filename.name for filename in list(
        bucket_obj.list_blobs(prefix=''))]

    try:
        layout_folder_name = os.getenv('LAYOUT_FOLDER_NAME')+'/'
        blog = bucket_obj.list_blobs(
            prefix=f'{layout_folder_name}', delimiter='/')
    except Exception as e:
        print("connection not Build with gcp", e)
        return "Refrash"
    layouts = []
    used_layout = []
    print("Getting Blog")
    for blob in blog:
        print(blob.name)

    TOTAL_LAYOUT = 0
    lenth_of_each_layout = []

    for prefix in blog.prefixes:
        layouts.append(
            [filename.name for filename in list(
                bucket_obj.list_blobs(prefix=f'{prefix}'))]
        )

    print("get html template name")
    TOTAL_LAYOUT = len(layouts)
    for layout in layouts:
        lenth_of_each_layout.append(len(layout))
        used_layout.append([])

    if cache.get("CACHE_LAYOUT_data") is None:
        cache.set("CACHE_LAYOUT_data", used_layout)

    used_layout = cache.get("CACHE_LAYOUT_data")
    index = 0
    for layout in layouts:
        layout_list_number = list(range(0, len(layout)))
        random.shuffle(layout_list_number)
        for i in range(1, len(layout)):
            # randomnumber = random.randint(1, len(layout)-1)
            choosed = layout[layout_list_number[-1]]
            if choosed not in used_layout[index]:
                used_layout[index].append(choosed)
                index = index+1
                break
            if not len(layout_list_number) == 1:
                layout_list_number.pop()
            else:
                pass
        else:
            index = index+1
            print(
                f"max limit of laypout {index} reached, rendering last layout ")
    cache.set("CACHE_LAYOUT_data", used_layout)
    templats = []
    print("start to Download Html layout")
    try:
        for i in range(TOTAL_LAYOUT):
            layout = bucket_obj.blob(
                blob_name=f"{used_layout[i][-1]}").download_as_string()
            templats.append(layout)

        random.shuffle(templats)
        start = bucket_obj.blob(
            blob_name='start.html').download_as_string()
    except Exception as e:
        print("error while geting tmplate")
        return "Refresh"
    end = bytes("</body>\r\n\r\n</html>", 'utf-8')
    print("download complate")
    retval = start
    for templats_string in templats:
        retval = retval+templats_string
    retval = retval + end
    return retval
