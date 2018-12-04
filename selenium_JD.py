import time
import requests
from lxml import etree
import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome配置
chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.set_window_size(1400, 700)
wait = WebDriverWait(browser, 5)

# MySQL链接
db = pymysql.connect(host='localhost', user='root', password='yao120', port=3306, db='jd_pinghengche')
cursor = db.cursor()


def get_page(page):
    if page == 1:
        url = 'https://www.jd.com'
        browser.get(url)
        # 输入搜索名称
        input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="key"]')))
        input.send_keys('帽子')
        # 点击搜索按钮
        button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="form"]/button')))
        button.click()
        time.sleep(3)


    else:
        # 填写页面编号
        input = wait.until(
            EC.presence_of_element_located((By.XPATH, '//a[@class="btn btn-default"]/..//input')))
        input.clear()
        input.send_keys(page)

        # 点击下一页
        button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="btn btn-default"]')))
        button.click()

    for i in range(16):
        str_js = 'var step = document.body.scrollHeight / 16; window.scrollTo(0, step * %d)' % (i + 1)
        browser.execute_script(str_js)
        time.sleep(1)
    return browser.page_source


def parse_page(html):
    html_etree = etree.HTML(html)
    li_list = html_etree.xpath('//li[@class="gl-item"]')
    goods_url_list = []
    for li in li_list:
        goods_url = li.xpath('.//div[@class="p-img"]/a/@href')[0]
        if goods_url[:5] != 'https':
            goods_url = 'https:' + goods_url
        goods_url_list.append(goods_url)
    return goods_url_list


def req_get_page(goods_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    html = requests.get(goods_url, headers=headers)
    if html.status_code == 200:
        return html.text
    return None


def parse_goods(html):
    html_etree = etree.HTML(html)
    # 品牌
    brand = html_etree.xpath('//ul[@id="parameter-brand"]/li/a/text()')[0]

    ul = html_etree.xpath('//ul[@class="parameter2 p-parameter-list"]')[0]
    # 商品名称
    try:
        goods_name = ul.xpath('./li[contains(text(), "商品名称")]/text()')[0][5:]
    except:
        goods_name = ''
    # 商品编号
    try:
        goods_number = ul.xpath('./li[contains(text(), "商品编号")]/text()')[0][5:]
    except:
        goods_number = ''
    # 店铺
    try:
        shop = ul.xpath('./li[contains(text(), "店铺")]/a/text()')[0]
    except:
        shop = ''
    # 商品毛重
    try:
        maozhong = ul.xpath('./li[contains(text(), "商品毛重")]/text()')[0][5:]
    except:
        maozhong = ''
    # 商品产地
    try:
        origin = ul.xpath('./li[contains(text(), "商品产地")]/text()')[0][5:]
    except:
        origin = ''
    # 货号
    try:
        huohao = ul.xpath('./li[contains(text(), "货号")]/text()')[0][3:]
    except:
        huohao = ''
    # 重量
    try:
        weight = ul.xpath('./li[contains(text(), "重量")]/text()')[0][3:]
    except:
        weight = ''
    # 理论时速
    try:
        speed = ul.xpath('./li[contains(text(), "理论时速")]/text()')[0][5:]
    except:
        speed = ''
    # 能否折叠
    try:
        fold = ul.xpath('./li[contains(text(), "能否折叠")]/text()')[0][5:]
    except:
        fold = ''
    # 额定功率
    try:
        edgl = ul.xpath('./li[contains(text(), "额定功率")]/text()')[0][5:]
    except:
        edgl = ''
    # 电池能否拆卸
    try:
        dcnfcx = ul.xpath('./li[contains(text(), "电池能否拆卸")]/text()')[0][7:]
    except:
        dcnfcx = ''
    # 电池类别
    try:
        cell_type = ul.xpath('./li[contains(text(), "电池类别")]/text()')[0][5:]
    except:
        cell_type = ''
    # 控制方式
    try:
        control = ul.xpath('./li[contains(text(), "控制方式")]/text()')[0][5:]
    except:
        control = ''
    # 理论续航
    try:
        life = ul.xpath('./li[contains(text(), "理论续航")]/text()')[0][5:]
    except:
        life = ''
    # 电池电压
    try:
        voltage = ul.xpath('./li[contains(text(), "电池电压")]/text()')[0][5:]
    except:
        voltage = ''
    # 适用人群
    try:
        apply_people = ul.xpath('./li[contains(text(), "适用人群")]/text()')[0][5:]
    except:
        apply_people = ''
    # 变速档位
    try:
        gear = ul.xpath('./li[contains(text(), "变速档位")]/text()')[0][5:]
    except:
        gear = ''
    # 标准认证
    try:
        bzrz = ul.xpath('./li[contains(text(), "标准认证")]/text()')[0][5:]
    except:
        bzrz = ''
    # 分类
    try:
        classify = ul.xpath('./li[contains(text(), "分类")]/text()')[0][3:]
    except:
        classify = ''
    # 款式
    try:
        style = ul.xpath('./li[contains(text(), "款式")]/text()')[0][3:]
    except:
        style = ''
    # 轮圈尺寸
    try:
        size = ul.xpath('./li[contains(text(), "轮圈尺寸")]/text()')[0][5:]
    except:
        size = ''

    # 将爬去的数据添加到字典中
    item_dict = {}
    item_dict['brand'] = brand
    item_dict['goods_name'] = goods_name
    item_dict['goods_number'] = goods_number
    item_dict['shop'] = shop
    item_dict['maozhong'] = maozhong
    item_dict['origin'] = origin
    item_dict['huohao'] = huohao
    item_dict['weight'] = weight
    item_dict['speed'] = speed
    item_dict['fold'] = fold
    item_dict['edgl'] = edgl
    item_dict['dcnfcx'] = dcnfcx
    item_dict['cell_type'] = cell_type
    item_dict['control'] = control
    item_dict['life'] = life
    item_dict['voltage'] = voltage
    item_dict['apply_people'] = apply_people
    item_dict['gear'] = gear
    item_dict['bzrz'] = bzrz
    item_dict['classify'] = classify
    item_dict['style'] = style
    item_dict['size'] = size
    return item_dict


def save_to_mysql(item):
    sql = "INSERT INTO goods (brand, goods_name, goods_number, shop, maozhong, origin, huohao, weight, speed, fold, " \
          "edgl, dcnfcx, cell_type, control, life, voltage, apply_people, gear, bzrz, classify, style, size) " \
          "values( " + ("'%s', " * 21) + "'%s')"
    sql = sql % (item['brand'], item['goods_name'], item['goods_number'], item['shop'], item['maozhong'], item['origin'], item['huohao'], item['weight'], item['speed'], item['fold'], item['edgl'], item['dcnfcx'], item['cell_type'], item['control'], item['life'], item['voltage'], item['apply_people'], item['gear'], item['bzrz'], item['classify'], item['style'], item['size'])
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print('数据添加失败!')


def main():
    for page in range(100):
        print('第%s页' % (page + 1))
        # selenium 爬取商品列页面
        html = get_page(page + 1)
        # 解析商品列页面 返回 每个商品的详细链接
        goods_url_list = parse_page(html)
        i = 1
        for goods_url in goods_url_list:
            print('第%s条数据' % i)
            # 爬取商品的详细页面
            html = req_get_page(goods_url)
            # 接卸商品详细页面 返回 字典
            item_dict = parse_goods(html)
            # 将爬取到的数据存入MySQL
            save_to_mysql(item_dict)
            i += 1
    # 关闭MySQL
    db.close()
    # 关闭Chrome浏览器
    browser.close()


if __name__ == '__main__':
    main()
