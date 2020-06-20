# import pytz
import nonebot
import requests
from lxml import etree
# from datetime import datetime
from fake_useragent import UserAgent
from aiocqhttp.exceptions import Error as CQHttpError


@nonebot.scheduler.scheduled_job('cron', hour=8)
async def bing_pic():
    bot = nonebot.get_bot()
    # now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        group_id_list = [660322651, 1127661224]
        result = bing_t()
        if not result:
            return
        for group_id in group_id_list:
            await bot.send_group_msg(group_id=group_id, message=result)
    except CQHttpError:
        print('发送失败')

def bing_t():
    try:
        url = "https://cn.bing.com"
        headers = {"User-Agent": UserAgent().random}
        print("正在抓取图片中,请稍候...")
        r_text = requests.get(url, headers=headers).text
        tags = etree.HTML(r_text)
        url_pic = tags.xpath('//link[@id="bgLink"]/@href')[0]
        img_url = url + url_pic
        img_info = tags.xpath('//a[@id="sh_cp"]/@title')[0]
        message = f"#每日一图#\n{img_info}\n{img_url}"
        if message:
            print("爬取成功")
            return message
        else:
            print("爬取失败")
    except:
        print("爬取失败2")