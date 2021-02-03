# -*- coding: utf-8 -*- 

import discord
import asyncio
import datetime
import urllib
import requests
import re
import os
import config
import json
import random
from urllib.request import HTTPError
from discord.ext import commands, tasks
from itertools import cycle

intents = discord.Intents.default()
intents.members = True
bot = discord.Client()
bot = commands.Bot(command_prefix=config.bot["prefix"], help_command=None, description='아크봇', intents=intents)
bot.remove_command('help')
#bicon -> bot icon, ticon -> team icon
bicon = "https://postfiles.pstatic.net/MjAyMDEyMTlfNjUg/MDAxNjA4MzgwMjMwMTk1.vpGaTsHFbFfhvPpt9Hm1NqSDr0DZre02K-usz16qWjgg.bJpkQYomYDzFn9h4kOVuzcs5zw6pPS0JvUTXxtMRH4wg.PNG.kingstonlee/179_20201219070213.png?type=w966"
blankicon = 'https://postfiles.pstatic.net/MjAyMDEyMzBfMjMz/MDAxNjA5MjU3MjI0MjY1.Ywa3JgqklresO2beNqiCyASxDU_CxOIf1DcfL7g0l90g.oJzcdR5bxgQ36qQ8E_NYbPtFOXw7kMYXXPyvRVQL61Ig.PNG.kingstonlee/9HZBYcvaOEnh4tOp5EqgcCr_vKH7cjFJwkvw-45Dfjs.png?type=w966'

async def readjson(filename):
    try:
        with open(f'./json/{filename}.json', 'r', encoding="utf-8") as read_file:
            return json.load(read_file)
    except ValueError as e:
        print(f'Json파일 로드실패\n에러 코드: {e}')
        return None

async def writejson(filename, content):
    with open(f'./json/{filename}.json', 'w', encoding="utf-8") as write_file:
        json.dump(content, write_file, ensure_ascii=False, indent=4)

def owner(ctx):
    if str(ctx.author.id) in config.bot["owner"]:
        return True

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.playing, name=f"아크야 도움 | {len(bot.guilds)}서버"))
    print("준비완료")

@bot.event
async def on_message(message):
    try:
        if "아크야" in message.content:
            json=await readjson(str(message.guild.id))
            json[str(message.author.id)]['exp']+=10
            await writejson(str(message.guild.id), json)
        else:
            pass
    except KeyError:
        pass
    await bot.process_commands(message)

@bot.event
async def on_guild_join(guild):
    channel=bot.get_channel(789330923111710801)
    data = {
        guild.owner.id : {
            "balance": 500,
            "exp": 0
        }
    }
    data2 = {
        guild.id : 0
    }
    await writejson(str(guild.id), data)
    await writejson('anno', data2)
    await channel.send(f'> {guild.name}에 초대받았습니다.')

@bot.event
async def on_guild_remove(guild):
    channel=bot.get_channel(789330923111710801)
    await channel.send(f'> {guild.name}에서 강퇴당했습니다.')
    file = f"./json/{guild.id}.json"
    if os.path.isfile(file):
        os.remove(file)
    else:
        pass

@bot.event
async def on_message_delete(message):
    json = await readjson('anno')
    try:
        channel = bot.get_channel(json[str(message.guild.id)])
        dem = discord.Embed(title='메세지 삭제됨', description=f'{message.channel.mention}에서 메세지 **{message.id}** 삭제됨\n**메세지 내용**: {message.content}', timestamp=datetime.datetime.utcnow(), colour=0xFF0000)
        dem.set_author(name=f'메세지 작성자 - {message.author} ({message.author.id})', icon_url=f'{message.author.avatar_url}')
        return await channel.send(embed=dem)
    except AttributeError:
        pass

