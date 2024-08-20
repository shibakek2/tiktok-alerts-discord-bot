#### YOU CAN TOGGLE ON OR OFF THE EVENTS. THEY ARE ALL SENT VIA DISCORD


ENABLE_SUBSCRIBE_EVENT = True
ENABLE_RANK_UPDATE_EVENT = True
ENABLE_CONNECT_EVENT = False
ENABLE_JOIN_EVENT = True
ENABLE_GIFT_EVENT = True
ENABLE_COMMENT_EVENT = True
ENABLE_LIKE_EVENT = True
ENABLE_SOCIAL_EVENT = True # This is shares
ENABLE_ROOM_USER_SEQ_EVENT = False # This will get the current live user count
ENABLE_FOLLOW_EVENT = True
tiktok_channel = "shibakek0"
bot_name = "Tiktok V1"
toke = ''
log_channel_id =  1268760898181398571
live_ping_channel = 1154960715174658078
import discord
from discord.ext import commands
from TikTokLive.client.errors import UserOfflineError  
from TikTokLive.client.client import TikTokLiveClient
from TikTokLive.events import ConnectEvent, GiftEvent, CommentEvent, JoinEvent, LikeEvent, SocialEvent, RoomUserSeqEvent, SubscribeEvent, RankUpdateEvent, LiveEndEvent, DisconnectEvent, FollowEvent
import asyncio
import logging
from collections import deque 
from discord import Embed 
from datetime import datetime
#logging.basicConfig(level=logging.INFO) i turned this off because there is no need for it right now

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

client: TikTokLiveClient = TikTokLiveClient(unique_id=tiktok_channel)
live_status = False

log_queue = deque() 
log_sending = False 

gift_queue = deque() 
gift_sending = False 

follow_queue = deque() 
follow_sending = False 

chat_queue = deque() 
chat_sending = False

share_queue = deque() 
share_sending = False 

sub_queue = deque() 
sub_sending = False 

join_queue = deque() 
join_sending = False 

gift_log_channel = 1275164654716457052
follow_log_channel = 1275164558222295143
chat_log_channel = 1275164570830246000
share_log_channel = 1275164602031931403
join_log_channel = 1275168055248552099
sub_log_channel = 1275168125100228708
stream_stats_channel = 1275173528827854850

likes = 0
comments = 0
followers = 0
subscribers = 0
gifts = 0
joins = 0
shares = 0

@client.on(LiveEndEvent)
async def on_live_end(_):
    global live_status
    global user_was_live
    global likes
    global comments
    global followers
    global subscribers
    global gifts
    global joins
    global shares
    global live_status
    global user_was_live
    await client.disconnect()
    live_status = False 
    user_was_live = True  
    log_queue.append(f"{tiktok_channel} has ended the live stream.")
    channel = bot.get_channel(live_ping_channel)
    stats_channel = bot.get_channel(stream_stats_channel)
    if channel:
        await channel.send(f"{tiktok_channel} has ended the live stream.")
    if stats_channel: 
        embed = Embed(
            title=f"{tiktok_channel}'s Stream Stats from today",
            description=f"Stream Stats {datetime.now().strftime('%Y-%m-%d')}",
            color=0x800080
        )
        embed.set_footer(text=bot_name, icon_url="https://i.imgur.com/SSWQOAS.png")
        embed.set_author(name=bot_name, icon_url="https://i.imgur.com/SSWQOAS.png")
        embed.add_field(name="Total Subscribers", value=subscribers, inline=True)  
        embed.add_field(name="Total Views", value=joins, inline=True)  
        embed.add_field(name="Total Gifts", value=gifts, inline=True)  
        embed.add_field(name="Total Shares", value=shares, inline=True)  
        embed.add_field(name="Total Followers", value=followers, inline=True)   
        embed.add_field(name="Total Likes", value=likes, inline=True)  
        embed.add_field(name="Total Comments", value=comments, inline=True)  
        await stats_channel.send(embed=embed)
        likes = 0
        comments = 0
        followers = 0
        subscribers = 0
        gifts = 0
        joins = 0
        shares = 0
        await run_tiktok_client()
    else:
        print("Channel not found!")

async def process_log_queue():
    global log_sending
    global gift_sending
    global follow_sending
    global chat_sending
    global share_sending
    global sub_sending
    global join_sending
    while True:
        if log_queue and not log_sending: 
            log_sending = True
            message = log_queue.popleft() 
            await send_log(message, log_channel_id) 
            await asyncio.sleep(1)  
            log_sending = False 
        elif gift_queue and not gift_sending:  
            gift_sending = True
            message = gift_queue.popleft() 
            await send_log(message, gift_log_channel) 
            await asyncio.sleep(1)  
            gift_sending = False  
        elif follow_queue and not follow_sending:  
            follow_sending = True
            message = follow_queue.popleft() 
            await send_log(message, follow_log_channel) 
            await asyncio.sleep(1)  
            follow_sending = False  
        elif chat_queue and not chat_sending:  
            chat_sending = True
            message = chat_queue.popleft() 
            await send_log(message, chat_log_channel) 
            await asyncio.sleep(1)  
            chat_sending = False 
        elif share_queue and not share_sending:  
            share_sending = True
            message = share_queue.popleft() 
            await send_log(message, share_log_channel) 
            await asyncio.sleep(1)  
            share_sending = False    
        elif sub_queue and not sub_sending:  
            sub_sending = True
            message = sub_queue.popleft() 
            await send_log(message, sub_log_channel) 
            await asyncio.sleep(1)  
            sub_sending = False   
        elif join_queue and not join_sending:  
            join_sending = True
            message = join_queue.popleft() 
            await send_log(message, join_log_channel) 
            await asyncio.sleep(1)  
            join_sending = False   
        else:
            await asyncio.sleep(1) 

