import os
import requests

word = input("請輸入名稱(標籤)：")
start_page = int(input("請輸入起始頁數："))
end_page = int(input("請輸入結束頁數："))
custom_path = input("是否要自訂儲存路徑？(輸入 '是' 或 '否')：")

if custom_path == "是":
    download_folder = input("請輸入自訂儲存路徑：")
else:
    download_folder = input("請輸入自訂資料夾名稱：")
    desktop_path = os.path.expanduser('~/desktop')
    download_folder = os.path.join(desktop_path, download_folder)

# 確保資料夾存在，如果不存在則創建資料夾
os.makedirs(download_folder, exist_ok=True)

for page_num in range(start_page, end_page + 1):
    params = {
        'word'   : word,
        'order'  : 'date_d',
        'mode'   : 'all',
        'p'      : page_num,
        's_mode' : 's_tag_full',
        'type'   : 'illust_and_ugoira',
        'lang'   : 'zh_tw'
    }

    response = requests.get('https://www.pixiv.net/ajax/search/illustrations/' + params['word'] + '?', params = params)
    data = response.json()

    num_illusts = len(data["body"]["illust"]["data"])

    for i, illust in enumerate(data["body"]["illust"]["data"]):
        illust_data = illust["id"]
        referer = "https://www.pixiv.net/artworks/" + illust_data
        print(f"第 {page_num} 頁_{i+1}：{referer}")

        # 獲取 referer
        referer = referer

        # 構造獲取 JSON 數據的 URL
        json_url = referer.replace("artworks", "ajax/illust") + "/pages?lang=zh_tw&version=f32089e9d176912e655d9eda2c1b816e46a82d4b"

        # 添加自定義標頭
        headers = {
            'user-agent': 'user-agent',
            'referer': referer,
            'cookie': 'cookie'
        }

        # 發送請求獲取 JSON 數據
        response = requests.get(json_url, headers=headers).json()

        # 檢查是否成功取得 JSON 資料
        pages = response["body"]
        for index, page in enumerate(pages):
            download_url = page["urls"]["original"]
            image_name = download_url.split("/")[-1].split(".")[0]  # 提取圖片名稱
            image_response = requests.get(download_url, headers=headers)
            if image_response.status_code == 200:
                image_data = image_response.content
                image_extension = os.path.splitext(download_url)[-1]  # 提取圖片擴展名
                image_filename = f"{image_name}{image_extension}"
                image_path = os.path.join(download_folder, image_filename)
                with open(image_path, "wb") as image_file:
                    image_file.write(image_data)
                print(f"{image_filename} 下載成功。")
            else:
                print(f"無法下載圖片 {image_name}。狀態碼: {image_response.status_code}")