@bot.event
async def on_member_join(member):
    json = await readjson('anno')
    try:
        channel = bot.get_channel(json[str(member.guild.id)])
        if member.bot:
            jem = discord.Embed(title='입장로그', description=f'**{member}** 님이 서버입장', timestamp=datetime.datetime.utcnow(), colour=0x00ff2a)
            jem.set_thumbnail(url=member.avatar_url)
            jem.add_field(name='🤖봇 입니다.', value=f'닉네임: **{member}**\n아이디: **{member.id}**\n멘션: {member.mention}')
            return await channel.send(embed=jem)
        else:
            jem = discord.Embed(title='입장로그', description=f'**{member}** 님 서버입장', timestamp=datetime.datetime.utcnow(), colour=0x00ff2a)
            jem.set_thumbnail(url=member.avatar_url)
            jem.add_field(name='👤유저 입니다.', value=f'닉네임: **{member}**\n아이디: **{member.id}**\n멘션: {member.mention}')
            return await channel.send(embed=jem)
    except AttributeError:
        pass

@bot.event
async def on_member_remove(member):
    json = await readjson('anno')
    try:
        channel = bot.get_channel(json[str(member.guild.id)])
        if member.bot:
            jem = discord.Embed(title='퇴장로그', description=f'**{member}** 님이 서버퇴장', timestamp=datetime.datetime.utcnow(), colour=0xff0000)
            jem.set_thumbnail(url=member.avatar_url)
            jem.add_field(name='🤖봇 입니다.', value=f'닉네임: **{member}**\n아이디: **{member.id}**\n멘션: {member.mention}')
            return await channel.send(embed=jem)
        else:
            jem = discord.Embed(title='퇴장로그', description=f'**{member}** 님 서버퇴장', timestamp=datetime.datetime.utcnow(), colour=0xff0000)
            jem.set_thumbnail(url=member.avatar_url)
            jem.add_field(name='👤유저 입니다.', value=f'닉네임: **{member}**\n아이디: **{member.id}**\n멘션: {member.mention}')
            return await channel.send(embed=jem)
    except AttributeError:
        pass

@bot.event
async def on_member_update(before, after):
    json = await readjson('anno')
    try:
        if before.nick==None and after.nick==None:
            pass
        else:
            channel = bot.get_channel(json[str(before.guild.id)])
            upem = discord.Embed(title="닉네임변경 로그", description=f'{before.mention}님 닉네임 변경\n`{before.nick}` -> `{after.nick}`', timestamp=datetime.datetime.utcnow(), colour=0xebcb00)
            upem.set_author(name=f'{before}', icon_url=before.avatar_url)
            return await channel.send(embed=upem)
    except AttributeError:
        pass

@bot.event
async def on_guild_channel_create(channel):
    json = await readjson('anno')
    try:
        logchannel = bot.get_channel(json[str(channel.guild.id)])
        chcem = discord.Embed(title='채널생성 로그', description=f'{channel.mention} 채널 생성됨', timestamp=datetime.datetime.utcnow(), colour=0x00ff2a)
        return await logchannel.send(embed=chcem)
    except AttributeError:
        pass

@bot.event
async def on_guild_channel_delete(channel):
    json = await readjson('anno')
    try:
        logchannel = bot.get_channel(json[str(channel.guild.id)])
        chcem = discord.Embed(title='채널삭제 로그', description=f'**{channel}** 채널 삭제됨', timestamp=datetime.datetime.utcnow(), colour=0xff0000)
        return await logchannel.send(embed=chcem)
    except AttributeError:
        pass

@bot.event
async def on_webhooks_update(channel):
    json = await readjson('anno')
    try:
        logchannel = bot.get_channel(json[str(channel.guild.id)])
        em = discord.Embed(title='웹훅업데이트 로그', description=f'{channel.mention} 채널에 웹훅 업데이트됨', timestamp=datetime.datetime.utcnow(), colour=0xebcb00)
        return await logchannel.send(embed=em)
    except AttributeError:
        pass

@bot.event
async def on_guild_role_create(role):
    json = await readjson('anno')
    try:
        logchannel = bot.get_channel(json[str(role.guild.id)])
        em = discord.Embed(title='역할생성 로그', description=f'{role.mention} 역할 생성됨', timestamp=datetime.datetime.utcnow(), colour=0x00ff2a)
        return await logchannel.send(embed=em)
    except AttributeError:
        pass

