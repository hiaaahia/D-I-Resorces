import json
import xlwt
from datetime import datetime
from urllib import request
from urllib.parse import quote
import time
import os


# 获取数据
def get_data(pageindex, url_amap):
    global total_record
    time.sleep(0.5)
    url = url_amap.replace('pageindex', str(pageindex))
    html = ""
    url = quote(url, safe='/:?&=')
    
    with request.urlopen(url) as f:
        html = f.read()
        rr = json.loads(html)
        if total_record == 0:
            total_record = int(rr['count'])
        return rr['pois']


        


def getPOIdata(page_size, json_name, url_amap):
    global total_record
    print('获取POI数据开始')
    josn_data = get_data(1, url_amap)
    if (total_record % page_size) != 0:
        page_number = int(total_record / page_size) + 2
    else:
        page_number = int(total_record / page_size) + 1

    with open(json_name, 'w') as f:
        f.write(json.dumps(josn_data).rstrip(']'))
        for each_page in range(2, page_number):
            html = json.dumps(get_data(each_page, url_amap)).lstrip('[').rstrip(']')
            if html:
                html = "," + html
            f.write(html)
            print('已保存到json文件:' + json_name)
        f.write(']')
    print('获取POI数据结束')

# 写入数据到excel
def write_data_to_excel(json_name, hkeys, bkeys, name):
    today = datetime.today()
    today_date = datetime.date(today)

    # 从文件中读取数据
    fp = open(json_name, 'r')
    result = json.loads(fp.read())
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)

    # 创建表头
    for index, hkey in enumerate(hkeys):
        sheet.write(0, index, hkey)

    # 遍历result中的每个元素。
    for i in range(len(result)):
        values = result[i]
        n = i + 1
        for index, key in enumerate(bkeys):
            val = ""
            if key=='rating'or key=='lowest_price':
                print(key)
                biz_val=values['biz_ext']
                for biz_key in enumerate(biz_val):
                    stest=str(biz_key[1])
                    if stest==key:
                        val=biz_val[biz_key[1]]
                    
            else:
                val = values[key]
            sheet.write(n, index, val)
    wbk.save(name + str(today_date) + '.xls')
    print('保存到excel文件: ' +name + str(today_date) + '.xls!')


if __name__ == '__main__':
    url_amap = 'http://restapi.amap.com/v3/place/text?key=a9b19369ff438e1e1e4ccf412a6987d8&keywords=酒店&city=南京&citylimit=true&children=1&offset=20&page=1&extensions=all'
    page_size = 25      
    page_index = r'page=1'  # 显示页码
    global total_record
    total_record = 0
       # Excel表头
    hkeys = ['id', '行业类型', '名称', '类型', '地址', '联系电话', 'location',  '城市名称', '区域名称',
                '所在商圈','评分','最低价格']
       # 获取数据列
    bkeys = ['id', 'biz_type', 'name', 'type', 'address', 'tel', 'location', 'cityname', 'adname', 'business_area','rating','lowest_price']
      
    getPOIdata(page_size, json_name, url_amap)
    write_data_to_excel(json_name, hkeys, bkeys, "data_index\\南京酒店-高德地图")
   
