#!/usr/bin/python3
import discord, copy, asyncio, pickle, time, datetime
import c6embed, settings
from discord.ext.commands import Bot
global posts, eventIDs, eventDict, bot
eventFile='data/events.pkl'
sttngs=settings.Settings()
teamSizes={
            'leviathan':6,
            'nightfall':3, 
            'crucible':4, 
            'borderlands2':4
            }
Data={
        'message':None,
        'leader':None, 
        'bot':None, 
        'start':None, 
        'end':None,
        'channel':None, 
        'complete':False,
        'players':[],
        'type':None,
        'teamSize':6
    }
def setEmojiStack(server):
    global emojiStack
    emojiStack=dict()
    emojiStack['destiny']=list()
    for name in ['warlock', 'titan', 'hunter', 'darkness']:
        emojiStack['destiny'].append(discord.utils.get(server.emojis, name=name))
    emojiStack['borderlands2']=list()
    for name in ['maya', 'salvador', 'z3r0', 'axton', 'gaige', 'krieg', 'cl4ptp']:
        emojiStack['borderlands2'].append(discord.utils.get(server.emojis, name=name))
    emojiStack['util']=list()
    for name in ['brooksphone']:
        emojiStack['util'].append(discord.utils.get(server.emojis, name=name))
    return emojiStack
def pickleReader(filename):
    try:
        with open(filename, 'rb') as pickleFile:
            newObject=pickle.load(pickleFile)
            return newObject
    except:
        print('no pickle to read!')
        return False
def pickleWriter(filename, Obj):
    with open(filename, 'wb') as pickleFile: 
        try:
            pickle.dump(Obj, pickleFile)
            pickleFile.close()
            return True
        except: 
            print('write to file failed!')
            return False
c6=Bot(command_prefix='^')
@c6.event
async def on_ready():
    global bot, posts, eventIDs, eventDict, reactEmoji
    readF=pickleReader(eventFile)
    bot=await c6.get_user_info('326270253384597505')
    if readF:
        print('pickle found, loading.')
        eventDict=readF
        reactEmoji=setEmojiStack(eventDict['server'])
        posts=list()
        eventIDs=list()
        for event in eventDict['events']:
            if event['complete']==False:
                msg=event['message'].id
                message=await c6.get_message(event['message'].channel, id=event['message'].id)                
                c6.messages.append(message)
                posts.append(event['message'].id)
                eventIDs.append(event['eventID'])
                await getOfflineReactions(event)
            else:
                print('skipping completed event')
        print('%i events loaded from pickle.' % len(posts))
    else:
        print('no pickle file detected!')
        eventDict={
            'server':discord.utils.get(c6.servers, id='223519936935362561'), 
            'index':0,
            'events':list()
            }
        reactEmoji=setEmojiStack(eventDict['server'])
        posts=[]
        eventIDs=[]
@c6.command(pass_context=True)
async def crucible(msg, sTime=0):
    message=msg.message
    game='destiny'
    Type='crucible'
    if isinstance(sTime, int):
        offset=sTime*60
        start=time.time()+offset
    await makeEvent(message, start, Type, game)
@c6.command(pass_context=True)
async def borderlands2(msg, sTime=0):
    message=msg.message
    game='borderlands2'
    Type='borderlands2'
    if isinstance(sTime, int):
        offset=sTime*60
        start=time.time()+offset
    await makeEvent(message, start, Type, game)
@c6.command(pass_context=True)
async def nightfall(msg, sTime=0):
    message=msg.message
    game='destiny'
    Type='nightfall'
    if isinstance(sTime, int):
        offset=sTime*60
        start=time.time()+offset
    await makeEvent(message, start, Type, game)
@c6.command(pass_context=True)
async def event(msg, sTime=0):
    message=msg.message
    game='destiny'
    Type='leviathan'
    if isinstance(sTime, int):
        offset=sTime*60
        start=time.time()+offset
    await makeEvent(message, start, Type, game)