@bot.event
async def on_guild_role_delete(role):
    json = await readjson('anno')
    try:
        logchannel = bot.get_channel(json[str(role.guild.id)])
        em = discord.Embed(title='역할삭제 로그', description=f'**{role}** 역할 삭제됨', timestamp=datetime.datetime.utcnow(), colour=0xff0000)
        return await logchannel.send(embed=em)
    except AttributeError:
        pass

@bot.event
async def on_member_ban(guild, member):
    json = await readjson('anno')
    try:
        logchannel = bot.get_channel(json[str(guild.id)])
        em = discord.Embed(title='유저 밴 로그', description=f'{member.mention}님이 관리자에 의해 **차단** 됨', timestamp=datetime.datetime.utcnow(), colour=0xebcb00)
        return await logchannel.send(embed=em)
    except AttributeError:
        pass

@bot.event
async def on_member_unban(guild, member):
    json = await readjson('anno')
    try:
        logchannel = bot.get_channel(json[str(guild.id)])
        em = discord.Embed(title='유저 언밴 로그', description=f'**{member}**님이 관리자에 의해 **차단해제** 됨', timestamp=datetime.datetime.utcnow(), colour=0x1f80ff)
        return await logchannel.send(embed=em)
    except AttributeError:
        pass

@bot.event
async def on_invite_create(invite):
    json = await readjson('anno')
    try:
        logchannel = bot.get_channel(json[str(invite.guild.id)])
        em = discord.Embed(title='초대링크 생성 로그', description=f'`{invite}` 초대링크 생성됨', timestamp=datetime.datetime.utcnow(), colour=0x00ff2a)
        return await logchannel.send(embed=em)
    except AttributeError:
        pass

#도움 명령어
@bot.command()
async def 도움(ctx):
    embed=discord.Embed(title='아크봇 도움말', timestamp=datetime.datetime.utcnow(), colour=0x00FFB7)
    embed.add_field(name="관리명령어", value="> **아크야 관리** 를 입력해주세요!", inline=False)
    embed.add_field(name="기본명령어", value="> **아크야 기본** 을 입력해주세요!", inline=False)
    embed.add_field(name="전적명령어", value="> **아크야 전적** 을 입력해주세요!", inline=False)
    embed.add_field(name="도박명령어", value="> **아크야 도박** 을 입력해주세요!", inline=False)
    embed.add_field(name="기타", value="[아크봇 공식서버](https://discord.gg/9xc32PGJMU)\n[아크봇 소속서버](https://discord.gg/quzArR5)\n[아크봇 초대하기](https://discord.com/api/oauth2/authorize?client_id=781395276689965077&permissions=8&scope=bot)\n아크봇을 서버에 추가하시면 [이용약관](https://github.com/Arkxyz/Policy)에 동의한 것으로 간주됩니다.")
    embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
    return await ctx.send(embed=embed)

@bot.command()
async def 관리(ctx):
    adem=discord.Embed(title="아크봇 관리명령어", description='서버로그를 확인하시려면 **아크야 로그 [로그들을 보낼 채널 멘션]** 으로 로그채널을 설정해주셔야 합니다!', timestamp=datetime.datetime.utcnow(), colour=0x00ffb7)
    adem.add_field(name="아크야 청소 [삭제할 메세지 숫자]", value="> 메세지 삭제 명령어입니다.", inline=False)
    adem.add_field(name="아크야 밴 [차단할 멤버 멘션]", value="> 유저 밴 명령어입니다.", inline=False)
    adem.add_field(name="아크야 킥 [추방할 멤버 멘션]", value="> 유저 킥 명령어입니다.", inline=False)
    adem.add_field(name="아크야 슬로우 [슬로우모드 시간(초)]", value="> 슬로우모드 설정 명령어입니다.", inline=False)
    adem.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=adem)

