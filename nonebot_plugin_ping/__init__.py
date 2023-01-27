from nonebot.plugin.on import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.params import CommandArg
from httpx import AsyncClient
import nonebot
import asyncio
import platform

try:
    model: int = nonebot.get_driver().config.ping
except:
    model: int = 1



"""PING网址"""
ping = on_command('ping', aliases={'Ping'}, priority=60, block=True)
@ping.handle()
async def _(msg: Message = CommandArg()):
    url = msg.extract_plain_text().strip()
    if model == 1:
        api = f'https://api.gmit.vip/Api/Ping?format=json&ip={url}'
        message = await api_ping(api)
    elif model == 2:
        message = await cmd_ping(url)
    else:
        message = "PING 配置项填写有误, 联系 SUPPERUSER 检查!"
    await ping.finish(message)

async def api_ping(api):
    async with AsyncClient() as client:
        res = (await client.get(api)).json()
        if res["code"] == 200:
            url = (res["data"]["host"])
            ip = (res["data"]["ip"])
            max = (res["data"]["ping_max"])
            min = (res["data"]["ping_min"])
            avg = (res["data"]["ping_avg"])
            place = (res["data"]["location"])
            res = f"域名: {url}\nIP: {ip}\n最大延迟: {max}\n最小延迟: {min}\n平均延迟: {avg}\n服务器归属地: {place}"
            return res
        elif res["code"] == 201:
            res = (res["data"])
            return res
        else:
            return "寄"

async def cmd_ping(url):
    # 获取系统信息, Windows 请求默认 4 次, Linux 请求默认不会停止.
    sys = platform.system()
    # 由于不同系统参数不同, 这里做一下判断.
    if sys == "Windows":
        url = f"ping {url} -n 4"
    elif sys == "Linux":
        # Ubuntu 系统是 -c , 其它发行版未测试.
        url = f"ping {url} -c 4"
    else:
        # 其它系统未测试.
        url = f"ping {url}"
    p = await asyncio.subprocess.create_subprocess_shell(url, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await p.communicate()
    try:
        result = (stdout or stderr).decode('gb2312')
    except Exception:
        result = str(stdout or stderr)
    result = result.strip()
    return result



"""二维码生成"""
qrcode = on_command('qrcode', aliases={'二维码', '二维码生成'}, priority=60, block=True)
@qrcode.handle()
async def _(msg: Message = CommandArg()):
    url = msg.extract_plain_text().strip()
    api = f'https://api.gmit.vip/Api/QrCode?text={url}'
    await qrcode.finish(MessageSegment.image(file=api))



"""WHOIS查询"""
whois = on_command('whois', aliases={'whois', 'whois查询'}, priority=60, block=True)
@whois.handle()
async def _(msg: Message = CommandArg()):
    url = msg.extract_plain_text().strip()
    api = f'http://whois.4.cn/api/main?domain={url}'
    message = await whois_search(api)
    await whois.finish(message)
    
async def whois_search(api):
    async with AsyncClient() as client:
        res = (await client.get(api)).json()
        if res["data"]["status"] == "":
            return "寄"
        else:
            url = (res["data"]["domain_name"])
            reg = (res["data"]["registrars"])
            email = (res["data"]["owner_email"])
            regtime = (res["data"]["create_date"])
            exptime = (res["data"]["expire_date"])
            dnsserver = (res["data"]["nameserver"])
            status = (res["data"]["status"])
            updatetime = (res["data"]["update_date"])
            res = f"请求域名: {url}\n注册商: {reg}\n邮箱: {email}\n注册时间: {regtime}\n过期时间: {exptime}\nDNS服务器: {dnsserver}\n域名状态: {status}\n更新时间: {updatetime}"
            return res
            