async def makeEvent(message, start, Type, game):
    global eventDict, posts, eventIDs
    data=copy.deepcopy(Data)
    botUser=discord.utils.get(message.server.members, id='326270253384597505')
    data['start']=start
    data['channel']=message.channel
    data['bot']=botUser
    data['leader']=message.author
    eventID='%s%s%i' % (Type[0], game[0], eventDict['index'])
    eventDict['index']=eventDict['index']+1
    data['eventID']=eventID
    data['type']=Type
    data['game']=game
    data['teamSize']=teamSizes[data['type']]
    data['message']=await createAdv(data)
    print(data['message'].id) 
    eventDict['events'].append(data)
    posts.append(data['message'].id)
    eventIDs.append(data['eventID'])
    pickleWriter(eventFile, eventDict)
async def remind(event): 
    if (len(event['players'])>0) and ((event['start']-time.time())>0):
        await c6.send_typing(event['channel'])
        await asyncio.sleep(5)
        reminderString="%s event reminder! players: " % event['type']
        for playerTuple in event['players']:
            reminderString=reminderString+'%s, ' % playerTuple[0].mention
        start=datetime.datetime.fromtimestamp(event['start']).strftime('%I:%m%p %a')
        reminderString=reminderString+'Leader:%s starting at %s.' % (event['leader'].mention, start)
        await c6.send_message(event['channel'], reminderString)
@c6.command(pass_context=True)
async def show(msg, sub=None):
    if sub!=None: 
        if sub in eventIDs:
            for event in eventDict['events']:
                if event['eventID']==sub:
                    await updateEvent(event)
        elif sub=='board':
            await c6.send_typing(msg.message.channel)
            await asyncio.sleep(3)
            eventList=list()
            for event in eventDict['events']: 
                if event['channel']==msg.message.channel: 
                    eventList.append(event)
            if len(eventList)>0: 
                card=c6embed.createBoardEmbed(eventList)
                await c6.send_message(msg.message.channel, '', embed=card)
            else:
                c6.say('No events found for this channel! Create one with ^newRaid!')
        elif sub=='mine':
            await c6.send_typing(msg.message.channel)
            await asyncio.sleep(5)
            eventList=list()
            for event in eventDict['events']: 
                if (event['channel']==msg.message.channel):
                    if (event['leader']==msg.message.author): 
                        eventList.append(event)
                    else:
                        for playerTuple in event['players']:
                            if playerTuple[0]==msg.message.author: 
                                eventList.append(event)
            if len(eventList)>0: 
                card=c6embed.createBoardEmbed(eventList)
                await c6.send_message(msg.message.channel, '', embed=card)
            else:
                c6.say("You don't seem to be involved in any events from this channel! Create one with ^newRaid!")
        elif sub=='soon':
            await c6.send_typing(msg.message.channel)
            await asyncio.sleep(3)
            eventList=list()
            for event in eventDict['events']: 
                now=time.time()
                if (event['channel']==msg.message.channel): 
                    if (event['start'] is not None):
                        if (event['start']>now) and ((int(event['start'])-int(now))<=1800):
                            eventList.append(event)
            if len(eventList)>=1: 
                card=c6embed.createBoardEmbed(eventList)
                await c6.send_message(msg.message.channel, '', embed=card)
            else:
                c6.say("No events starting within 15 minutes for this channel! Create one with ^newRaid!")
        elif sub=='vacancy':
            await c6.send_typing(msg.message.channel)
            await asyncio.sleep(2)
            eventList=list()
            for event in eventDict['events']: 
                if (len(event['players']) < 6) and (event['channel']==msg.message.channel):
                    eventList.append(event)
            if len(eventList)>0: 
                card=c6embed.createBoardEmbed(eventList)
                await c6.send_message(msg.message.channel, '', embed=card)
            else:
                c6.say("No events with vacant spots in this channel! Create a new one with ^newRaid!")
    else:
        for event in eventDict['events']:
            if (event['complete'] == False) and (event['channel']==msg.message.channel): 
                await updateEvent(event)