@bot.command()
async def 기본(ctx):
    uem=discord.Embed(title="아크봇 기본명령어", timestamp=datetime.datetime.utcnow(), colour=0x00ffb7)
    uem.add_field(name="아크야 핑", value="> 당신의 핑 상태를 보여줍니다.", inline=False)
    uem.add_field(name="아크야 내정보", value="> 당신의 디스코드 계정 정보를 보여줍니다.", inline=False)
    uem.add_field(name="아크야 서버정보", value="> 해당 서버의 정보를 보여줍니다.", inline=False)
    uem.add_field(name="아크야 봇정보", value="> 봇의 정보와 상태를 보여줍니다.", inline=False)
    uem.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=uem)

@bot.command()
async def 전적(ctx):
    uem=discord.Embed(title="아크봇 전적명령어", timestamp=datetime.datetime.utcnow(), colour=0x00ffb7)
    uem.add_field(name="아크야 롤 [소환사명]", value="> 당신의 롤 전적을 보여드립니다!\n> **대문자와 소문자는 꼭! 구분하여 써주세요.**", inline=False)
    uem.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=uem)

@bot.command()
async def 도박(ctx):
    dem=discord.Embed(title="아크봇 도박명령어", description="도박게임들을 진행하시려면 **아크야 계좌생성** 으로 계좌를 개설해주셔야 합니다!\n서버 주인의 계좌는 봇을 추가할 때 생성됩니다!", timestamp=datetime.datetime.utcnow(), colour=0x00ffb7)
    dem.add_field(name="아크야 계좌생성", value="> 계좌를 개설해주는 명령어입니다.", inline=False)
    dem.add_field(name="아크야 내계좌", value="> 당신의 계좌를 보여주는 명령어입니다. (아크코인 잔액, 경험치 확인가능)", inline=False)
    dem.add_field(name="아크야 이체 [아크코인 이체대상 멘션]", value="> 다른 사람에게 아크코인을 이체하는 명령어입니다. (두 유저 모두 계좌가 개설된 상태여야 합니다.)", inline=False)
    dem.add_field(name="아크야 주사위 [1~6사이의 숫자]", value="> 주사위를 굴려주는 명령어입니다.", inline=False)
    dem.add_field(name="아크야 동전 [앞 or 뒤]", value="> 동전을 뒤집어주는 명령어입니다.", inline=False)
    dem.add_field(name="아크야 슬롯 [베팅금액]", value="> 슬롯머신을 돌려주는 기능입니다.", inline=False)
    dem.add_field(name="아크야 인출", value="> 잔액이 0원일 경우에 50 아크코인을 충전해드립니다!", inline=False)
    dem.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=dem)


#관리자 명령어
@bot.command()
async def 청소(ctx, amount=None):
    if ctx.author.guild_permissions.administrator:
        if amount==None or int(amount)==0:
            await ctx.channel.send(f"{ctx.author.mention} `아크야 청소 [메세지 개수]` 를 입력해주세요.")
            # await asyncio.sleep(3)
            # return await msg1.delete()
        else:
            em=discord.Embed(title='메세지 청소', description=f'**{amount}** 개의 메세지를 정상적으로 삭제했습니다.', timestamp=datetime.datetime.utcnow(), colour=ctx.author.color)
            await ctx.channel.purge(limit=int(amount)+1)
            await ctx.send(embed=em)
    else:
        return await ctx.send(f"{ctx.author.mention}님은 관리자권한이 없습니다.")
    
@bot.command()
async def 밴(ctx, member: discord.Member, *, reason = None):
    if ctx.author.guild_permissions.administrator:
        try:
            await member.ban(reason=reason)
            em = discord.Embed(title=f'{ctx.author.mention}님이 {member.mention}님을 밴했습니다.\n밴 사유 - {reason}', colour=0xff0000)
            return await ctx.send(embed=em)
        except:
            return await ctx.send(f'{ctx.author.mention}, 명령어 형식이 잘못되었습니다.\n명령어 사용법 - 아크야 밴 [밴 유저 멘션]')
    else:
        return await ctx.send(f"{ctx.author.mention}님은 관리자권한이 없습니다.")

