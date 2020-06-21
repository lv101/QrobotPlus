import requests
from nonebot import on_command, CommandSession

command = ['翻译', 'translate', 'fy']


@on_command('fanyi', aliases=command, only_to_me=False)
async def fanyi(session: CommandSession):
    arg = session.current_arg_text
    print(arg)

    at = ''
    if session.ctx['message_type'] == 'group':
        at = f"[CQ:at,qq={session.ctx['user_id']}] "

    if not arg:
        await session.pause(at+'请输入你想要翻译的内容 >-<')

    paylod = {'doctype': 'json',
              'type': 'AUTO',
              'i': arg}
    url = 'http://fanyi.youdao.com/translate'
    data = requests.get(url, params=paylod).json()

    # print(r.url)
    type_ = data["type"]
    error = data["errorCode"]
    results = data["translateResult"]
    if type_ == "UNSUPPORTED":
        await session.send(at+"这个词好深奥,人家不会呢,换个词试试吧 >_<")
    else:
        trans = []
        for result in results:
            text = result[0]["tgt"]
            if text:
                trans.append(text)
        result_info = '\n'.join(trans)
        await session.send(result_info)