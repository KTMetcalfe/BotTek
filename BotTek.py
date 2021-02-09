# Kian M (RedTek)
# 02/09/2021

# This is a simple bot designed for my discord servers just for fun.

import discord
import json
import time

client = discord.Client()

# Important global variable for the bot
filename_token = 'token.txt'
filename_members = 'member_data.json'
homo_words = ('penis', 'dick', 'cock', 'balls')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
# Does nothing if the message is from the bot itself
    if message.author == client.user:
        return

# Basic hello message and test point for the bot
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# Replies with an automated response when one of the (homo_words) are sent in a message
    if any(s in message.content for s in homo_words):
        await message.channel.send(f'{message.author.mention} No homo...')


# Provides an automated response to anyone who starts their message with "@complaint",
# also stores the complaint, minus "@complaint ", in the (filename_members) JSON file
    if message.content.startswith('@complaint'):
        member = message.author.name
        try:
            with open(filename_members, "r") as data_file:
                data_file.seek(0)
                json_data = json.load(data_file)
        except:
            print(f'{filename_members} does not exist or is inproperly formatted')
            data_string = f'{{"{member}": {{"complaints": []}}}}'
            print(f'New JSON: {data_string}')
            json_data = json.loads(data_string)

    # Checks for existence of (member) and "complaints" directories in the
    # (filename_members) JSON file before editing and writing to the file
        if f'{member}' not in json_data:
            json_data[f'{member}'] = {}
            json_data[f'{member}']['complaints'] = []
        elif 'complaints' not in json_data[f'{member}']:
            json_data[f'{member}']['complaints'] = []

        json_data[member]['complaints'].append(message.content.replace('@complaint ', ''))

        with open(filename_members, 'w') as data_file:
            json.dump(json_data, data_file, indent = 4)

    # Waits before sending message for dramatic effect
        time.sleep(5)
        await message.channel.send(f'{message.author.mention} We are proccessing your feedback and will work swiftly to resolve your issue. We appreciate your patience.')

# Provides an automated response to anyone who starts their message with "@complaint",
# also stores the complaint, minus "@legal ", in the (filename_members) JSON file
    if message.content.startswith('@legal'):
        member = message.author.name
        try:
            with open(filename_members, "r") as data_file:
                data_file.seek(0)
                json_data = json.load(data_file)
        except:
            print(f'{filename_members} does not exist or is inproperly formatted')
            data_string = f'{{"{member}": {{"legal_issues": []}}}}'
            print(f'New JSON: {data_string}')
            json_data = json.loads(data_string)

    # Checks for existence of (member) and "legal_issues" directories in the
    # (filename_members) JSON file before editing and writing to the file
        if f'{member}' not in json_data:
            json_data[f'{member}'] = {}
            json_data[f'{member}']['legal_issues'] = []
        elif 'legal_issues' not in json_data[f'{member}']:
            json_data[f'{member}']['legal_issues'] = []

        json_data[member]['legal_issues'].append(message.content.replace('@legal ', ''))

        with open(filename_members, 'w') as data_file:
            json.dump(json_data, data_file, indent = 4)

    # Waits before sending message for dramatic effect
        time.sleep(5)
        await message.channel.send(f'{message.author.mention} You have the right to remain silent. Anything you say can and will be used against you in a court of law. You have the right to an attorney. If you cannot afford an attorney, one will be provided for you.')

@client.event
async def on_message_edit(messageOld, messageNew):
# Counts the amount of times a member edits one of thier messages and adds it to
# the (filename_members) JSON file
    if messageOld.content != messageNew.content:
        member = messageNew.author.name
        try:
            with open(filename_members, 'r') as data_file:
                data_file.seek(0)
                json_data = json.load(data_file)
        except:
            print(f'{filename_members} does not exist or is inproperly formatted')
            data_string = f'{{"{member}": {{"edit_count": 0}}}}'
            print(f'New JSON: {data_string}')
            json_data = json.loads(data_string)

    # Checks for existence of (member) and "edit_count" directories in the
    # (filename_members) JSON file before editing and writing to the file
        if f'{member}' not in json_data:
            json_data[f'{member}'] = {}
            json_data[f'{member}']['edit_count'] = 1
        elif 'edit_count' not in json_data[f'{member}']:
            json_data[f'{member}']['edit_count'] = 1
        else:
            json_data[member]['edit_count'] += 1

        with open(filename_members, 'w') as data_file:
            json.dump(json_data, data_file, indent = 4)

@client.event
async def on_member_join(member):
    guild = member.guild
# Send a welcoming message anytime someone joins the server
    if guild.system_channel is not None:
        to_send = 'Welcome {0.mention} to {1.name}! I hope you enjoy your stay more than I do!'.format(member, guild)
        await guild.system_channel.send(to_send)

with open(filename_token) as token:
    client.run(token.read())