@bot.command()
async def 킥(ctx, member: discord.Member, *, reason = None):
    if ctx.author.guild_permissions.administrator:
        try:
            await member.kick(reason=reason)
            em = discord.Embed(title=f'{ctx.author.mention}님이 {member.mention}님을 킥했습니다.\n킥 사유 - {reason}', colour=0xebcb00)
            return await ctx.send(embed=em)
        except:
            return await ctx.send(f'{ctx.author.mention}, 명령어 형식이 잘못되었습니다.\n명령어 사용법 - 아크야 킥 [킥 유저 멘션]')
    else:
        return await ctx.send(f"{ctx.author.mention}님은 관리자권한이 없습니다.")

@bot.command()
async def 슬로우(ctx, seconds: int):
    if ctx.author.guild_permissions.administrator:
        em=discord.Embed(title='슬로우모드 설정', description=f"{ctx.channel.mention}의 슬로우모드를 {seconds}초로 설정했습니다", timestamp=datetime.datetime.utcnow(), colour=ctx.author.color)
        await ctx.channel.edit(slowmode_delay=seconds)
        return await ctx.send(embed=em)
    else:
        return await ctx.send(f'{ctx.author.mention}님은 관리자권한이 없습니다.')

#기본명령어
@bot.command()
async def 핑(ctx):
    if round(bot.latency * 1000) <= 50:
        embed=discord.Embed(
            title=f"{bot.user.name}이 친 탁구공 속도", 
            description=f"<:Green:789376729893699634> **{round(bot.latency *1000)}**ms", 
            timestamp=datetime.datetime.utcnow(),
            color=ctx.author.color
            )
        embed.set_footer(text=ctx.author,icon_url=ctx.author.avatar_url)
    elif round(bot.latency * 1000) <= 100:
        embed=discord.Embed(
            title=f"{bot.user.name}이 친 탁구공 속도", 
            description=f"<:Yellow:789376729952026644> **{round(bot.latency *1000)}**ms", 
            timestamp=datetime.datetime.utcnow(),
            color=ctx.author.color
            )
        embed.set_footer(text=ctx.author,icon_url=ctx.author.avatar_url)
    else:
        embed=discord.Embed(
            title=f"{bot.user.name}이 친 탁구공 속도", 
            description=f"<:Red:789376729453035532> **{round(bot.latency *1000)}**ms", 
            timestamp=datetime.datetime.utcnow(),
            color=ctx.author.color
            )
        embed.set_footer(text=ctx.author,icon_url=ctx.author.avatar_url)
    return await ctx.send(f"{ctx.author.mention}\n", embed=embed)

# @bot.command()
# async def helloworld(ctx):
#     await ctx.send('코딩의 첫걸음을 알리는 메세지이죠!\n<:confetti_ball:781905491612663869>이스터에그 발견<:confetti_ball:781905491612663869>')

@bot.command()
async def 내정보(ctx):
    embed=discord.Embed(title=f'{ctx.author}님의 정보', timestamp=datetime.datetime.utcnow(), colour=ctx.author.color)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.add_field(name='디스코드 닉네임', value=f'{ctx.author}', inline=False)
    embed.add_field(name='디스코드 계정 생성 날짜', value=f'{ctx.author.created_at.strftime("%b %d %Y, %I:%M %p")}', inline=False)
    embed.add_field(name=f'{ctx.guild}내 닉네임', value=f'{ctx.author.nick}', inline=False)
    embed.add_field(name=f'{ctx.guild} 입장 날짜', value=f'{ctx.author.joined_at.strftime("%b %d %Y, %I:%M %p")}', inline=False)
    embed.add_field(name=f'{ctx.guild}내 보유중인 역할', value=f', '.join([str(r.mention) for r in ctx.author.roles]), inline=False)
    embed.set_footer(text=ctx.author,icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
async def 서버정보(ctx):
    guild = ctx.guild
    
    embed = discord.Embed(title=f'{guild.name} ({guild.id})', timestamp=datetime.datetime.utcnow(), colour=ctx.author.color)
    embed.set_thumbnail(url = f'{guild.icon_url}')
    embed.add_field(name = '서버 주인', value = guild.owner.mention, inline = True)
    embed.add_field(name = '서버 유저수', value = guild.member_count, inline = True)
    embed.add_field(name = '서버 보안 레벨', value = guild.verification_level, inline = True)
    embed.add_field(name = '서버 생성 날짜', value = guild.created_at, inline = True)
    embed.add_field(name = '부스트 레벨', value = f'**{guild.premium_tier}**레벨 ({guild.premium_subscription_count}부스트)', inline = True)
    embed.add_field(name = '서버 위치', value = guild.region, inline = True)
    embed.add_field(name = '서버 채팅채널 개수', value = len(guild.text_channels), inline = True)
    embed.add_field(name = '서버 음성채널 개수', value = len(guild.voice_channels), inline = True)
    embed.add_field(name = '서버 잠수채널', value = f'**{guild.afk_channel}**' if guild.afk_channel==None else f'{guild.afk_channel.mention}', inline = True)
    embed.add_field(name = '서버 규칙채널', value = f'**{guild.rules_channel}**' if guild.rules_channel==None else f'{guild.rules_channel.mention}', inline = True)
    embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed = embed)

