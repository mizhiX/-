import time
from io import BytesIO
from PIL import Image
import requests


def get_page(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp
    return None


def get_small_img(save_big_img, i):
    x1 = 0
    x2 = 76
    for n in range(4):
        save_small_img = save_big_img.crop((x1, 0, x2, 76))
        small_img = './small_img/%d_%d.png' % (i + 1, n + 1)
        save_small_img.save(small_img)
        x1 += 76
        x2 += 76


def main():
    for i in range(400):
        print('第%d个' % (i + 1))
        url = 'http://www.1kkk.com/vipindex/image3.ashx'
        try:
            save_big_img = get_page(url)
        except:
            print('链接失败!')
            time.sleep(2)
            continue
        # 保存图片
        save_big_img = Image.open(BytesIO(save_big_img.content))
        name = 'big_img.png'
        save_big_img.save(name)

        # 切割小图片
        get_small_img(save_big_img, i)


if __name__ == '__main__':
    main()
