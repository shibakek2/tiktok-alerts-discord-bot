#### YOU CAN TOGGLE ON OR OFF THE EVENTS. THEY ARE ALL SENT VIA DISCORD


ENABLE_SUBSCRIBE_EVENT = True
ENABLE_RANK_UPDATE_EVENT = True
ENABLE_CONNECT_EVENT = True
ENABLE_JOIN_EVENT = True
ENABLE_GIFT_EVENT = True
ENABLE_COMMENT_EVENT = True
ENABLE_LIKE_EVENT = True
ENABLE_SOCIAL_EVENT = True # This is shares
ENABLE_ROOM_USER_SEQ_EVENT = True # This will get the current live user count
tiktok_channel = ""
bot_name = ""
toke = ''
log_channel_id =  12345



import discord
from discord.ext import commands
from TikTokLive.client.errors import UserOfflineError  
from TikTokLive.client.client import TikTokLiveClient
from TikTokLive.events import ConnectEvent, GiftEvent, CommentEvent, JoinEvent, LikeEvent, SocialEvent, RoomUserSeqEvent, SubscribeEvent, RankUpdateEvent, LiveEndEvent, DisconnectEvent
import asyncio
import logging
from collections import deque 
import random 
from discord import Embed 
#logging.basicConfig(level=logging.INFO) i turned this off because there is no need for it right now

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

client: TikTokLiveClient = TikTokLiveClient(unique_id=tiktok_channel)

log_queue = deque() 
log_sending = False 

async def process_log_queue():
    global log_sending
    while True:
        if log_queue and not log_sending: 
            log_sending = True
            message = log_queue.popleft() 
            await send_log(message) 
            await asyncio.sleep(1)  
            log_sending = False 
        else:
            await asyncio.sleep(1) 

async def send_log(message):
    channel = bot.get_channel(log_channel_id) 
    if channel:
        embed = Embed(description=message, color=random.randint(0, 0xFFFFFF)) 
        embed.set_footer(text=bot_name) 
        await channel.send(embed=embed) 
    else:
        print("Channel not found!")  

@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    if ENABLE_CONNECT_EVENT:
        log_queue.append(f"{bot_name} Is Now Running\n\nConnected to @{event.unique_id}!")  

@client.on(JoinEvent)
async def on_join(event: JoinEvent):
    if ENABLE_JOIN_EVENT:
        log_queue.append(f"{event.user.unique_id} has joined the stream!")

@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    if ENABLE_GIFT_EVENT:
        if event.gift.streakable:
            log_queue.append(f"{event.user.unique_id} sent {event.repeat_count}x \"{event.gift.name}\"") 
        else:
            log_queue.append(f"{event.user.unique_id} sent \"{event.gift.name}\"") 

@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    if ENABLE_COMMENT_EVENT:
        log_queue.append(f"{event.user.unique_id}: {event.comment}") 

@client.on(LikeEvent)
async def on_like(event: LikeEvent):
    if ENABLE_LIKE_EVENT:
        log_queue.append(f"{event.user.unique_id} liked the stream!") 

@client.on(SocialEvent)
async def on_social(event: SocialEvent):
    if ENABLE_SOCIAL_EVENT:
        log_queue.append(f"{event.user.unique_id} Shared The Live!") 

@client.on(RoomUserSeqEvent)
async def on_room_user_seq(event: RoomUserSeqEvent):
    if ENABLE_ROOM_USER_SEQ_EVENT:
        log_queue.append(f"Room user count updated\n\n {event.total} users in the room.")

@client.on(SubscribeEvent)
async def on_subscribe(event: SubscribeEvent):
    if ENABLE_SUBSCRIBE_EVENT:
        log_queue.append(f"New Subscriber!\n\n{event.user.unique_id} subscribed!")

@client.on(RankUpdateEvent)
async def on_rank_update(event: RankUpdateEvent):
    if ENABLE_RANK_UPDATE_EVENT:
        log_queue.append(f"{event.user.unique_id} rank updated to {event.new_rank}!")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"TikTok Channel @{tiktok_channel}"))  # Set bot status

async def run_tiktok_client():
    try:
        await client.start()
    except UserOfflineError:
        print(f"The user is offline. The Discord bot will continue running.")

async def run_discord_bot():
    await bot.start(toke)

user_was_live = False

async def check_user_live_status():
    global user_was_live 
    channel = bot.get_channel(log_channel_id) 
    while True:
        user_live = await client.is_live()
        if user_live and not user_was_live:
            user_was_live = True 
            if channel:
                await channel.send(f"The TikTok channel is now live! Watch here: https://www.tiktok.com/@{tiktok_channel}/live")
            else:
                print("Channel not found!")
        elif not user_live:
            user_was_live = False 
            print("User is not live. Checking again in 2 minutes...")
        await asyncio.sleep(120)

async def main():
    await asyncio.gather(
        run_tiktok_client(),
        run_discord_bot(),
        process_log_queue(),
        check_user_live_status()
    )

if __name__ == '__main__':
    asyncio.run(main()) 
