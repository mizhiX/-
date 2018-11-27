import json

from lxml import etree
import requests

from 草稿.课堂.random_user_agent import user_agent


def get_page(url, headers):
    html = requests.get(url, headers=headers)
    if html.status_code == 200:
        return html.text
    return None


def parse_page(html):
    response = etree.HTML(html)
    div_list = response.xpath('//div[@class="channel-item"]')
    # print(len(div_list))
    result_list = []
    for div in div_list:
        # 标题
        title = div.xpath('./div[@class="bd"]/h3/a/text()')[0]
        # 链接
        link = div.xpath('./div[@class="bd"]/h3/a/@href')[0]
        # 喜欢
        like = ''.join(div.xpath('.//div[@class="likes"]/text()'))
        # 小组
        team = div.xpath('.//span[@class="from"]/a/text()')[0]
        # 时间
        time = div.xpath('.//span[@class="pubtime"]/text()')[0]
        result_dict = {}
        result_dict['title'] = title
        result_dict['link'] = link
        result_dict['like'] = like
        result_dict['team'] = team
        result_dict['time'] = time
        result_list.append(result_dict)
    return result_list


def with_file(result_list):
    json_text = json.dumps(result_list, ensure_ascii=False)
    with open('douban.json', 'a', encoding='utf8') as f:
        f.write(json_text)


def main():
    result_list = []
    for i in range(0, 303):
        page = i * 30
        url = 'https://www.douban.com/group/explore?start={}'.format(page)
        headers = {
            'User-Agent': user_agent()
        }
        print('正在爬取第%s页' % (i + 1))
        html = get_page(url, headers)
        print('正在解析第%s页' % (i + 1))
        result_list += parse_page(html)
        print('正在保存第%s页' % (i + 1))
        with_file(result_list)


if __name__ == '__main__':
    main()
