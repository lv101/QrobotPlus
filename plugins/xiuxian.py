import json
import datetime
import random

from nonebot import on_command, CommandSession, permission

@on_command('修仙', aliases=['签到', 'xiuxian'], permission=permission.GROUP_MEMBER, only_to_me=False)
async def xiuxian(session: CommandSession):
    try:
        with open('xiuxian_rank.json', 'r') as f:
            today = str(datetime.date.today())
            yesterday = str(datetime.date.today() + datetime.timedelta(-1))
            all_datas = json.loads(f.read())
            group_ids = []
            try:
                for datas in all_datas:
                    group_ids.append(datas['group_id'])
                    if datas['group_id'] == session.ctx.group_id:
                        user_ids = []
                        for user in datas['user']:
                            user_ids.append(user['user_id'])
                            if user['user_id'] == session.ctx.user_id:
                                if today in user['data']['date']:
                                    await session.send("道友今日已完成修炼，修行之道不可操之过急", at_sender=True)
                                else:

                                        user['data']['counts'] += 1
                                        user['data']['date'].append(today)
                                        result1 = await check_effort(yesterday, user['data'])  # 检查昨日是否修行，奖励修行点
                                        result2 = await check_talent(user['data'])             # 检查修行等级，奖励天赋点
                                        user['data']['score'] += 5 + user['data']['effort'] + user['data']['talent']

                                        result2 = await check_talent(user['data'])
                                        if result2:
                                            result2 = result2 + '\n'
                                        await session.send(result1 + result2 + f"道友当前天赋点：{user['data']['talent']} | 修行点：{user['data']['effort']}\n仙途漫漫，要坚持修炼哦", at_sender=True)

                        if session.ctx.user_id not in user_ids:
                            nickname = session.current_arg_text.strip()
                            if not nickname:
                                await session.pause("请输入你的修行昵称(6个字符以内)：")
                            if not nickname:
                                nickname = '修行者'
                            datas['user'].append({'user_id': session.ctx.user_id, 'nickname': nickname[:6], 'data': {'start': today, 'counts': 1,
                                                  'count': 1, 'talent': 1, 'effort': 0, 'score': 5, 'level': 0, 'date': [today]}})
                            await session.send("修炼成功,达成成就[初窥仙途]\n道友当前天赋点：1 | 修行点：0", at_sender=True)

                if session.ctx.group_id not in group_ids:
                    nickname = session.current_arg_text.strip()
                    if not nickname:
                        await session.pause("请输入你的修行昵称(6个字符以内)：")
                    if not nickname:
                        nickname = '修行者'
                    all_datas.append({'group_id': session.ctx.group_id, 'user': [{'user_id': session.ctx.user_id, 'nickname': nickname[:6],
                                      'data': {'start': today, 'counts': 1, 'count': 1, 'talent': 1, 'effort': 0,
                                               'score': 5, 'level': 0, 'date': [today]}}]})
                    await session.send("修炼成功,达成成就[初窥仙途]\n道友当前天赋点：1 | 修行点：0", at_sender=True)
            except:
                await session.send("啊哦，仙网404，请再尝试修炼一次吧", at_sender=True)
        with open('xiuxian_rank.json', 'w') as f:
            json.dump(all_datas, f)
    except FileNotFoundError:
        with open('xiuxian_rank.json', 'w') as f:
            today = str(datetime.date.today())
            new_data = []
            nickname = session.current_arg_text.strip()
            if not nickname:
                await session.pause("请输入你的修行昵称(6个字符以内)：")
            if not nickname:
                nickname = '修行者'
            new_data.append({'group_id': session.ctx.group_id, 'user': [{'user_id': session.ctx.user_id,
                             'nickname': nickname[:6], 'data': {'start': today, 'counts': 1, 'count': 1,
                             'talent': 1, 'effort': 0, 'score': 5, 'level': 0, 'date': [today]}}]
                             })
            json.dump(new_data, f)
            await session.send("修炼成功,达成成就[初窥仙途]\n道友当前天赋点：1 | 修行点：0", at_sender=True)


@on_command('view_rank', permission=permission.GROUP_MEMBER, only_to_me=False)
async def view_rank(session: CommandSession):
    with open('xiuxian_rank.json', 'r') as f:
        all_datas = json.loads(f.read())
        if not all_datas:
            await session.send("呜呼哀哉，仙道中落，吾辈竟无人修此道", at_sender=True)
            return ''
        group_ids = []
        data = []
        rank = []
        for datas in all_datas:
            group_ids.append(datas['group_id'])
            if datas['group_id'] == session.ctx.group_id:
                for user in datas['user']:
                    if user['data']['level'] == 0:
                        level = "修士"
                    else:
                        level = xiuxian_level[user['data']['level']-1][0]
                    data.append(['', user['nickname'], str(user['user_id']), 'exp：'+str(user['data']['score'])+'/'+str(xiuxian_level[user['data']['level']][1]), level, str(user['data']['score'])])

        if not group_ids or not data:
            await session.send("呜呼哀哉，仙道中落，吾辈竟无人修此道", at_sender=True)
            return ''
        data = sorted(data, key=lambda x: x[5], reverse=True)
        for i in range(len(data)):
            data[i][0] = f'{i+1}' + data[i][0]
            del data[i][5]
            rank.append(' | '.join(data[i]))
        await session.send('\n-------修仙排行榜-------\n'+'\n'.join(rank)+'\n'+'-'*22, at_sender=True)


