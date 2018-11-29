import time
import random
import requests
import json
import pymysql
from 草稿.课堂.random_user_agent import user_agent


db = pymysql.connect(host='localhost', user='root', password='yao120', port=3306, db='mogujie_db')
cursor = db.cursor()


def get_page(url):
    headers = {
        'User-Agent': user_agent()
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content.decode('utf8')
    return None


def parse_page(html):
    i = html.index('(')
    html = html[i+1:]
    html = html[:-2]
    resutl_dict = json.loads(html)
    is_end = resutl_dict['result']['wall']['isEnd']
    if is_end:
        return None
    results = resutl_dict['result']['wall']['docs']
    resutl_list = []
    for item in results:
        result_dict = {}
        result_dict['tradeItemId'] = item.get('tradeItemId', '')
        result_dict['img'] = item.get('img', '')
        result_dict['itemType'] = item.get('itemType', '')
        result_dict['link'] = item.get('link', '')
        result_dict['itemMarks'] = item.get('itemMarks', '')
        result_dict['acm'] = item.get('acm', '')
        result_dict['title'] = item.get('title', '')
        result_dict['type'] = item.get('type', '')
        result_dict['orgPrice'] = item.get('orgPrice', '')
        result_dict['hasSimilarity'] = item.get('hasSimilarity', '')
        result_dict['cfav'] = item.get('cfav', '')
        result_dict['price'] = item.get('price', '')
        result_dict['similarityUrl'] = item.get('similarityUrl', '')
        resutl_list.append(result_dict)
    return resutl_list


def write_to_file(json_list):
    json_text = json.dumps(json_list, ensure_ascii=False)
    with open('mogujie.json', 'w', encoding='utf8') as f:
        f.write(json_text)


def save_mysql(result_list):
    for result in result_list:
        tradeitemid = result['tradeItemId']
        img = result['img']
        itemtype = result['itemType']
        link = result['link']
        itemmarks = result['itemMarks']
        acm = result['acm']
        title = result['title']
        type = result['type']
        orgprice = result['orgPrice']
        hassimilarity = result['hasSimilarity']
        cfav = result['cfav']
        price = result['price']
        similarityurl = result['similarityUrl']
        # 13
        sql = "INSERT INTO mogujie (tradeitemid, img, itemtype, link, itemmarks, acm, title, type, orgprice, hassimilarity, cfav, price, similarityurl) values(" + "'%s', " * 12 + "'%s')"
        cursor.execute(sql % (tradeitemid, img, itemtype, link, itemmarks, acm, title, type, orgprice, hassimilarity, cfav, price, similarityurl))
        db.commit()


def main():
    page = 1
    json_list = []
    while True:
        url = 'https://list.mogujie.com/search?callback=jQuery211035405599252635267_1543376645413&_version=8193&ratio=3%3A4&cKey=43&sort=pop&page={}'.format(page)
        html = get_page(url)
        if '(' not in html:
            print('页面拦截, 请稍等')
            t = random.randint(1, 2)
            time.sleep(t)
            continue
        result_list = parse_page(html)
        if result_list is None:
            print('完成!')
            result_list = []
            break
        json_list.append(result_list)
        print(page, len(result_list))
        page += 1
        save_mysql(result_list)
    # write_to_file(json_list)
    db.close()


if __name__ == '__main__':
    main()
