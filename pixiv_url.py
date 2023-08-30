import os
import requests

# 判斷下載單個作品還是多個作品
choice = input("要下載單一作品還是多個作品？(輸入 '單一' 或 '多個')：")

if choice == "單一":
    referer = input("請輸入作品網址：")

    # 構造獲取 JSON 數據的 URL
    json_url = referer.replace("artworks", "ajax/illust") + "/pages?lang=zh_tw&version=f32089e9d176912e655d9eda2c1b816e46a82d4b"

    # 添加自定義標頭
    headers = {
        'user-agent': 'user-agent',
        'cookie': 'cookie'
    }

    custom_path = input("是否要自訂儲存路徑？(輸入 '是' 或 '否')：")
    if custom_path == "是":
        download_folder = input("請輸入儲存路徑：")
    else:
        download_folder = input("請輸入資料夾名稱：")
        desktop_path = os.path.expanduser('~/desktop')
        download_folder = os.path.join(desktop_path, download_folder)

    os.makedirs(download_folder, exist_ok=True)

    response = requests.get(json_url, headers=headers).json()

    pages = response["body"]
    for index, page in enumerate(pages):
        download_url = page["urls"]["original"]
        image_name = download_url.split("/")[-1].split(".")[0]
        image_response = requests.get(download_url, headers=headers)
        if image_response.status_code == 200:
            image_data = image_response.content
            image_extension = os.path.splitext(download_url)[-1]
            image_filename = f"{image_name}{image_extension}"
            image_path = os.path.join(download_folder, image_filename)
            with open(image_path, "wb") as image_file:
                image_file.write(image_data)
            print(f"{image_filename} 下載成功。")
        else:
            print(f"無法下載圖片 {image_name}。狀態碼: {image_response.status_code}")

elif choice == "多個":
    num_works = int(input("請輸入要下載的作品數量："))
    
    works_info = []

    for i in range(num_works):
        referer = input(f"請輸入第 {i+1} 個作品的網址：")
        works_info.append(referer)

    same_path = input("是否要所有作品都儲存於相同路徑？(輸入 '是' 或 '否')：")
    if same_path == "是":
        custom_path = input("請輸入儲存路徑：")
    else:
        custom_path = "否"

    for i, referer in enumerate(works_info):
        print("=" * 50)
        print(f"處理第 {i+1} 個作品：")
        # 構造獲取 JSON 數據的URL
        json_url = referer.replace("artworks", "ajax/illust") + "/pages?lang=zh_tw&version=f32089e9d176912e655d9eda2c1b816e46a82d4b"

        # 添加自定義標頭
        headers = {
            'user-agent': 'user-agent',
            'cookie': 'cookie'
        }

        if custom_path == "否":
            download_folder = input("請輸入資料夾名稱：")
            desktop_path = os.path.expanduser('~/desktop')
            download_folder = os.path.join(desktop_path, download_folder)
        else:
            download_folder = custom_path

        os.makedirs(download_folder, exist_ok=True)

        response = requests.get(json_url, headers=headers).json()

        pages = response["body"]
        for index, page in enumerate(pages):
            download_url = page["urls"]["original"]
            image_name = download_url.split("/")[-1].split(".")[0]
            image_response = requests.get(download_url, headers=headers)
            if image_response.status_code == 200:
                image_data = image_response.content
                image_extension = os.path.splitext(download_url)[-1]
                image_filename = f"{image_name}{image_extension}"
                image_path = os.path.join(download_folder, image_filename)
                with open(image_path, "wb") as image_file:
                    image_file.write(image_data)
                print(f"{image_filename} 下載成功。")
            else:
                print(f"無法下載圖片 {image_name}。狀態碼: {image_response.status_code}")
else:
    print("輸入無效選擇。")