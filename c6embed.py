#!/usr/bin/python3
import discord, time, datetime
from discord import Embed, Color

def getPlayerFromID(server, playerID):
    player=discord.utils.get(server.members, id=playerID)
    return player

def createRaidEmbed(data):
    rCard=Embed()
    rCard.set_author(name=data['bot'].name, icon_url=data['bot'].avatar_url)
    rCard.title='-=<Leviathan Raid>=-'
    rCard.url='http://google.com'
    rCard.type='rich'
    rCard.color=Color.dark_grey()
    rCard.set_image(url='https://s3-us-west-2.amazonaws.com/cayde-6/leviathan.png')
    i=1
    for player in data['players']:
        rCard.add_field(name='Spot %i:' % i, value=player.mention)
        i=i+1
    while i <= data['teamSize']: 
        rCard.add_field(name='Spot %i:' % i, value='Empty' )
        i=i+1
    if data['start'] is not None: 
        rCard.add_field(name='Start Time:', value="%s Pacific" % time.ctime(data['start']))
    rCard.set_footer(text='raid leader: %s raid id: %s' % (data['leader'].name, data['raidID']))
    return rCard
def createAdvEmbed(data):
    rCard=Embed()
    rCard.set_author(name=data['bot'].name, icon_url=data['bot'].avatar_url)
    rCard.title='-=<%s>=-' % data['type']
    rCard.url='http://google.com'
    rCard.type='rich'
    rCard.color=Color.dark_grey()
    rCard.set_image(url='https://s3-us-west-2.amazonaws.com/cayde-6/%s.png' % data['type'])
#    elif data['type']=='crucible':
#        rCard.set_image(url='https://s3-us-west-2.amazonaws.com/cayde-6/crucible.png')
#    elif data['type']=='nightfall':
#       rCard.set_image(url='https://s3-us-west-2.amazonaws.com/cayde-6/nightfall.png')
    i=1
    for playerTuple in data['players']:
        rCard.add_field(name='Spot %i:' % i, value="%s (%s)" % (playerTuple[0].name, playerTuple[1]))
        i=i+1
    while i <= data['teamSize']: 
        rCard.add_field(name='Spot %i:' % i, value='Empty' )
        i=i+1
    if data['start'] is not None: 
        rCard.add_field(name='Start Time:', value="%s Pacific" % time.ctime(data['start']))
    rCard.set_footer(text='raid leader: %s raid id: %s' % (data['leader'].name, data['raidID']))
    return rCard  
def closeRaidEmbed(data):
    rCard=Embed()
    rCard.set_author(name=data['bot'].name, icon_url=data['bot'].avatar_url)
    rCard.title='-=<Raid Complete!>=-'
    rCard.url='http://google.com'
    rCard.type='rich'
    rCard.color=Color.dark_blue()
    rCard.set_image(url='https://s3-us-west-2.amazonaws.com/cayde-6/leviathan.png')
    i=1
    for playerTuple in data['players']:
        rCard.add_field(name='Spot %i' % i, value="%s (%s)" % (playerTuple[0].name, playerTuple[1]))
        i=i+1
    while i <= data['teamSize']: 
        rCard.add_field(name='Spot %i' % i, value='Empty' )
        i=i+1
    if data['start'] is not None: 
        rCard.add_field(name='Started at:', value="%s Pacific" % time.ctime(data['start']))
    rCard.add_field(name='Ended at:', value="%s Pacific" % time.ctime())
    rCard.set_footer(text='raid leader: %s raid id: %s' % (data['leader'].name, data['raidID']))
    return rCard
def createBoardEmbed(raids):
    rCard=Embed()
    rCard.set_author(name=raids[0]['bot'].name, icon_url=raids[0]['bot'].avatar_url)
    rCard.title='-=<%s events!>=-' % raids[0]['channel'].name
    rCard.url='http://google.com'
    rCard.type='rich'
    rCard.color=Color.purple()
    rCard.set_image(url='https://s3-us-west-2.amazonaws.com/cayde-6/boardImage.png')
    embedText=''
    for raid in raids:
        if (raid['start'] == None) or (int(raid['start']) < int(time.time())): 
            start='Started!'
        else:
            start=datetime.datetime.fromtimestamp(raid['start']).strftime('%I:%m%p %a')
        raidLine="%s leader: %s players: %i/%i starts: %s" % (raid['raidID'], raid['leader'].name, 
                                                              len(raid['players']), raid['teamSize'], start)
        embedText='%s\n%s' % (embedText, raidLine)
    rCard.add_field(name='board:', value=embedText)
    rCard.set_footer(text='caydeRaid© 2017 alex&theΩ')
    return rCard
