# reaction watchdog v1.0
# a suuuper simple/lazy discord bot for 
# watching and listing reaction events 
# on messages sent on a server.
#
# requires discord.py!
# install with "pip install discord".
#
# dont forget to set your bot token!
#
# by kerochan/thiccboye808

# commands:
# post [channel name] [message]
#   posts a message to a channel and
#   watches its reactions.
# watch [message id]
#   watches message thats been posted.
#   (not needed for messages posted by
#   the post command)
# stop [message id]
#   stops watching a message thats been posted and
#   deletes the logs.
#   it is highly recommended to do this after you
#   are done watching a message.
# log [message id] [(optional)modifiers]
#   outputs a log of reactions on a message
#   thats being watched. 
#   modifiers:
#     force-mention or fm: overrides mention settings on the log
#     include-removed or ir: includes removed reactions in the log

from datetime import datetime
import discord

TOKEN = "add your bot token here" # super secret bot token
PRINT_LEVEL = 3 # 0 = no console print, 1 = only errors, 2 = everything but parse, 3 = all 
REPLY_LEVEL = 2 # 0 = no messages, 1 = only logs, 2 = all messages
COMMAND = "~" # command prefix
MENTION_USERS = False
ROLE_NAME = "watchdog master" # not case sensitive (change this to whatever role u want)
TIME_FORMAT = "%H:%M:%S"
CLEANUP_TIME = 0 #  lifetime of reaction logs, gets deleted after this long

message_ids = []
reactions = []

if PRINT_LEVEL > 0:
  print( "reaction watchdog v1.0" )
client = discord.Client()

@client.event
async def on_ready():
  if PRINT_LEVEL > 1:
    print( f"{datetime.now()}: client connected as {client.user}" )

