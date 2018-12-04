import json
from mongodb_help import *
import requests

url = 'http://www.u17.com/comic/ajax.php?mod=comic_list&act=comic_list_new_fun&a=get_comic_list'
headers = {
    'Host': 'www.u17.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Referer': 'http://www.u17.com/comic_list/th99_gr99_ca99_ss99_ob0_ac0_as0_wm0_co99_ct99_p1.html?order=2'
}


def get_page(page):
    post_data = {
        'data[group_id]': 'no',
        'data[theme_id]': 'no',
        'data[is_vip]': 'no',
        'data[accredit]': 'no',
        'data[color]': 'no',
        'data[comic_type]': 'no',
        'data[series_status]': 'no',
        'data[order]': '2',
        'data[page_num]': page,
        'data[read_mode]': 'no'
    }
    response = requests.post(url, post_data, headers=headers)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    return None


def parse_page(comic_list):
    for comic in comic_list:
        result_dict = {}
        result_dict['comic_id'] = comic.get('comic_id')
        result_dict['name'] = comic.get('name')
        result_dict['cover'] = comic.get('cover')
        result_dict['update_type'] = comic.get('update_type')
        result_dict['line1'] = comic.get('line1')
        result_dict['line2'] = comic.get('line2')
        # print(result_dict)
        # 插入到MongoDB数据库
        insert_company(result_dict)


def main():
    page = 1
    while 1:
        print('第%s页' % page)
        html = get_page(page)
        result_json = json.loads(html)
        comic_list = result_json['comic_list']
        print(len(comic_list))
        if len(comic_list) == 0:
            break
        parse_page(comic_list)
        page += 1


if __name__ == '__main__':
    main()
