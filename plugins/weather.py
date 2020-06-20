'''
程序功能函数,查询当日天气预报
'''
import json
import re
import time
import requests
from nonebot import on_command, CommandSession, permission


@on_command('tianqi', aliases=['天气', '查天气', '天气预报', 'tq'], only_to_me=False)
async def tianqi(session: CommandSession):
    city = session.get('city', prompt="你想查询哪个城市的天气呢？")
    weather_report = get_weather(city)
    if session.ctx['message_type'] == 'group':
        weather_report = f"[CQ:at, qq={session.ctx['user_id']}]\n"+weather_report

    await session.send(weather_report)


@tianqi.args_parser
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
        citys = json.loads(f.read())
    city = None
    for city_ in citys:
        if re.findall(city_['cityZh'], arg):
            city = city_['cityZh']
            print(city)
            break
    if not city:
        time.sleep(3)
        return "啊哦，没有查到该地的信息，换个城市试试吧 >_<"

    paylod = {
        'version': 'v6',
        'appid': ,
        'appsecret': '',
        'city': city
    }

    url = 'https://tianqiapi.com/api'
    r = requests.get(url, params=paylod).content.decode('unicode-escape').replace('<\/em><em>', '')
    data = json.loads(r)

    return f"{data['country']}{data['city']}\n更新时间：{data['update_time']}\n" \
        f"天气情况：{data['wea']}\n实时温度：{data['tem']}\n气压：{data['pressure']}hPa\n" \
        f"空气质量：{data['air']}\n"f"空气质量等级：{data['air_level']}\n{data['air_tips']}"
