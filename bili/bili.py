import time

import requests
from fake_useragent import UserAgent

ua = UserAgent()


# https://vc.bilibili.com/p/eden/rank#/?tab=%E5%85%A8%E9%83%A8
# XHR 找到top?page_size 接口


def get_url(page):
    url = 'http://api.vc.bilibili.com/board/v1/ranking/top?page_size=10&next_offset=&tag=%E4%BB%8A%E6%97%A5%E7%83%AD%E9%97%A8&platform=pc'.format(
        page)

    response = requests.get(url).json()  # 响应内容转成json

    items = response.get('data').get('items')

    for i in items:
        ite = i.get('item')
        video_name = ite.get('description')
        release_time = ite.get('upload_time')
        video_url = ite.get('video_playurl')
        video_user = i.get('user').get('name')
        # print(video_user)
        try:
            download_video(video_url, '{}.mp4'.format(video_name))
        except Exception as e:
            print(e.args)


def download_video(url, path):
    '''视频是数据流，源源不断'''
    start = time.time()
    headers = {
        'User-Agent': ua.random
    }
    # stream=True 视频流下载
    response = requests.get(url, headers=headers, stream=True)

    chunk_size = 1024  # 每次下载的大小
    content_size = int(response.headers['content-length'])  # 数据的总大小
    size = 0  # 已下载的大小

    if response.status_code == 200:
        print('[文件大小:{}MB]'.format(content_size / chunk_size / 1024))

        with open(path, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                size += len(data)
                print('[下载进度:{}{}%'.format('>' * int(size * 50 / content_size), float(size / content_size * 100),
                                           end=']'))
    end = time.time()
    print('used time={}'.format(end - start))


for i in range(100):
    i = i * 10 + 1
    get_url(i)
