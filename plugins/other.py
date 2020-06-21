import json
import random
import re
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
        if re.match(r"^\d*$", expression):
            print(1)
            Dec = eval(expression)
            Bin = bin(Dec)
            Oct = oct(Dec)
            Hex = hex(Dec)
            await session.send(f"进制转换\n"
                               f"二进制：{Bin}\n"
                               f"八进制：{Oct}\n"
                               f"十进制：{Dec}\n"
                               f"十六进制：{Hex}")
        else:
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
            permission=permission.GROUP_ADMIN | permission.SUPERUSER, only_to_me=False)  # 只有管理员可以调用
async def get_member_count(session: CommandSession):
    group_id = session.ctx['group_id']
    try:
        member_list = await session.bot.get_group_member_list(group_id=group_id)
        await session.send(f"群人数：{len(member_list)}")
    except:
        await session.send("无法获取")
        return


@on_command('send_like', aliases=['赞'])
async def zan(session: CommandSession):
    await session.bot.send_like(user_id=session.ctx.user_id, times=10)
    await session.send("好友赞 成功")


@on_command('禁言', aliases=['ban'], permission=permission.GROUP_MEMBER | permission.GROUP_OWNER |
            permission.GROUP_ADMIN | permission.SUPERUSER, only_to_me=False)
async def ban_member(session: CommandSession):
    group_id = session.ctx.group_id
    user_id = session.ctx.user_id
    if session.current_arg_text == 'all':
        judge = await judge_permission(session, ban_id='0', user_id=user_id)
        if not judge:
            return ''
        print(group_id)
        await session.bot.set_group_whole_ban(group_id=group_id, enable=True)
        await session.send(f"[CQ:at,qq={user_id}] 已开启 全员禁言")
        print("全员禁言成功")
        return ''
    try:
        ban_id = re.findall(r"\[CQ:at,qq=(.*?)\]", session.ctx.raw_message)[0]
    except IndexError:
        await session.send("艾特一下你要禁言的用户吧 >_<")
        return ''
    judge = await judge_permission(session, ban_id, user_id)
    if not judge:
        return ''
    try:
        await session.bot.set_group_ban(group_id=group_id, user_id=ban_id,
                                        duration=60*random.randint(1, 10))
        await session.send(f"[CQ:at,qq={user_id}] 已禁言")
        print("禁言成功")
    except:
        await session.send(f"[CQ:at,qq={user_id}] 404 禁言失败 >_<")
        print("404 禁言失败")


@on_command('解除禁言', aliases=['free'], permission=permission.GROUP_MEMBER | permission.GROUP_OWNER |
            permission.GROUP_ADMIN | permission.SUPERUSER, only_to_me=False)
async def ban_member(session: CommandSession):
    group_id = session.ctx.group_id
    user_id = session.ctx.user_id
    if session.current_arg_text == 'all':
        judge = await judge_permission(session, ban_id='0', user_id=user_id)
        if not judge:
            return ''
        await session.bot.set_group_whole_ban(group_id=group_id, enable=False)
        await session.send(f"[CQ:at,qq={user_id}] 已解除 全员禁言")
        print("解除 全员禁言 成功")
        return ''
    try:
        ban_id = re.findall(r"\[CQ:at,qq=(.*?)\]", session.ctx.raw_message)[0]
    except IndexError:
        await session.send("艾特一下你要解除禁言的用户吧 >_<")
        return ''
    judge = await judge_permission(session, ban_id, user_id)
    if not judge:
        return ''
    try:
        await session.bot.set_group_ban(group_id=group_id, user_id=ban_id, duration=0)
        await session.send(f"[CQ:at,qq={user_id}] 已解除禁言")
    except:
        await session.send(f"[CQ:at,qq={user_id}] 404 解除禁言失败 >_<")


async def judge_permission(session, ban_id, user_id):
    member_list = await session.bot.get_group_member_list(group_id=session.ctx.group_id)
    for member in member_list:
        if member['user_id'] == user_id:
            if member['role'] == 'member':
                await session.send(f"[CQ:at,qq={user_id}] 权限不足 >_<")
                return 0
        if member['user_id'] == session.ctx.self_id:
            if member['role'] == 'member':
                await session.send(f"[CQ:at,qq={user_id}] 权限不足 >_<")
                return 0
        if member['user_id'] == eval(ban_id):
            if member['role'] in ['admin', 'owner']:
                await session.send(f"[CQ:at,qq={user_id}] 权限不足 >_<")
                return 0
        if session.ctx.self_id == eval(ban_id):
            await session.send("机智如我又怎么会自己禁言自己 [CQ:face,id=12]")
            return 0
    return 1


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
            await session.send(f"[{name}]可能的含义有：\n{' | '.join(trans)}")
        else:
            await session.send(f"未找到[{data['text']}]的释义，已为您找到相近词[{name}]释义如下：\n"
                  f"{' | '.join(trans)}")
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


@on_command('help', only_to_me=False)
async def help(session: CommandSession):
    await session.send("我的源码放在https://github.com/lv101/QrobotPlus\n"
                       "尽情探索吧~")