import json
import random
import requests
from math import *
from nonebot import on_command, CommandSession, permission
from nonebot import on_notice, NoticeSession


@on_command('chp', only_to_me=False)
async def chp(session: CommandSession):
    r = requests.get('https://chp.shadiao.app/api.php')
    await session.send(r.text)


@on_command('jisuan', aliases=['计算', 'suan', '算', 'js'], only_to_me=False)
async def jisuan(session: CommandSession):
    try:
        expression = session.current_arg_text.strip()
        if not expression:
            await session.pause("请输入你想计算的算术")
        expression = expression.replace('（', '(')
        expression = expression.replace('）', ')')
        count1 = count2 = 0
        for e in expression:
            if e == '(':
                count1 += 1
            elif e == ')':
                count2 += 1
        if not count1 == count2:
            await session.pause('啊哦，请补全你输入算术中的括号 >_<')
        result = expression + '=' + str(eval(expression))
        print(result)
        await session.send(result)
    except NameError:
        await session.send('这个算术题好难,人家算不出来呢 >_<')


@on_command('member_count', aliases=['总人数', '群人数'],
            permission=permission.GROUP_ADMIN, only_to_me=False)  # 只有管理员可以调用
async def get_member_count(session: CommandSession):
    group_id = session.ctx['group_id']
    try:
        member_list = await session.bot.get_group_member_list(group_id=group_id)
        await session.send(f"群人数：{len(member_list)}")
    except:
        await session.send("无法获取")
        return


@on_notice('group_increase')
async def _(session: NoticeSession):
    await session.send(f"[CQ:at,qq={session.ctx['user_id']}] 欢迎新朋友入群~~")


@on_command('sxcx', aliases=['sx'], only_to_me=False)
async def sxcx(session: CommandSession):
    arg = session.current_arg_text.strip()

    if not arg:
        await session.pause("请输入你想查询的缩写吧~")

    try:
        url = "https://lab.magiconch.com/api/nbnhhsh/guess"
        data = {"text": arg}

        r = requests.post(url, data=data)
        r.raise_for_status()
        name = json.loads(r.text)[0]['name']
        trans = json.loads(r.text)[0]['trans']
        if not trans:
            await session.send(f"未找到[{data['text']}]的释义，换个词试试吧 >_<")
        elif data['text'] == name:
            await session.send(f"[{name}]可能的含义为：\n{'，'.join(trans)}")
        else:
            await session.send(f"未找到[{data['text']}]的释义，已为您找到相近词[{name}]释义如下：\n"
                  f"{'，'.join(trans)}")
    except:
        await session.send('404 查询失败，换个关键词试试吧 >_<')


@on_command('ask', only_to_me=False)
async def ask(session: CommandSession):
    arg = session.current_arg_text.strip()

    if not arg:
        await session.pause('请输入你想要预测的问题,人家没有看到呢 *_*')
    if session.ctx['user_id'] == 296491216:
        reply = 'Yes'
    else:
        x = random.randint(0, 1)
        if x:
            reply = 'Yes'
        else:
            reply = 'No'
    await session.send(reply)