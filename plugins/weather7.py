'''
程序功能函数,查询未来七日天气预报
'''
import json
import random
import re
import time
import requests
from nonebot import on_command, CommandSession

command = ['tq7', '天气7', '天气七', '查天气7', '未来7日天气', '7天天气', '7日天气', '七天天气', '七日天气', '未来七日天气', '未来天气']

@on_command('tianqi7', aliases=command, only_to_me=False)
async def tianqi7(session: CommandSession):
    city = session.get('city', prompt="你想查询哪个城市的天气呢？")
    weather_reports = get_weather(city)
    for weather_report in weather_reports:
        time.sleep(1)
        await session.send(weather_report)


@tianqi7.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()  # 去除消息两侧的空白符

    if session.is_first_run:
        if stripped_arg:
            session.state['city'] = stripped_arg
        return

    if not stripped_arg:
        await session.pause("要查询的城市不能为空哦，请输入有效的城市名称")

    session.state[session.current_key] = stripped_arg
    print(stripped_arg)


def get_weather(arg):
    with open('city.json', 'r', encoding='unicode-escape') as f:
        datas = json.loads(f.read())
    city = None
    for data in datas:
        if re.findall(data['cityZh'], arg):
            city = data['cityZh']
            print(city)

    if not city:
        time.sleep(3)
        return "啊哦,没有查到该地的信息,换个城市试试吧 >_<"

    paylod = {
              'version': 'v1',
              'appid': ,
              'appsecret': '',
              'city': city
                  }

    url = 'https://tianqiapi.com/api'
    r = requests.get(url, params=paylod).content.decode('unicode-escape').replace('<\/em><em>', '')

    text = json.loads(r)
    weather_list = []

    for data in text['data']:
        desc_list = []
        for x in data['index']:
            desc_list.append(x['desc'])
        desc = desc_list[random.randint(0, len(desc_list) - 1)]
        weather_list.append(f"{text['country']}{text['city']}\n"f"更新时间：{text['update_time']}\n"
               f"{data['day']}\n"f"天气情况：{data['wea']}\n平均温度：{data['tem']}\n{desc}")
    return weather_list
