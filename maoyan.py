import requests
import re
import json


def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # return response.text  # text解析容易有乱码
        return response.content
    return None


def parse_page(html):
    # 电影名称
    movie_items = re.findall('<p class="name">.*?>(.*?)</a>', html, re.S)
    # print(movie_items)
    # 主演
    star_items = re.findall('<p class="star">(.*?)</p>', html, re.S)
    # print(star_items)
    # 上映时间
    time_items = re.findall('<p class="releasetime">(.*?)</p>', html, re.S)
    # print(time_items)
    # 排名
    top_items = re.findall('<i class="board-index board-index-\d+">(.*?)</i>', html, re.S)
    # print(top_items)
    # 分数
    score_items = re.findall('<p class="score"><i class="integer">(.*?)</i><i class="fraction">(.*?)</i>', html, re.S)
    # print(score_items)
    # print(''.join(score_item))
    # 图片
    image_items = re.findall('<img data-src="(.*?)".*?/>', html, re.S)
    # print(image_items)
    result_list = []
    for i in range(len(image_items)):
        result_dict = {}
        result_dict['movie'] = movie_items[i]
        result_dict['star'] = star_items[i].strip()
        result_dict['time'] = time_items[i]
        result_dict['top'] = top_items[i]
        # result_dict['score'] = score_items[i][0] + score_items[i][1]
        result_dict['score'] = ''.join(score_items[i])
        result_dict['image'] = image_items[i]
        result_list.append(result_dict)
    return result_list


def get_all_page(base_url):
    result_list = []
    for i in range(10):
        url = base_url.format(i * 10)
        html = get_page(url).decode('utf8')
        # items += parse_page(html)
        result_list.extend(parse_page(html))
    return result_list


def write_img(result_list):
    for item in result_list:
        img_url = item['image']
        url = img_url.split('@')[0]
        img_name = img_url.split('/')[-1].split('@')[0]
        print(img_name)
        content = get_page(url)
        with open('./image/%s' % img_name, 'wb') as f:
            f.write(content)


def save_json(result_list):
    json_text = json.dumps(result_list, ensure_ascii=False)
    with open('./maoyan.json', 'w', encoding='utf8') as f:
        f.write(json_text)


def main():
    base_url = 'http://maoyan.com/board/4?offset={}'
    result_list = get_all_page(base_url)
    # print(result_list)
    # 保存图片
    # write_img(result_list)
    # 保存json
    save_json(result_list)


if __name__ == '__main__':
    main()
