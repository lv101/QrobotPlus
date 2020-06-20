import re
import bs4
import time
import requests
from bs4 import BeautifulSoup
from nonebot import on_command, CommandSession
from concurrent.futures import ThreadPoolExecutor

pool =ThreadPoolExecutor(1)
resources = []

@on_command('lsj', only_to_me=False)
async def lsj(session: CommandSession):
    global ending, resources

    arg = session.current_arg_text.strip()

    if not arg:
        await session.pause('请输入你想要查找的资源名~')
    await session.send("正在搜索资源,请稍候...")
    await main(arg)

    if not resources and ending:
        await session.send("啊哦,人家没有找到你想要的资源哦,换个关键词试试吧~")
        resources = []
    elif ending:
        result = ''.join(resources)
        print(result, type(result))
        await session.send(result)
        print('发送成功')
        resources = []


def getHtmltext(find_url, headers):
    '''
    url解析器
    :param find_url: 要查找的url
    :param headers:
    :return: 若response状态码为200,返回网页原代码
    '''
    try:
        r = requests.get(find_url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html = r.text
        return html
    except:
        return ''

def print_resource(name):
    '''
    打印输出结果
    :param name: 深度解析并核实链接有效性后的信息字典
    :param count_ch: 用于格式化输出结果
    :param start: 计时开始时间,用于计算代码运行时间
    :return: None
    '''
    global count, ending, resources
    count += 1
    print('搜索成功')
    msg = f"{count}  {name['文件名'][:20]+'...'}\n类别：{name['类别']}\n文件大小：{name['文件大小']}\n文件格式：{name['文件格式']}\nurl：{name['资源链接']}\n"
    if not ending:
        resources.append(msg)

def check(filename, fileurl):
    try:
        judge = 1
        dict_name = {}
        list_1 = filename.split('，')
        for j in range(len(list_1)):
            list_2 = list_1[j].split('：')
            if len(list_2) == 2:
                dict_name[list_2[0]] = list_2[1]
        try:
            for ch in "《》【】. []：——":
                dict_name['文件名'] = dict_name['文件名'].replace(ch, '')
            for ch in ' ':
                dict_name['类别'] = dict_name['类别'].replace(ch, '')
                dict_name['文件格式'] = dict_name['文件格式'].replace(ch, '')
            if dict_name['文件大小'].split()[1] in ['kb', 'Kb', 'KB', 'kB'] \
                    and eval(dict_name['文件大小'].split()[0]) <= 5:
                judge = 0
            if dict_name['文件格式'] in ['.txt', '.doc', '.docx', '.exe']:
                judge = 0
            dict_name['资源链接'] = fileurl
            if judge:
                print_resource(dict_name)
            else:
                return ''
        except:
            return ''
    except:
        return ''

def parserHtml_1(html, url, headers):
    global ending
    try:
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup('div', attrs={'class': 'pss'})
        try:
            for tag in tags:
                if ending:
                    break
                file_url = url + tag.a.attrs['href']
                file_name = tag.div.text
                html_1 = getHtmltext(file_url, headers)
                soup_2 = BeautifulSoup(html_1, 'html.parser')
                tags = soup_2('a', attrs={'rel': 'noreferrer external nofollow'})
                try:
                    for tag in tags:
                        if ending:
                            break
                        detail_url = tag.attrs['href']
                        html_2 = getHtmltext(detail_url, headers)
                    result = re.findall(r'<div class="platform-tips" node-id="(.*?)"', html_2, re.M)
                    if result == ['web-cancelleddoc']:
                        continue
                    else:
                        check(file_name, detail_url)
                except:
                    return ''
        except:
            return ''
    except:
        return ''

def parserHtml_2(html, headers):
    global ending
    try:
        soup = BeautifulSoup(html, "html.parser")
        tags_1 = soup('span', attrs={'class': 'red'})
        for tag_1 in tags_1:
            if ending:
                break
            download = {}
            mid_url = tag_1.parent.attrs['href']
            html = getHtmltext(mid_url, headers)
            soup_2 = BeautifulSoup(html, "html.parser")
            try:
                for tags_2 in soup_2.find('div', attrs={'class': 'attachlist'}).children:
                    if ending:
                        break
                    if isinstance(tags_2, bs4.element.Tag):
                        tag_2 = tags_2('a', attrs={'class': 'ajaxdialog'})
                        for a in tag_2:
                            if ending:
                                break
                            down_u = a.attrs['href'].replace('dialog', 'download')
                            down_n = a.text
                            download['文件名'] = down_n
                            download['类别'] = 'BT种子'
                            download['文件格式'] = '.torrent'
                            download['资源链接'] = down_u
                            tag_3 = tags_2('td', attrs={'class': 'grey'})
                            for td in tag_3:
                                if '.' in td.text:
                                    download['文件大小'] = td.text.replace(' ', '')
                            for ch in "《》【】. []：——":
                                download['文件名'] = download['文件名'].replace(ch, '')
                            print_resource(download)
            except:
                continue
    except:
        return ''

def fun_1(depth, url, headers, find_name):
    global ending
    try:
        for i in range(depth):
            index = i + 1
            find_url = url + '/zh/' + find_name + f'/pn{index}.html'
            html = getHtmltext(find_url, headers)
            parserHtml_1(html, url, headers)
            if ending:
                break
    except:
        print("查找失败,请重试.")

def fun_2(depth, url_1, url_2, headers, find_name, page):
    global count, judge_, ending

    try:
        print("正在搜索资源,请稍候...")
        for i in range(page):
            find_url = url_2 + find_name +f'-page-{page}.htm'
            html = getHtmltext(find_url, headers)
            parserHtml_2(html, headers)
            if ending:
                break
        if count >= 6:
            judge_ = 0
        else:
            judge_ = 1
            fun_1(depth, url_1, headers, find_name)
    except:
        if judge_ == 1:
            fun_1(depth, url_1, headers, find_name)

def judge_outtime(start):
    global resources, ending
    ending = 0
    while True:
        if count > 6 or (time.perf_counter() - start) > 30:
            ending = 1
            if not resources:
                print('查询失败')
                return
            break

async def main(find_name):
    url_1 = "http://www.pansoso.org"
    url_2 = "http://www.2btjia.com/search-index-keyword-"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        "Cookie": "UM_distinctid=1714d9b495d425-056118bde2e097-c343162-100200-1714d9b495e99c; pss=0; CNZZDATA1278636714=369591025-1586141514-https%253A%252F%252Fcn.bing.com%252F%7C1586163136"}

    depth = 2
    global count
    global judge_
    global resources
    count = 0
    judge_ = 1
    page = 1
    print('开始搜索')

    start = time.perf_counter()
    pool.submit(judge_outtime, start)
    fun_2(depth, url_1, url_2, headers, find_name, page)
    print('搜索结束')