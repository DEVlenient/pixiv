import requests
import random

word = input("請輸入名稱(標籤)：")

referer_list = []  # 儲存所有找到的 referer

for random_page in range(1, 101):
    params = {
        'word': word,
        'order': 'date_d',
        'mode': 'all',
        'p': random_page,
        's_mode': 's_tag_full',
        'type': 'illust_and_ugoira',
        'lang': 'zh_tw'
    }

    # 添加自定義標頭
    headers = {
        'user-agent': 'user-agent',
        'cookie': 'cookie'
    }

    response = requests.get('https://www.pixiv.net/ajax/search/illustrations/' + params['word'] + '?', params=params, headers=headers)
    data = response.json()

    num_illusts = len(data["body"]["illust"]["data"])

    if num_illusts > 0:
        for illust in data["body"]["illust"]["data"]:
            illust_data = illust["id"]
            referer = "https://www.pixiv.net/artworks/" + illust_data
            referer_list.append(referer)

if referer_list:
    random_referer = random.choice(referer_list)
    print(f"隨機選擇的 referer：{random_referer}")
else:
    print("未找到符合條件的插畫作品。")