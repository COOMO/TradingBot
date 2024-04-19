import requests

url = 'https://notify-api.line.me/api/notify'
token = 'Your Line Notify Token'
headers = {
    'Authorization': 'Bearer ' + token    # 設定權杖
}

# 送訊息
data = {
    'message':'Test Message'     # 設定要發送的訊息
}
data = requests.post(url, headers=headers, data=data)   # 使用 POST 方法

# 送貼圖
data = {
    'message':'send sticker',
    'stickerPackageId':'446',
    'stickerId':'1989'
}
data = requests.post(url, headers=headers, data=data)

# 送圖片
data = {
    'message':'send image URL',
    'imageThumbnail':'https://example.com/original.jpg',
    'imageFullsize':'https://example.com/preview.jpg'
}
data = requests.post(url, headers=headers, data=data)

# send local image
data = {
    'message':'send local image',
}
image = open('test code/20240409_005150.jpg', 'rb')
files = { 'imageFile': image }
data = requests.post(url, headers=headers, data=data, files=files)