async def send_log(message, channel_id):
    channel = bot.get_channel(channel_id) 
    if channel:
        embed = Embed(
            title="Log",
            description=message,
            color=0x800080
        )
        embed.set_footer(text=bot_name, icon_url="https://i.imgur.com/SSWQOAS.png") 
        embed.set_thumbnail(url="https://i.imgur.com/SSWQOAS.png") 
        embed.set_author(name=bot_name, icon_url="https://i.imgur.com/SSWQOAS.png")
        embed.add_field(name="Channel", value=tiktok_channel, inline=True)  
        embed.add_field(name="Status", value="Live" if live_status else "Offline", inline=True)
        await channel.send(embed=embed) 
    else:
        print("Channel not found!")  


@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    if ENABLE_CONNECT_EVENT:
        log_queue.append(f"{bot_name} Is Now Running\n\nConnected to @{event.unique_id}!")  

@client.on(JoinEvent)
async def on_join(event: JoinEvent):
    global joins
    if ENABLE_JOIN_EVENT:
        joins += 1
        join_queue.append(f"{event.user.unique_id} has joined the stream!")

@client.on(FollowEvent)
async def on_follow(event: FollowEvent):
    global followers
    if ENABLE_FOLLOW_EVENT:
        followers += 1
        follow_queue.append(f"{event.user.unique_id} has followed!")

@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    global gifts
    if ENABLE_GIFT_EVENT:
        if event.gift.streakable:
            print(event.repeat_count)
            gifts += event.repeat_count
            gift_queue.append(f"{event.user.unique_id} sent {event.repeat_count}x \"{event.gift.name}\"") 
        else:
            gifts += 1
            gift_queue.append(f"{event.user.unique_id} sent \"{event.gift.name}\"") 

@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    global comments
    if ENABLE_COMMENT_EVENT:
        comments += 1
        chat_queue.append(f"{event.user.unique_id}: {event.comment}") 

@client.on(LikeEvent)
async def on_like(event: LikeEvent):
    global likes
    if ENABLE_LIKE_EVENT:
        likes += 1
        log_queue.append(f"{event.user.unique_id} liked the stream!") 

@client.on(SocialEvent)
async def on_social(event: SocialEvent):
    global shares   
    if ENABLE_SOCIAL_EVENT:
        shares += 1
        share_queue.append(f"{event.user.unique_id} Shared The Live!") 

@client.on(RoomUserSeqEvent)
async def on_room_user_seq(event: RoomUserSeqEvent):
    if ENABLE_ROOM_USER_SEQ_EVENT:
        log_queue.append(f"Room user count updated\n\n {event.total} users in the room.")

@client.on(SubscribeEvent)
async def on_subscribe(event: SubscribeEvent):
    global subscribers
    if ENABLE_SUBSCRIBE_EVENT:
        subscribers += 1
        sub_queue.append(f"New Subscriber!\n\n{event.user.unique_id} subscribed!")

@client.on(RankUpdateEvent)
async def on_rank_update(event: RankUpdateEvent):
    if ENABLE_RANK_UPDATE_EVENT:
        log_queue.append(f"{event.user.unique_id} rank updated to {event.new_rank}!")


async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    asyncio.create_task(send_live_ping()) 
    asyncio.create_task(rotate_status()) 

async def run_tiktok_client():
    global live_status
    try:
        await client.start()
        live_status = True
        print(f"{tiktok_channel} is live!")
    except UserOfflineError:
        print(f"{tiktok_channel} is offline. Checking again in 30 seconds...")
        live_status = False
        await asyncio.sleep(30)
        await run_tiktok_client()
    except ConnectionResetError as e:
        print(f"WebSocket connection closed: {e}")
        live_status = False
        await asyncio.sleep(5) 
        await run_tiktok_client()

async def run_discord_bot():
    await bot.start(toke)

user_was_live = False

async def rotate_status():
    global live_status
    await bot.wait_until_ready()
    while True:
        try:
            if live_status:
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{tiktok_channel} Is live on TikTok!"))
            else:
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"TikTok Channel @{tiktok_channel}"))
                await asyncio.sleep(5)
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Tiktok Bot v1"))
                await asyncio.sleep(5)
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Waiting for {tiktok_channel} to go live..."))
        except ConnectionResetError:
            print("ConnectionResetError: Cannot write to closing transport. Reconnecting...")
            await bot.close()
            await asyncio.sleep(5)
            await run_discord_bot()
        await asyncio.sleep(5)


async def send_live_ping():
    global live_status
    global user_was_live
    while True:
        try:
            channel = bot.get_channel(live_ping_channel)
            if live_status and not user_was_live:
                user_was_live = True
                print(f"User went live. live_status set to {live_status}")
                if channel:
                    await channel.send(f"{tiktok_channel} channel is now live! Watch here: https://www.tiktok.com/@{tiktok_channel}/live\n\n@everyone")
                else:
                    print("Channel not found!")
            elif not live_status and user_was_live:
                user_was_live = False
                print(f"{tiktok_channel} is not live")
        except ConnectionResetError:
            print("ConnectionResetError: Cannot write to closing transport. Setting live_status to False.")
            live_status = False
        await asyncio.sleep(2)



async def main():
    await asyncio.gather(
        run_tiktok_client(),
        run_discord_bot(),
        process_log_queue(),
        send_live_ping(), 
        rotate_status()  
    )


if __name__ == '__main__':
    asyncio.run(main()) 