@client.event
async def on_message( message ):
  if message.author == client.user:
    return
  if ROLE_NAME not in [ role.name.lower() for role in message.author.roles ]:
    return
  if PRINT_LEVEL > 2:
    print( f"{datetime.now()}: parsing message {message.id} from {message.author}: {message.content}" )
  split = message.content.split()
  if message.content.startswith( f"{COMMAND}post" ):
    if len( split ) < 3:
      if PRINT_LEVEL > 0:
        print( f"{datetime.now()}: error! not enough arguments for post!" )
      if REPLY_LEVEL > 1:
        await message.reply( f"usage: `{COMMAND}post [channel name] [message]`" )
    else:
      if split[ 1 ][ 0:2 ] == "<#":
        print( split[ 1 ][ 2:-1 ] )
        message_channel = discord.utils.get( message.guild.text_channels, id=int( split[ 1 ][ 2:-1 ] ) )
      else:  
        message_channel = discord.utils.get( message.guild.text_channels, name=split[ 1 ] )
      if message_channel == None:
        if PRINT_LEVEL > 0:
          print( f"{datetime.now()}: error! couldn't find channel!" )
        if REPLY_LEVEL > 1:
          await message.reply( f"couldnt find channel {split[ 1 ]}..." )
      else:
        message_content = ' '.join( split[ 2: ] )
        if PRINT_LEVEL > 1:
          print( f"{datetime.now()}: posting message in {split[ 1 ]}: {message_content}" )
        message_id = await message_channel.send( message_content )
        message_id = message_id.id
        message_ids.append( message_id )
        if REPLY_LEVEL > 1:
          await message.reply( f"posted message with id {message_id}" )
  elif message.content.startswith( f"{COMMAND}watch" ):
    if len( split ) < 2:
      if PRINT_LEVEL > 0:
        print( f"{datetime.now()}: error! not enough arguments for watch!" )
      if REPLY_LEVEL > 1:
        await message.reply( f"usage: `{COMMAND}watch [message id]`" )
    else:
      try:
        message_id = int( message.content.split()[ 1 ] )
      except ValueError:
        if PRINT_LEVEL > 0:
          print( f"{datetime.now()}: error! {message.content.split()[ 1 ]} is not a message id!" )
        if REPLY_LEVEL > 1:
          await message.reply( f"{message.content.split()[ 1 ]} is not a message id..." )
      else:
        message_ids.append( message_id )
        if PRINT_LEVEL > 1:
          print( f"{datetime.now()}: watching reactions on message {message_id}..." )
        if REPLY_LEVEL > 1:
          await message.reply( f"watching reations on message {message_id}!" )
  elif message.content.startswith( f"{COMMAND}stop" ):
    if len( split ) < 2:
      if PRINT_LEVEL > 0:
        print( f"{datetime.now()}: error! not enough arguments for stop!" )
      if REPLY_LEVEL > 1:
        await message.reply( f"usage: `{COMMAND}stop [message id]`" )
    else:
      try:
        message_id = int( message.content.split()[ 1 ] )
      except ValueError:
        if PRINT_LEVEL > 0:
          print( f"{datetime.now()}: error! {message.content.split()[ 1 ]} is not a message id!" )
        if REPLY_LEVEL > 1:
          await message.reply( f"{message.content.split()[ 1 ]} is not a message id..." )
      else:
        message_ids.remove( message_id )
        for reaction in reactions:
          if reaction.message == message_id:
            reactions.remove( reaction )
        if PRINT_LEVEL > 1:
          print( f"{datetime.now()}: stopped watching reactions on message {message_id}..." )
        if REPLY_LEVEL > 1:
          await message.reply( f"stopped watching reations on message {message_id}!" )
  elif message.content.startswith( f"{COMMAND}log" ):
    if len( split ) < 2:
      if PRINT_LEVEL > 0:
        print( f"{datetime.now()}: error! not enough arguments for log!" )
      if REPLY_LEVEL > 1:
        await message.reply( f"usage: `{COMMAND}log [message id] [(optional)modifiers]`" )
    else:
      order = 0
      reply = ""
      try:
        message_id = int( split[ 1 ] )
      except ValueError:
        if PRINT_LEVEL > 0:
          print( f"{datetime.now()}: error! {message.content.split()[ 1 ]} is not a message id!" )
        if REPLY_LEVEL > 1:
          await message.reply( f"{message.content.split()[ 1 ]} is not a message id..." )
      else:
        if len( split ) > 2:
          modifiers = split[ 2: ]
        else:
          modifiers = ""
        fm = False
        ir = False
        for modifier in modifiers:
          if modifier == "force-mention" or modifier == "fm":
            fm = True
          if modifier == "include-removed" or modifier == "ir":
            ir = True
        if PRINT_LEVEL > 1:
          print( f"{datetime.now()}: outputing log on message {message_id}..." )
        for i in reactions:
          if i[ "message" ] == message_id:
            if i[ "removed" ] == 0 or ir:
              order += 1
              if MENTION_USERS or fm:
                user = message.author.mention
              else:
                user = message.author
              time = i[ "time" ].time()
              if REPLY_LEVEL > 0:
                if order > 1:
                  reply += "\n"
                reply += f"#{order}: {user} at {time.strftime( TIME_FORMAT )} {i[ 'emoji' ]}"
        if order == 0:
          if REPLY_LEVEL > 0:
            reply = f"no reactions logged for message {message_id}!"
        await message.reply( reply )

@client.event
async def on_raw_reaction_add( event ):
  user = await client.fetch_user( event.user_id )
  if event.message_id in message_ids:
    reactions.append( { "message": event.message_id, "time": datetime.now(), "userid": event.user_id, "emoji": event.emoji, "removed": 0 } )
    if PRINT_LEVEL > 1:
      print( f"{datetime.now()}: {user} reacted with: {event.emoji.name}" )

@client.event
async def on_raw_reaction_remove( event ):
  user = await client.fetch_user( event.user_id )
  if event.message_id in message_ids:
    for i in reactions:
      if i[ "userid" ] == event.user_id and i[ "emoji" ] == event.emoji:
        i[ "removed" ] = 1
    if PRINT_LEVEL > 1:
      print( f"{datetime.now()}: {user} removed reaction: {event.emoji.name}" )

client.run( TOKEN )