#!/usr/bin/python3
import discord, copy, asyncio, pickle, time, datetime
import c6embed, settings
from discord.ext.commands import Bot
global posts, raidIDs, raidDict, bot
raidFile='data/raids.pkl'
sttngs=settings.Settings()
teamSizes={
            'leviathan':6,
            'nightfall':3, 
            'crucible':4, 
            'borderlands2':4
            }
data={
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
    global bot, posts, raidIDs, raidDict, reactEmoji
    readF=pickleReader(raidFile)
    bot=await c6.get_user_info('326270253384597505')
    if readF:
        print('pickle found, loading.')
        raidDict=readF
        reactEmoji=setEmojiStack(raidDict['server'])
        posts=list()
        raidIDs=list()
        for raid in raidDict['raids']:
            if raid['complete']==False:
                print(raid)
                msg=raid['message'].id
                print(msg)
                message=await c6.get_message(raid['message'].channel, id=raid['message'].id)                
                c6.messages.append(message)
                posts.append(raid['message'].id)
                raidIDs.append(raid['raidID'])
                await getOfflineReactions(raid)
            else:
                print('skipping completed raid')
        print('%i raids loaded from pickle.' % len(posts))
    else:
        print('no pickle file detected!')
        raidDict={
            'server':discord.utils.get(c6.servers, id='223519936935362561'), 
            'index':0,
            'raids':list()
            }
        reactEmoji=setEmojiStack(raidDict['server'])
        posts=[]
        raidIDs=[]
@c6.command(pass_context=True)
async def crucible(msg, sTime=0):
    global raidDict, posts, raidIDs
    message=msg.message
    botUser=discord.utils.get(message.server.members, id='326270253384597505')
    raidData=copy.deepcopy(data)
    if isinstance(sTime, int):
        offset=sTime*60
        start=time.time()+offset
        raidData['start']=start
    raidData['channel']=message.channel
    raidData['bot']=botUser
    raidData['leader']=message.author
    raidID='crucible%i' % raidDict['index']
    raidDict['index']=raidDict['index']+1
    raidData['raidID']=raidID
    raidData['type']='crucible'
    raidData['game']='destiny'
    raidData['teamSize']=teamSizes[raidData['type']]
    raidData['message']=await createAdv(raidData)
    print(raidData['message'].id) 
    raidDict['raids'].append(raidData)
    posts.append(raidData['message'].id)
    raidIDs.append(raidData['raidID'])
    pickleWriter(raidFile, raidDict)
@c6.command(pass_context=True)
async def borderlands2(msg, sTime=0):
    global raidDict, posts, raidIDs
    message=msg.message
    botUser=discord.utils.get(message.server.members, id='326270253384597505')
    raidData=copy.deepcopy(data)
    if isinstance(sTime, int):
        offset=sTime*60
        start=time.time()+offset
        raidData['start']=start
    raidData['channel']=message.channel
    raidData['bot']=botUser
    raidData['leader']=message.author
    raidID='borderlands2%i' % raidDict['index']
    raidDict['index']=raidDict['index']+1
    raidData['raidID']=raidID
    raidData['type']='borderlands2'
    raidData['game']='borderlands2'
    raidData['teamSize']=teamSizes[raidData['type']]
    raidData['message']=await createAdv(raidData)
    print(raidData['message'].id) 
    raidDict['raids'].append(raidData)
    posts.append(raidData['message'].id)
    raidIDs.append(raidData['raidID'])
    pickleWriter(raidFile, raidDict)
@c6.command(pass_context=True)
async def nightfall(msg, sTime=0):
    global raidDict, posts, raidIDs
    message=msg.message
    botUser=discord.utils.get(message.server.members, id='326270253384597505')
    raidData=copy.deepcopy(data)
    if isinstance(sTime, int):
        offset=sTime*60
        start=time.time()+offset
        raidData['start']=start
    raidData['channel']=message.channel
    raidData['bot']=botUser
    raidData['leader']=message.author
    raidID='nightfall%i' % raidDict['index']
    raidDict['index']=raidDict['index']+1
    raidData['raidID']=raidID
    raidData['type']='nightfall'
    raidData['game']='destiny'
    raidData['teamSize']=teamSizes[raidData['type']]
    raidData['message']=await createAdv(raidData)
    print(raidData['message'].id) 
    raidDict['raids'].append(raidData)
    posts.append(raidData['message'].id)
    raidIDs.append(raidData['raidID'])
    pickleWriter(raidFile, raidDict)
@c6.command(pass_context=True)
async def raid(msg, sTime=0):
    global raidDict, posts, raidIDs
    message=msg.message
    botUser=discord.utils.get(message.server.members, id='326270253384597505')
    raidData=copy.deepcopy(data)
    if isinstance(sTime, int):
        offset=sTime*60
        start=time.time()+offset
        raidData['start']=start
    raidData['channel']=message.channel
    raidData['bot']=botUser
    raidData['leader']=message.author
    raidID='leviathan%i' % raidDict['index']
    raidDict['index']=raidDict['index']+1
    raidData['raidID']=raidID
    raidData['type']='leviathan'
    raidData['game']='destiny'
    raidData['teamSize']=teamSizes[raidData['type']]
    raidData['message']=await createAdv(raidData)
    print(raidData['message'].id) 
    raidDict['raids'].append(raidData)
    posts.append(raidData['message'].id)
    raidIDs.append(raidData['raidID'])
    pickleWriter(raidFile, raidDict)
async def remind(raid): 
    await c6.send_typing(raid['channel'])
    await asyncio.sleep(5)
    reminderString="%s event reminder! players: " % raid['type']
    for playerTuple in raid['players']:
        reminderString=reminderString+'%s, ' % playerTuple[0].mention
    start=datetime.datetime.fromtimestamp(raid['start']).strftime('%I:%m%p %a')
    reminderString=reminderString+'Leader:%s starting at %s.' % (raid['leader'].mention, start)
    await c6.send_message(raid['channel'], reminderString)
@c6.command(pass_context=True)
async def show(msg, sub=None):
    if sub!=None: 
        if sub in raidIDs:
            for raid in raidDict['raids']:
                if raid['raidID']==sub:
                    await updateRaid(raid)
        elif sub=='board':
            await c6.send_typing(msg.message.channel)
            await asyncio.sleep(3)
            raidList=list()
            for raid in raidDict['raids']: 
                if raid['channel']==msg.message.channel: 
                    raidList.append(raid)
            if len(raidList)>0: 
                card=c6embed.createBoardEmbed(raidList)
                await c6.send_message(msg.message.channel, '', embed=card)
            else:
                c6.say('No raids found for this channel! Create one with ^newRaid!')
        elif sub=='mine':
            await c6.send_typing(msg.message.channel)
            await asyncio.sleep(5)
            raidList=list()
            for raid in raidDict['raids']: 
                if (raid['channel']==msg.message.channel):
                    if (raid['leader']==msg.message.author): 
                        raidList.append(raid)
                    else:
                        for playerTuple in raid['players']:
                            if playerTuple[0]==msg.message.author: 
                                raidList.append(raid)
            if len(raidList)>0: 
                card=c6embed.createBoardEmbed(raidList)
                await c6.send_message(msg.message.channel, '', embed=card)
            else:
                c6.say("You don't seem to be involved in any raids from this channel! Create one with ^newRaid!")
        elif sub=='soon':
            await c6.send_typing(msg.message.channel)
            await asyncio.sleep(3)
            raidList=list()
            for raid in raidDict['raids']: 
                now=time.time()
                if (raid['channel']==msg.message.channel): 
                    if (raid['start'] is not None):
                        if (raid['start']>now) and ((int(raid['start'])-int(now))<=1800):
                            raidList.append(raid)
            if len(raidList)>=1: 
                card=c6embed.createBoardEmbed(raidList)
                await c6.send_message(msg.message.channel, '', embed=card)
            else:
                c6.say("No raids starting within 15 minutes for this channel! Create one with ^newRaid!")
        elif sub=='vacancy':
            await c6.send_typing(msg.message.channel)
            await asyncio.sleep(2)
            raidList=list()
            for raid in raidDict['raids']: 
                if (len(raid['players']) < 6) and (raid['channel']==msg.message.channel):
                    raidList.append(raid)
            if len(raidList)>0: 
                card=c6embed.createBoardEmbed(raidList)
                await c6.send_message(msg.message.channel, '', embed=card)
            else:
                c6.say("No raids with vacant spots in this channel! Create a new one with ^newRaid!")
    else:
        for raid in raidDict['raids']:
            if (raid['complete'] == False) and (raid['channel']==msg.message.channel): 
                await updateRaid(raid)
async def createAdv(data):
    for emoji in reactEmoji[data['game']]:
        print(emoji)
    channel=data['channel']
    if data['complete']:
        card=c6embed.closeRaidEmbed(data)
    else:
        card=c6embed.createAdvEmbed(data)
    raidPost=await c6.send_message(channel, '', embed=card)
    print("id inside createPost: %s" % raidPost.id)
    if data['complete']:
        return raidPost
    else:
        print((data['start']-time.time()))
        for emoji in reactEmoji[data['game']]:
            await c6.add_reaction(raidPost, emoji)
        if ((data['start']-time.time())>=0) and ((data['start']-time.time())<1800):
            for emoji in reactEmoji['util']:
                await c6.add_reaction(raidPost, emoji)                
    return raidPost
async def updateRaid(data):
    global posts, raidDict
    posts.remove(data['message'].id)
    await c6.delete_message(data['message'])
    data['message']=await createAdv(data)
    if data['complete'] == True:
        raidDict['raids'].remove(data)
        await asyncio.sleep(30)
        await c6.delete_message(data['message'])
    else:
        posts.append(data['message'].id)
    pickleWriter(raidFile, raidDict)
@c6.event
async def on_reaction_add(reaction, user):
    global posts
    data=None
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
            for raid in raidDict['raids']:
                if raid['message'].id==reaction.message.id:
                    update=await parseReaction(emoji, member, raid)
                    if (update!=None) and (update):
                        await updateRaid(update)
async def getOfflineReactions(raid):
    reactObj=list()
    for emoji in reactEmoji[raid['game']]:
        reaction=discord.Reaction(message=raid['message'], emoji=emoji)
        reactObj.append(reaction)
    print('getting offline reactions for %s' % raid['raidID'])
    update=None
    for reaction in reactObj:
        print("parsing %s reactions" % reaction.emoji.name)
        users=await c6.get_reaction_users(reaction, limit=100)
        for user in users:
            if user != raid['bot']:
                print('parsing %s reaction from %s on raid post %s' 
                      % (reaction.emoji.name, user.name, raid['raidID']))
                member=reaction.message.server.get_member(user.id)
                emoji=reaction.emoji
                message=reaction.message
                await c6.remove_reaction(message=message, emoji=emoji, member=member)
                if update!=False:
                    print('297')
                    old=copy.deepcopy(update)
                    update=await parseReaction(emoji, member, raid)
                    if update==None: 
                        update=old
            else: 
                print('ignoring self-reaction')
    if update and (update != None):
        await updateRaid(update)
async def parseReaction(emoji, member, data):
#    if  emoji.name in reactEmojis.keys():
    if emoji.name=='brooksphone':
        await remind(data)
    if emoji in reactEmoji[data['game']]:
        print('%s icon in recognized reaction emoji' % emoji.name)
        if (emoji.name =='darkness') or (emoji.name=='cl4ptp'):
            if data['leader'].id==member.id:
                print('member is raid leader')
                data['complete']=True
                if len(data['players'])>=1:
                    await updateRaid(data)
                else:
                    await c6.delete_message(data['message'])
                print('raid lost in the dark corners of time')
                return False
            else:
                return None 
        else:
            userTuple=(member, emoji)
            print(len(data['players'])-1)    
            if userTuple in data['players']:
                print('removing %s: %s from raid' % (userTuple[0].name, userTuple[1].name))
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
                print('adding %s: %s to raid' % (userTuple[0].name, userTuple[1].name))
                data['players'].append(userTuple)
                return data
    else:
        return None
token=sttngs['token']
print(token)
c6.run(token)
