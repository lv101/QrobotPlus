import nonebot
from aiocqhttp.exceptions import Error as CQHttpError

@nonebot.scheduler.scheduled_job('cron', hour='8-20')
async def auto_drink():
    bot = nonebot.get_bot()
    # now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        group_id_list = [1127661224]
        for group_id in group_id_list:
            await bot.send_group_msg(group_id=group_id, message=f'喝水小助手提醒您，该喝水啦~')
    except CQHttpError:
        pass