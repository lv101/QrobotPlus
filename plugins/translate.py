import re
import requests
from nonebot import on_command, CommandSession

command = ['翻译', 'translate', 'fy']


@on_command('fanyi', aliases=command, only_to_me=False)
async def fanyi(session: CommandSession):
    arg = session.current_arg_text.strip()

    if not arg:
        await session.pause('人家没有看到要翻译的内容呢,再试一次吧 >-<')

    paylod = {'doctype': 'json',
              'type': 'AUTO',
              'i': arg}
    url = 'http://fanyi.youdao.com/translate'
    r = requests.get(url, params=paylod)
    type_ = re.findall(r'"type":(.*?),', r.text)[0]
    error = re.findall(r'"errorCode":(.*?),', r.text)[0]
    text = re.findall(r'"tgt":"(.*?)"', r.text)[0]
    if eval(type_) == "UNSUPPORTED":
        await session.send("这个词好深奥,人家不会呢,换个词试试吧 >_<")
    else:
        if session.ctx['message_type'] == 'group':
            text = f"[CQ:at, qq={session.ctx['user_id']}] " + text
        await session.send(text)