@bot.command()
async def 봇정보(ctx):
    binf = discord.Embed(title="아크봇 정보", color=0x00FFB7)
    binf.set_thumbnail(url=f"{bicon}")
    binf.add_field(name='사용중인 모듈', value='```py\nimport discord\nimport asyncio\nimport datetime\nimport urllib\nimport requests\nimport re\nimport os\nimport config\nimport json\nimport random\nfrom urllib.request import HTTPError\nfrom discord.ext import commands, tasks\nfrom itertools import cycle\nfrom bs4 import BeautifulSoup\n```', inline=False)
    binf.add_field(name="Discord.py 버전", value=f"**__{discord.__version__}__**", inline=False)
    binf.add_field(name="활동중인 서버수", value=f"**{len(bot.guilds)}** 개의 서버", inline=False)
    binf.add_field(name="사용중인 유저수", value=f"**{len(bot.users)}** 명의 유저", inline=False)
    binf.set_footer(text="dev by ARK#2222", icon_url=f"{bicon}")
    await ctx.send(embed=binf)

#로그채널설정
@bot.command()
async def 로그(ctx, channel: discord.TextChannel):
    if ctx.message.author.guild_permissions.administrator:
        json = await readjson('anno')
        json[str(ctx.guild.id)] = int(channel.id)
        await writejson('anno', json)
        embed = discord.Embed(title=f'채널을 로그채널로 등록하였습니다.', description=f"등록된 채널 : <#{channel.id}>", timestamp=datetime.datetime.utcnow(), colour=0x00FFB7)
        embed.set_footer(text=ctx.author,icon_url=ctx.author.avatar_url)
        return await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="명령어 실행중 오류가 발생했습니다.\n", description=f"**해당 명령어는 서버관리자만 사용할 수 있습니다.**", timestamp=datetime.datetime.utcnow(), colour=0x00FFB7)
        embed.set_footer(text=ctx.author,icon_url=ctx.author.avatar_url)
        return await ctx.send(embed=embed)

#도박 명령어

@bot.command()
async def 랭크(ctx):
    with open(f'./json/{ctx.guild.id}.json', 'r') as f:
        users = json.load(f)
    high_score_list = sorted(users, key=lambda x : users[x].get('balance', 0), reverse=True)
    message = ''
    count=0
    for number, user in enumerate(high_score_list):
        message += (f"**{number+1}위** <@{user}> `{users[user].get('balance', 0)}`:coin:\n")
        count+=1
        if count>1:
            embed = discord.Embed(title='**재산 순위**', description=f'해당 순위표는 서버데이터베이스를 기준으로 정리하였습니다.\n\n{message}', color=ctx.author.colour)
            return await ctx.send(embed=embed)
        else:
            pass

