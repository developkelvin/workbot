import discord
import logging
from worktime import start_work, end_work
from env import token

##########################################
BOT_NAME = 'WorkBot'
__author__ = "Kelvin Jung"
__copyright__ = "Copyright (C) 2020 Kelvin Jung"
__license__ = "MIT"
__version__ = "0.0.1"

BOT_INFO = ' '.join([BOT_NAME, __version__, __copyright__])
##########################################
SUCCESS = 1
FAILURE = 2
START_INFO_NOT_EXIST = 3
##########################################


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client() #This client is our connection to Discord.

# asyncio 관련 레퍼런스 : https://dojang.io/mod/page/view.php?id=2469

# client의 이벤트를 정의해 줌
@client.event 
async def on_ready(): # 로그인이 완료 되었을 때 실행되는 함수
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):# 메세지를 수신했을 때 실행되는 함수
    if message.author == client.user: # 봇이 말하는 내용은 무시
        return

    if message.content.startswith('!봇정보'):
        await message.channel.send('출퇴근 관리와 업무 관리를 지원하는 봇입니다.\n' + BOT_INFO)
    
    if message.content.startswith('!도움말'):
        await message.channel.send('!봇정보, !출근, !퇴근')

    if message.content.startswith('!출근'):
        res = start_work(message.author)
        
        if res['status_code'] == FAILURE:
            await message.channel.send(f'오류가 발생했습니다. STATUS CODE : {res["status_code"]}')
        else:
            await message.channel.send(f'{message.author.name}이 출근했습니다.')

    if message.content.startswith('!퇴근'):
        res = end_work(message.author)
        

        if res['status_code'] == FAILURE:
            await message.channel.send(f'오류가 발생했습니다. STATUS CODE : {res["status_code"]}')
        elif res['status_code'] == START_INFO_NOT_EXIST:
            await message.channel.send(f'출근을 하지 않았습니다.')
        else:
            await message.channel.send(f'{message.author.name}이 퇴근했습니다.')
            
            await message.channel.send(res['msg'])

client.run(token)