async def check_effort(yesterday, data):        # 检查昨日是否修行，奖励修行点
    result1 = ''
    if yesterday in data['date']:
        data['count'] += 1
        if data['count'] > 10:
            result1 = f"修行成功！道友已连续修行{data['count']}日\n"
        elif data['count'] == 10:
            data['effort'] = 6
            result1 = f"修行成功！道友已连续修行{data['count']}日，获得修行点+3\n"
        elif data['count'] > 8:
            result1 = f"修行成功！道友已连续修行{data['count']}日\n"
        elif data['count'] == 8:
            data['effort'] = 3
            result1 = f"修行成功！道友已连续修行{data['count']}日，获得修行点+2\n"
        elif data['count'] > 3:
            result1 = f"修行成功！道友已连续修行{data['count']}日\n"
        elif data['count'] == 3:
            data['effort'] = 1
            result1 = f"修行成功！道友已连续修行{data['count']}日，获得修行点+1\n"
        elif data['count'] == 2:
            result1 = f"修行成功！道友已连续修行{data['count']}日\n"
        else:
            result1 = "修行成功！\n"
    else:
        data['count'] = 1
        data['effort'] = 0
        result1 = f"修行成功！由于道友昨日未修炼，连续修行中断\n"
    return result1


async def check_talent(data):         # 检查修行等级，奖励天赋点
    result2 = ''
    level = await check_level(data)
    if 6000 <= data['score'] and level:
        if random.randrange(10):
            data['score'] -= 100
            result2 = "哀哉，道友飞升失败，仙力-100，继续努力修炼吧！"
        else:
            print(f"wow 恭喜道友，贺喜道友。飞升成功\n累计修行{len(data['date'])}日\n新的世界在等待你的探索！")
    elif 5980 < data['score'] < 6000:
        result2 = "道友仙缘深厚，预祝道友飞升顺利~"
    elif 5000 <= data['score'] < 5800 and level:
        if random.randrange(5):
            data['score'] -= 50
            result2 = "哀哉，道友渡劫失败，仙力-60"
        else:
            result2 = "恭喜道友渡劫成功！"
    elif 3000 <= data['score'] < 5000 and level:
        if not random.randrange(3):
            data['talent'] = 10
            result2 = "贺喜道友渡劫成功，获得天赋点+1"
        else:
            data['score'] -= 20
            result2 = "哀哉，道友渡劫失败，仙力-30"
    elif 2200 <= data['score'] < 3000 and level:
        data['talent'] = 9
        result2 = "贺喜道友化神成功，奖励天赋点+1"
    elif 1500 <= data['score'] < 2200 and level:
        data['talent'] = 8
        result2 = "贺喜道友晋升元婴期，奖励天赋点+1\nwow 恭喜道友获得秘境藏宝，额外奖励天赋点+1"
    elif 600 <= data['score'] < 1500 and level:
        data['talent'] = 6
        result2 = "贺喜道友结成金丹，获得奖励天赋点+2"
    elif 300 <= data['score'] < 600 and level:
        data['talent'] = 4
        result2 = "恭喜道友已成为开光期修士，获得奖励天赋点+2"
    elif 100 <= data['score'] < 300 and level:
        data['talent'] = 2
        result2 = "贺喜道友筑基成功，获得奖励天赋点+1"
    else:
        data['talent'] = 1
    return result2


xiuxian_level = (('筑基期', 100),
                 ('开光期', 300),
                 ('金丹期', 600),
                 ('元婴期', 1500),
                 ('化神期', 2200),
                 ('渡劫期', 3000),
                 ('大乘期', 5000),
                 ('飞升', 6666))


async def check_level(data):            # 检查修炼等级
    exp = data['score']
    level = data['level']
    while exp >= xiuxian_level[level][1]:
        data['level'] = level + 1
        return 1


@on_command('del_rank', permission=permission.GROUP_OWNER | permission.SUPERUSER)
async def del_rank(session: CommandSession):
    with open('xiuxian_rank.json', 'r') as f:
        all_datas = json.loads(f.read())
        delete = ''
        for i in range(len(all_datas)):
            if all_datas[i]['group_id'] == session.ctx.group_id:
                delete = i
    print(delete)
    if not delete == '':
        del all_datas[i]
        with open('xiuxian_rank.json', 'w') as f:
            json.dump(all_datas, f)
        await session.send("数据已重置", at_sender=True)
    else:
        await session.send("呜呼哀哉，仙道中落，吾辈竟无人修此道", at_sender=True)


@on_command('del_all_rank', permission=permission.SUPERUSER)
async def del_all_rank(session: CommandSession):
    with open('xiuxian_rank.json', 'w') as f:
        json.dump([], f)
    await session.send("数据已重置", at_sender=True)


@on_command('xiuxian_help', permission=permission.GROUP_MEMBER, only_to_me=False)
async def xiuxian_help(session: CommandSession):
    result = "\n修仙系统是一个每日签到获取经验值的虚拟小游戏，随着经验值的增长，你可以突破不同的境界，境界越高，突破难度越大。\n" \
             "修仙系统常用指令有：\n" \
             "\t/xiuxian -> 每日签到\n" \
             "\t/view_rank -> 查看排行榜\n" \
             "\t/del_rank -> 清除排行榜记录(仅群主可用，该指令会清除当前群的所有修仙记录，慎用！)"
    await session.send(result, at_sender=True)