async def createAdv(data):
    for emoji in reactEmoji[data['game']]:
        print(emoji)
    channel=data['channel']
    if data['complete']:
        card=c6embed.closeEventEmbed(data)
    else:
        card=c6embed.createAdvEmbed(data)
    eventPost=await c6.send_message(channel, '', embed=card)
    print("id inside createPost: %s" % eventPost.id)
    if data['complete']:
        return eventPost
    else:
        for emoji in reactEmoji[data['game']]:
            await c6.add_reaction(eventPost, emoji)
        if ((data['start']-time.time())>=0) and ((data['start']-time.time())<1800):
            for emoji in reactEmoji['util']:
                await c6.add_reaction(eventPost, emoji)                
    return eventPost
async def updateEvent(data):
    global posts, eventDict
    posts.remove(data['message'].id)
    await c6.delete_message(data['message'])
    data['message']=await createAdv(data)
    if data['complete'] == True:
        eventDict['events'].remove(data)
        await asyncio.sleep(30)
        await c6.delete_message(data['message'])
    else:
        posts.append(data['message'].id)
    pickleWriter(eventFile, eventDict)
@c6.event
async def on_reaction_add(reaction, user):
    global posts
    if reaction.message.id in posts: 
        print(posts)
        member=reaction.message.server.get_member(user.id)
        emoji=reaction.emoji
        if user.id==bot.id: 
            print('ignoring self')
            return 
        else:
            print("member id inside on_reaction_add %s" %member.id )
            await c6.remove_reaction(message=reaction.message, emoji=reaction.emoji, member=member )
            update=None
            for event in eventDict['events']:
                if event['message'].id==reaction.message.id:
                    update=await parseReaction(emoji, member, event)
                    if (update!=None) and (update):
                        await updateEvent(update)
async def getOfflineReactions(event):
    reactObj=list()
    for emoji in reactEmoji[event['game']]:
        reaction=discord.Reaction(message=event['message'], emoji=emoji)
        reactObj.append(reaction)
    print('getting offline reactions for %s' % event['eventID'])
    update=None
    for reaction in reactObj:
        print("parsing %s reactions" % reaction.emoji.name)
        users=await c6.get_reaction_users(reaction, limit=100)
        for user in users:
            if user != event['bot']:
                print('parsing %s reaction from %s on event post %s' 
                      % (reaction.emoji.name, user.name, event['eventID']))
                member=reaction.message.server.get_member(user.id)
                emoji=reaction.emoji
                message=reaction.message
                await c6.remove_reaction(message=message, emoji=emoji, member=member)
                if update!=False:
                    old=copy.deepcopy(update)
                    update=await parseReaction(emoji, member, event)
                    if update==None: 
                        update=old
            else: 
                print('ignoring self-reaction')
    if update and (update != None):
        await updateEvent(update)
async def parseReaction(emoji, member, data):
    if emoji.name=='brooksphone':
        await remind(data)
    if emoji in reactEmoji[data['game']]:
        print('%s icon in recognized reaction emoji' % emoji.name)
        if (emoji.name =='darkness') or (emoji.name=='cl4ptp'):
            if data['leader'].id==member.id:
                print('member is event leader')
                data['complete']=True
                if len(data['players'])>=1:
                    await updateEvent(data)
                else:
                    await c6.delete_message(data['message'])
                print('event lost in the dark corners of time')
                return False
            else:
                return None 
        else:
            userTuple=(member, emoji)
            print(len(data['players'])-1)    
            if userTuple in data['players']:
                print('removing %s: %s from event' % (userTuple[0].name, userTuple[1].name))
                data['players'].remove(userTuple)
                return data
            if userTuple in data['players']:
                data['players'].remove(userTuple)
                return data
            for player in data['players']:
                if player[0]==userTuple[0]:
                    indx=data['players'].index(player)
                    data['players'][indx]=userTuple
                    return data
            if len(data['players'])<data['teamSize']:
                print('adding %s: %s to event' % (userTuple[0].name, userTuple[1].name))
                data['players'].append(userTuple)
                return data
    else:
        return None
token=sttngs['token']
print(token)
c6.run(token)