@bot.command()
async def 내계좌(ctx):
    guild = ctx.guild
    json = await readjson(str(guild.id))
    try:
        if json:
            result = json[str(ctx.author.id)]
            balance = result['balance']
            exp = result['exp']
            await ctx.send(f"{ctx.author.mention}님의 계좌\n**아크코인**: `{balance}`:coin:\n**경험치**: `{exp}`:crown:")
        # else:
        #     await ctx.send("저런! 계좌를 찾지 못했어요. `아크야 계좌생성`으로 계좌를 생성해주세요!")
    except KeyError:
        await ctx.send("저런! 계좌를 찾지 못했어요. `아크야 계좌생성`으로 계좌를 개설해주세요!")

@bot.command()
async def 계좌생성(ctx):
    guild = ctx.guild
    json = await readjson(str(guild.id))
    # balance = result['balance']
    try:
        result = json[str(ctx.author.id)]
        if result:
            await ctx.send(f"{ctx.author.mention}님은 이미 계좌가 있습니다. `아크야 내계좌`로 계좌잔액을 확인하세요!")
    except KeyError:
        json[str(ctx.author.id)] = {"balance" : 500, "exp" : 0}
        await writejson(str(guild.id), json)
        await ctx.send(f"{ctx.author.mention}님의 계좌를 개설했어요! `아크야 내계좌`로 계좌잔액을 확인하세요!")

@bot.command()
async def 인출(ctx):
    guild = ctx.guild
    json = await readjson(str(ctx.guild.id))
    try: 
        result = json[str(ctx.author.id)]
    except KeyError:
        return await ctx.send(f"{ctx.author.mention}\n돈을 인출하기 위해선 계좌가 필요해요! `아크야 계좌생성`을 입력하여 계좌를 개설하세요!")
    if result['balance'] != 0:
        await ctx.send(f'{ctx.author.mention}, 돈은 계좌잔액이 0일때만 인출할 수 있어요!')
    else:
        result['balance'] += 50
        await writejson(str(guild.id), json)
        await ctx.send(f'{ctx.author.mention}\n계좌에 +`50`:coin:을 추가했습니다.')

@bot.command()
async def 이체(ctx, member: discord.Member, *, amount=None):
    try:
        if amount == None:
            await ctx.send("보내실 금액을 적어주세요!")
        elif int(amount)==0:
            await ctx.send("보내실 금액을 적어주세요!")
        else:
            json=await readjson(str(ctx.guild.id))
            if json[str(ctx.author.id)]['balance'] < int(amount):
                await ctx.send("잔액이 부족합니다. (삐빅)")
            else:
                json[str(ctx.author.id)]['balance'] -= int(amount)
                json[str(member.id)]['balance'] += int(amount)
                await writejson(str(ctx.guild.id), json)
                await ctx.send(f"{ctx.author.mention}님이 {member.mention}님께 정상적으로 {amount}:coin:을/를 이체했습니다.")
    except KeyError:
        await ctx.send(f"{ctx.author.mention}님 또는 {member.mention}님의 계좌를 찾지 못하였습니다. `아크야 계좌생성`으로 계좌를 개설해주세요!")

#게임 명령어
@bot.command()
async def 주사위(ctx, number=None, amount=None):
    json = await readjson(str(ctx.guild.id))
    try: 
        result = json[str(ctx.author.id)]
    except KeyError:
        return await ctx.send(f"{ctx.author.mention}\n**주사위**게임을 하기 위해선 계좌가 필요해요! `아크야 계좌생성`을 입력하여 계좌를 개설하세요!")

    cho = ['1', '2', '3', '4', '5', '6']
    ran = random.choice(cho)
    if number==None or amount==None:
        return await ctx.send(f"{ctx.author.mention} `아크야 주사위 [1~6의 숫자중 하나] [베팅금액]`을 입력해주세요!")
    elif number not in cho:
        return await ctx.send(f"{ctx.author.mention} 1~6 사이의 숫자만 입력해주세요!")
    elif int(amount)==0:
        return await ctx.send(f"{ctx.author.mention} `0` 아크코인을 베팅할 수는 없습니다!")
    elif result['balance'] < int(amount):
        return await ctx.send(f"{ctx.author.mention}님은 아크코인이 부족합니다!")
    elif ran==number:
        result['balance'] += int(amount)*4
        earncoin = int(amount)*5
        await writejson(str(ctx.guild.id), json)
        return await ctx.send(f"{ctx.author.mention}\n주사위 던지기의 결과는 **{number}**에요! +`{earncoin}`:coin:")
    else:
        result['balance'] -= int(amount)
        await writejson(str(ctx.guild.id), json)
        return await ctx.send(f"{ctx.author.mention} 아쉽게도 숫자를 맞추지 못했어요... 다음에 다시 도전하세요!")

@bot.command()
async def 동전(ctx, coin=None, amount=None):
    json = await readjson(str(ctx.guild.id))
    try:
        result = json[str(ctx.author.id)]
    except KeyError:
        return await ctx.send(f"{ctx.author.mention}\n**동전뒤집기**게임을 하기 위해선 계좌가 필요해요! `아크야 계좌생성`을 입력하여 계좌를 개설하세요!")
    
    cho = ['앞','뒤']
    ran = random.choice(cho)
    if coin==None or amount==None:
        return await ctx.send(f"{ctx.author.mention} `아크야 동전 [앞or뒤] [베팅금액]`을 입력해주세요!")
    elif coin not in cho:
        return await ctx.send(f"{ctx.author.mention} 앞 또는 뒤만 골라주세요!")
    elif int(amount)==0:
        return await ctx.send(f"{ctx.author.mention} `0` 아크코인을 베팅할 수는 없습니다!")
    elif result['balance'] < int(amount):
        return await ctx.send(f"{ctx.author.mention}님은 아크코인이 부족합니다!")
    elif ran==coin:
        result['balance'] += int(amount)
        abcd = int(amount) * 2
        await writejson(str(ctx.guild.id), json)
        return await ctx.send(f"{ctx.author.mention}\n동전 뒤집기의 결과는 **{coin}**! +`{abcd}`:coin:")
    else:
        result['balance'] -= int(amount)
        await writejson(str(ctx.guild.id), json)
        return await ctx.send(f"{ctx.author.mention}\n아쉽게도 면을 맞추지 못했어요... 다음에 다시 도전하세요!")

@bot.command()
async def 슬롯(ctx, *, amount=None):
    json = await readjson(str(ctx.guild.id))
    try:
        result = json[str(ctx.author.id)]
    except KeyError:
        return await ctx.send(f"{ctx.author.mention}\n**잭팟**게임을 하기 위해선 계좌가 필요해요! `아크야 계좌생성`을 입력하여 계좌를 개설하세요!")

    cho = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    num=random.choice(cho)
    
    if amount==None:
        return await ctx.send(f"{ctx.author.mention} `아크야 슬롯 [베팅금액]`을 입력해주세요!")
    elif int(amount)==0:
        return await ctx.send(f"{ctx.author.mention} `0` 아크코인을 베팅할 수는 없습니다!")
    elif result['balance'] < int(amount):
        return await ctx.send(f"{ctx.author.mention}님은 아크코인이 부족합니다!")

    elif num%7 == 0:
        amount2 = int(amount)*2
        amount3 = int(amount)*3
        result['balance'] += amount2
        await writejson(str(ctx.guild.id), json)
        await ctx.send(f'{ctx.author.mention}\n3개를 모두 맞추셨어요! 잭팟이군요! +`{amount3}`:coin:')
    elif num%3 == 0:
        amount2 = int(amount)*2
        result['balance'] += int(amount)
        await writejson(str(ctx.guild.id), json)
        await ctx.send(f'{ctx.author.mention}\n2개를 맞추셨어요! +`{int(amount)}`:coin:')
    else:
        result['balance'] -= int(amount)
        await writejson(str(ctx.guild.id), json)
        await ctx.send(f'{ctx.author.mention}\n1개도 맞추지 못했어요... 다음에 다시 도전하세요!')

bot.run(config.bot['token'])
