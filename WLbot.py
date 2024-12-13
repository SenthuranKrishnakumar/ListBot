import discord
from discord.ext import commands
# -----------------------------------------------------------------------------------------------------------------------------------------------
import pymongo
from pymongo import MongoClient
import urllib
import urllib.request
# -----------------------------------------------------------------------------------------------------------------------------------------------
import ast
import asyncio
import random
from discord.utils import find
# -----------------------------------------------------------------------------------------------------------------------------------------------
client = commands.Bot(command_prefix='.')
mongoPath = "mongodb+srv://senthu:"
mongoHostPath = "@watchlistbot.ssjho.mongodb.net/"
mongoHostEnd = "?retryWrites=true&w=majority"
mongo_url = mongoPath + urllib.parse.quote_plus(
    "Caesar@2017") + mongoHostPath + urllib.parse.quote_plus("database") + mongoHostEnd
cluster = MongoClient(mongo_url)
db = cluster["database"]
collection = db["new"]
# -----------------------------------------------------------------------------------------------------------------------------------------------
emptyArr = []
textPrefix = "list"
embedname = "The List creator" 
embedTick = "https://i.imgur.com/FiyWumV.png"
embedCross = "https://i.imgur.com/w1ChmUP.png"


# -----------------------------------------------------------------------------------------------------------------------------------------------
def on_check_init(ctx):
    id = str(ctx.author.id)
    results = collection.find({"_id": {'$exists': id}})
    check = False
    for x in results:
        SubstringX = str(x)
        Modified = SubstringX[9:27]
        if Modified == id:
            check = True
    return check
def on_user_not_exist(target, ctx):
    embed = discord.Embed(
        title=target + ' does not exist in my database!',
        description='You have not initialized an account, type in **.initialize** to do so!',
        colour=discord.colour.Color.red()
    )
    embedWrong(ctx, embed)
    return embed
def get_author_name(ctx):
    target = str(ctx.author)
    target = target[:-5]
    return target
def get_author_id(ctx):
    return str(ctx.author.id)
def wronglist(listname, ctx):
    embed = discord.Embed(
        title="There are no lists with that name" + "\n" + "For user: " + get_author_name(ctx),
        description='You can type in **.' + textPrefix +
        'created** to see what lists you currently have created',
        colour=discord.colour.Color.red()
        )
    embedWrong(ctx, embed)
    return embed
def embedRight(ctx, embed):
    embed.set_footer(text = "Bot created by Senthu")
    embed.set_thumbnail(url = ctx.author.avatar_url) 
    embed.set_author(name=embedname, icon_url=embedTick)
def embedWrong(ctx, embed):
    embed.set_footer(text = "Bot created by Senthu")
    embed.set_thumbnail(url = ctx.author.avatar_url) 
    embed.set_author(name=embedname, icon_url=embedCross)
def argumentError(ctx,embed):
    embed.set_footer(text = "Bot created by Senthu")
    embed.set_thumbnail(url = "https://i.imgur.com/dXNs9qI.png") 
    embed.set_author(name=embedname, icon_url=embedCross)
# -----------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=".listhelp" + " - " + str(len(client.guilds)) + " Servers"))
    print('Ready')

# -----------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_commmand_error(ctx, error):
    pass
# -----------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_guild_remove(guild):
    await client.change_presence(activity=discord.Game(name=".listhelp" + " - " + str(len(client.guilds)) + " Servers"))

@client.event
async def on_guild_join(guild):
    await client.change_presence(activity=discord.Game(name=".listhelp" + " - " + str(len(client.guilds)) + " Servers"))

# -----------------------------------------------------------------------------------------------------------------------------------------------   
@client.command()
async def initialize(ctx):
    target = str(ctx.author)
    target = target[:-5]

    id = str(ctx.author.id)
    results = collection.find({"_id": {'$exists': id}})
    check = False
    for x in results:
        SubstringX = str(x)
        Modified = SubstringX[9:27]
        if Modified == id:
            check = True

    if check == False:
        create_id = {"_id": id, "UserDefaultList": emptyArr}
        collection.insert_one(create_id)
        embed = discord.Embed(
            title=target + ' added to my database!',
            description='Thanks for joining, you can now create your own lists, search them and more! \n You can check out the list of commands by typing in __**.' + textPrefix + 'help**__',
            colour=discord.colour.Color.green(),
        )
        embedRight(ctx, embed)
        await ctx.channel.send(embed=embed)
    else:
        embed = discord.Embed(
            title=target + ' already exists in my database!',
            description='You have already initialized your account. You can check out the list of commands by typing in __**.' +
            textPrefix + 'help**__',
            colour=discord.colour.Color.red()
        )
        embedWrong(ctx, embed)
        await ctx.channel.send(embed=embed)
# -----------------------------------------------------------------------------------------------------------------------------------------------
@client.command()
async def listadd(ctx, listname, *, entered):
    check = on_check_init(ctx)

    stripArr = []

    for items in entered:
        for item in items:
            item = str(item).strip()
            stripArr.append(item)


    hasE = False
    if check == False:
        embed = on_user_not_exist(get_author_name(ctx),ctx)
        await ctx.channel.send(embed=embed)
    else:
        array = entered.split(",")
        for items in array:
            if all(not x.split() for x in items):
                hasE = True

        if entered == ",": 
            embed = discord.Embed(
                title = "Usage to add multiple items is <item 1>,<item 2>......",
                description = "",
                colour=discord.colour.Color.red()
            )
            embedWrong(ctx, embed)
            await ctx.channel.send(embed=embed)

        elif ",," in entered:
            embed = discord.Embed(
                title = "Please do not use concurrent commas/ empty items",
                description = "",
                colour=discord.colour.Color.red()
            )
            embedWrong(ctx, embed)
            await ctx.channel.send(embed=embed)

        elif hasE == True:
            embed = discord.Embed(
                title = "Please do not add any empty items",
                description = "",
                colour=discord.colour.Color.red()
            )
            embedWrong(ctx, embed)
            await ctx.channel.send(embed=embed)

        elif str(entered)[:1] == "," or str(entered)[-1:] == ",":
            embed = discord.Embed(
                title = "Do not start or end with a comma",
                description = "",
                colour=discord.colour.Color.red()
            )
            embedWrong(ctx, embed)
            await ctx.channel.send(embed=embed)

        else:
            exist = False
            result = collection.find({"_id": get_author_id(ctx)})
            for items in result:
                for item in items:
                    if listname == item:
                        exist = True
            if exist == True:
                results = collection.find({"_id": get_author_id(ctx)})
                for vals in results:
                    for separate in vals:
                        if listname != "_id" and listname == separate:
                            targetArray = collection.distinct(listname)
                            if listname == "UserDefaultList":
                                arrayLength = len(targetArray)-10
                            else:
                                arrayLength = len(targetArray)
                             
            if exist == False:
                embed = wronglist(listname, ctx)
                await ctx.channel.send(embed=embed)
            else:

                id = get_author_id(ctx)

                resultsnext = collection.find({"_id": id}, {listname})
                for nextval in resultsnext:
                    nextval = str(nextval)[34+len(listname):-1]
                    targetArray = str(nextval).split(",")
                    if listname == "UserDefaultList":
                        arrayLength = len(targetArray)-10
                    else:
                        arrayLength = len(targetArray)
                   
                
                addable = 30 - arrayLength
                
                stringAdd = ""

                if arrayLength >= 30:
                    embed = discord.Embed(
                        title = "That list has reached its max limit for user " + get_author_name(ctx),
                        description = "You can remove items with the **.listremove** command",
                        colour=discord.colour.Color.red()
                    )
                    embedWrong(ctx, embed)
                    await ctx.channel.send(embed=embed)
                elif len(entered.split(",")) > addable:
                    embed = discord.Embed(
                        title = "You can only add " + str(addable) + " more item(s) in that list for user " + get_author_name(ctx),
                        description = "You can remove items with the **.listremove** command",
                        colour=discord.colour.Color.red()
                    )
                    embedWrong(ctx, embed)
                    await ctx.channel.send(embed=embed)

                else:
                    CanEnter = True
                    if "," in entered: # MULTIPLE
                        vals = entered.split(",")
                        for items in vals:
                            if len(items) > 30:
                                CanEnter = False
                
                        if CanEnter == False:
                            embed = discord.Embed(
                                title = "Make sure each entered item is 30 characters or less",
                                description = "",
                                colour=discord.colour.Color.red()
                            )
                            embedWrong(ctx, embed)
                            await ctx.channel.send(embed=embed)
                
                        else:
                            stringAdd = ""
                            addedArray = []
                            vals = entered.split(",")
                            for items in vals:
                                
                                if items not in addedArray:
                                    addedArray.append(items)
                                    
                                collection.update_one({'_id': get_author_id(ctx)}, {'$addToSet': {listname: str(items).strip()}})
    
                            for item in addedArray:
                                stringAdd = stringAdd + "," + str(item)

                            embed = discord.Embed(
                                title = "__Items added:__ " + stringAdd[1:] + "\n" + "__List added to:__ " + listname,
                                description ='Type **.listview <list name>** to view that list',
                                colour=discord.colour.Color.teal()
                            )
                            embedRight(ctx, embed)    
                            await ctx.channel.send(embed=embed)
                    

                    else: # SINGLE
                        
                        collection.update_one({'_id': get_author_id(ctx)}, {'$addToSet': {listname: entered}})
                        embed = discord.Embed(
                                title = "__Items added:__ " + entered + "\n" + "__List added to:__ " + listname,
                                description ='You can type in **.' + textPrefix +
                                'view** to check out the contents of your list. If any of those items already existed in your list, it was not added again',
                                colour=discord.colour.Color.teal()
                            )
                        embedRight(ctx, embed)
                        await ctx.channel.send(embed=embed)
# -----------------------------------------------------------------------------------------------------------------------------------------------
@listadd.error
async def AddError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title = "Incorrect Usage",
            description = "Usage is: **.listadd <list to add to> <item to add>**",
            colour=discord.colour.Color.red()
        )
        argumentError(ctx,embed)
        await ctx.channel.send(embed=embed)
#------------------------------------------------------------------------------------------------------------------------------------------------       
@client.command()
async def listhelp(ctx):
    embed = discord.Embed(
        title= 'List creating bot',
        description='This is the '+ textPrefix + ' bot. You can use me to add things to a list, remove things in them, display items in your list, and far more for unlimited purposes! \n---------------------------------------------------------------------------------------------',
        colour=discord.colour.Color.darker_grey()
    )
    embed.add_field(name='__**.initialize-**__',
                    value='Initialize and create an account \n Usage: **.initialize**', inline=False)    
    embed.add_field(name= '__**.' + textPrefix + 'add- **__',
                    value='Add something to your list \n Usage: **.'+textPrefix+'add <Listname> <Item 1>,<Item 2>,<Item 3>..**', inline=False)
    embed.add_field(name='__**.' + textPrefix +'remove-**__',
                    value='Remove something from your list \n Usage: **.'+textPrefix+'remove <Listname> <Item to remove>**', inline=False)
    embed.add_field(name='__**.' + textPrefix +'new-**__',
                    value='Create a new list, maximum of 5 \n Usage: **.'+textPrefix+'new <Name of list>**', inline=False)
    embed.add_field(name='__**.' + textPrefix +'view-**__',
                    value='View the items in your lists \n Usage: **.'+textPrefix+'view <List to view>**', inline=False)
    embed.add_field(name='__**.' + textPrefix +'created-**__',
                    value='Check the title of each list you have created \n Usage: **.'+textPrefix+'created**', inline=False)
    embed.add_field(name='__**.' + textPrefix +'amount-**__',
                    value='Displays the number of items in your list \n Usage: **.'+textPrefix+'amount <Name of list>**', inline=False)
    embed.add_field(name='__**.' + textPrefix +'delete-**__',
                    value='Delete one of your lists \n Usage: **.'+textPrefix+'delete <Name of list>**', inline=False)
    embed.add_field(name='__**.' + textPrefix +'random-**__',
                    value='Display a random item from the selected list \n Usage: **.'+textPrefix+'random <Name of list>**', inline=False)
    embed.add_field(name='__**.' + textPrefix +'clear-**__',
                    value='Clear all items in a list \n Usage: **.'+textPrefix+'clear <Name of list>**', inline=False)
    embed.add_field(name='__**.deleteaccount-**__',
                    value='Delete your account if you have one \n Usage: **.deleteaccount**', inline=False)
    await ctx.author.send(embed=embed)
    await ctx.channel.send("A DM has been sent with all the commands")
# -----------------------------------------------------------------------------------------------------------------------------------------------
@client.command()
async def listview(ctx, *, entered):
    # =====================================================
    id = str(ctx.author.id)
    results = collection.find({"_id": {'$exists': id}})
    check = False
    check = on_check_init(ctx)
    # =====================================================
    if check == True:
        id = str(ctx.author.id)
        results = collection.find({"_id": id})
        existing = False
        for x in results:
            SubstringX = str(x)
            SubstringX = SubstringX[30:]
            u = SubstringX.split("],")

            for valsget in u:
                Remove1 = valsget.replace("}", '')
                if "'" + entered + "'" in Remove1:
                    targetArray = valsget
                    existing = True
        vals = ""
        # =====================================================
        if existing == True:
            
            targetArray = targetArray.replace("[", '')
            targetArray = targetArray.replace("]", '')
            targetArray = targetArray.replace("}", '')
            lengthToCut = 1 + len(entered)+4
            targetArray = targetArray[lengthToCut:]
            
            targetArray = targetArray.split(',')
            
            
            for items in targetArray:
                items = items.replace("'", '')
                items = "**" + items + "**"
                vals = vals + items + "\n"

            target = str(ctx.author)
            target = target[:-5]
            # =====================================================
            if items == "**" + "**":
                noVals = True
            else:
                noVals = False
            # =====================================================
            if noVals == True:
                embed = discord.Embed(
                    title='There are no items in this list for user: ' + get_author_name(ctx),
                    description='You can add items in your list with the command- **.' +
                    textPrefix + 'add <name>** ',
                    colour=discord.colour.Color.red()
                )
                embedWrong(ctx, embed)
                await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title='Showing list "'+entered+"' created by " + get_author_name(ctx),
                    description=str(vals),
                    colour=discord.colour.Color.purple()
                )
                embedRight(ctx, embed)
                await ctx.channel.send(embed=embed)
        # =====================================================
        else:
            embed = wronglist(entered, ctx)
            await ctx.channel.send(embed=embed)

    # =====================================================
    else:
        embed = on_user_not_exist(get_author_name(ctx), ctx)
        await ctx.channel.send(embed=embed)
# -----------------------------------------------------------------------------------------------------------------------------------------------
@listview.error
async def ViewError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title = "Incorrect Usage",
            description = "Usage is: **.listview <list to view>**",
            colour=discord.colour.Color.red()
        )
        argumentError(ctx,embed)
    await ctx.channel.send(embed=embed)
#------------------------------------------------------------------------------------------------------------------------------------------------ 
@client.command()
async def listremove(ctx, listname, *, entered):
    debug = True
    check = on_check_init(ctx)
    id = str(ctx.author.id)
    if check == True:
        results = collection.find({"_id": {'$exists': id}})

        for items in results:
            for item in items:
                if str(item) == listname:
                    debug = False

        if debug == True:
            embed = wronglist(listname, ctx)
            await ctx.channel.send(embed=embed)

        else:
            target = str(ctx.author)
            target = target[:-5]
            toAdd = str(entered)

            results = collection.find({"_id": id})
            for x in results:
                results = collection.find({"_id": id})
                for x in results:
                    SubstringX = str(x)
                    Modified = SubstringX[:-1]
                    length = len(Modified)
                    RemoveFirst = Modified[50:length-1]
                    u = RemoveFirst.split(",")
                    results = collection.find({'_id': id},{listname: entered})
                    for vals in results:
                        targetArray = str(vals)
                        targetArray = targetArray[:-1]
                        targetArray = targetArray[34+len(listname):]
                        
                if entered in targetArray:
                    u.append(str(entered))
                    collection.update_one(
                        {'_id': id}, {'$pull': {listname: str(toAdd)}})
                    embed = discord.Embed(
                        title="Item removed: " + entered + "\n" + "List removed from: " + listname + "\n" + "By user: " + get_author_name(ctx),
                        description='You can type in **.' + textPrefix + 'view** to check out the contents of your list',
                        colour=discord.colour.Color.teal()
                    )
                    embedRight(ctx, embed)
                    await ctx.channel.send(embed=embed)

                else:
                    embed = discord.Embed(
                        title="Entered item not in that list" + "\n" + "User: " + get_author_name(ctx),
                        description='You may have entered the wrong list or not added that item',
                        colour=discord.colour.Color.red()
                    )
                    embedWrong(ctx, embed)
                    await ctx.channel.send(embed=embed)


    else:
        target = str(ctx.author)
        target = target[:-5]
        embed = on_user_not_exist(target, ctx)
        await ctx.channel.send(embed=embed)
# -----------------------------------------------------------------------------------------------------------------------------------------------
@listremove.error
async def RemoveError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title = "Incorrect Usage",
            description = "Usage is: **.listremove <list to remove from> <item to remove>**",
            colour=discord.colour.Color.red()
        )
        argumentError(ctx,embed)
    await ctx.channel.send(embed=embed)
#------------------------------------------------------------------------------------------------------------------------------------------------ 
@client.command()
async def listnew(ctx, entered):
    check = on_check_init(ctx)
    if check == True:
        if len(entered) > 15:
            embed = discord.Embed(
                title="Length error!",
                description="Only lists with a character count of 15 or less can be added",
                colour=discord.colour.Color.red()
            )
            await ctx.channel.send(embed=embed)
        elif "," in entered:
            embed = discord.Embed(
                title="Character error!",
                description="Do not include any commas in your list",
                colour=discord.colour.Color.red()
            )
            embedWrong(ctx, embed)
            await ctx.channel.send(embed=embed)

        else:
            id = str(ctx.author.id)
            results = collection.find({"_id": id})
            count = 0
            existingList = False
            for x in results:
                for y in  x:
                    count = count + 1
                    if entered == y:
                        existingList = True

            
            if count < 6:
            
                if existingList == False:
                    id = str(ctx.author.id)
                    collection.update_one(
                        {"_id": id},
                        {"$set":
                         {entered: emptyArr,
                          }})
                    target = get_author_name(ctx)
                    embed = discord.Embed(
                        title="New list made: " + str(entered),
                        description="For user: " + str(target),
                        colour=discord.colour.Color.green()
                    )
                    embedRight(ctx, embed)
                    await ctx.channel.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="User, "+get_author_name(ctx)+ " already has a list with that name",
                        description= "",
                        colour=discord.colour.Color.red()
                    )
                    embedWrong(ctx, embed)
                    await ctx.channel.send(embed=embed)

            else:
                embed = discord.Embed(
                    title="User, "+get_author_name(ctx)+" has reached maximum number of lists that can be created",
                    description="You can delete a list by typing in- **." +
                    textPrefix + "delete <list name>**",
                    colour=discord.colour.Color.red()
                )
                embedWrong(ctx, embed)
                await ctx.channel.send(embed=embed)

    else:
        target = get_author_name(ctx)
        embed = on_user_not_exist(target, ctx)
        await ctx.channel.send(embed=embed)
# -----------------------------------------------------------------------------------------------------------------------------------------------
@listnew.error
async def NewError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title = "Incorrect Usage",
            description = "Usage is: **.listadd <Name of list to make>**",
            colour=discord.colour.Color.red()
        )
        argumentError(ctx,embed)
    await ctx.channel.send(embed=embed)
#------------------------------------------------------------------------------------------------------------------------------------------------ 
@client.command()
async def listcreated(ctx):
    check = on_check_init(ctx)
    if check == True:

        id = get_author_id(ctx)
        target = get_author_name(ctx)

        results = collection.find({"_id": id})
        vals = ""
        for items in results:
            for item in items:
                if item != "_id":
                    vals = vals + item + "\n"

        embed = discord.Embed(
            title='Showing all lists created by '+ target,
            description=str(vals),
            colour=discord.colour.Color.from_rgb(225,233,0)
        )
        embedRight(ctx, embed)
        await ctx.channel.send(embed=embed)
    else:
        embed = on_user_not_exist(get_author_name(ctx),ctx)
        await ctx.channel.send(embed=embed)
#------------------------------------------------------------------------------------------------------------------------------------------------ 
@client.command()
async def listamount(ctx, listname):
    check = on_check_init(ctx)
    if check == True:

        id = get_author_id(ctx)
        results = collection.find({"_id": id})
        exists = False
        for items in results:
            for item in items:
                if item == listname:
                    exists = True

        
    
        if exists == True:
            results = collection.find({"_id": id})
            for vals in results:
                for separate in vals:
                    if listname != "_id" and listname == separate:
                        resultsnext = collection.find({"_id": id}, {listname})
                        for items in resultsnext:
                            items = str(items)[34+len(listname):-1]
                            targetArray = str(items).split(",")
                        if listname == "UserDefaultList":
                            arrayLength = len(targetArray)-10
                        else:
                            arrayLength = len(targetArray)
                        if arrayLength ==1 :
                            stringVal = "item"
                        else:
                            stringVal = "items"
                        embed = discord.Embed(
                            title="No of items: " + str(arrayLength) + " " + stringVal,
                            description= 'List: ' + listname,
                            colour=discord.colour.Color.green()
                        )
                        embedRight(ctx, embed)
        else:
            embed = wronglist(listname, ctx)
            embedWrong(ctx, embed)
        
        
        await ctx.channel.send(embed=embed)
    else:
        embed = on_user_not_exist(get_author_name(ctx),ctx)
        await ctx.channel.send(embed=embed)
# -----------------------------------------------------------------------------------------------------------------------------------------------
@listamount.error
async def AmountError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title = "Incorrect Usage",
            description = "Usage is: **.listamount <list to check amount of>**",
            colour=discord.colour.Color.red()
        )
        argumentError(ctx,embed)
    await ctx.channel.send(embed=embed)
# -----------------------------------------------------------------------------------------------------------------------------------------------
@client.command()
async def listdelete(ctx, listname):
    check = on_check_init(ctx)
    if check == True:
        id = get_author_id(ctx)
        results = collection.find({"_id": id})
        exists = False
        for items in results:
            for item in items:
                if item == listname:
                    exists = True
        
        if exists == True:
            if listname == "UserDefaultList":
                embed = discord.Embed(
                    title='You cannot delete the default list',
                    description=' ',
                    colour=discord.colour.Color.dark_red()
                )
                embedWrong(ctx, embed)
                await ctx.channel.send(embed=embed)
            else:
                collection.update_one( { "_id": get_author_id(ctx) },{ "$unset": {listname: ""}})
                embed = discord.Embed(
                    title='List deleted: ' + listname + "\n" + "for user, " + get_author_name(ctx),
                    description='You can create new lists with the command- **.'+textPrefix+'new <name>**',
                    colour=discord.colour.Color.dark_green()
                )
                embedRight(ctx, embed)
                await ctx.channel.send(embed=embed)
        else:
            embed = wronglist(listname, ctx)
            embedWrong(ctx, embed)
            await ctx.channel.send(embed=embed)

    else:
        embed = on_user_not_exist(get_author_name(ctx),ctx)
        await ctx.channel.send(embed=embed)
# -----------------------------------------------------------------------------------------------------------------------------------------------
@listdelete.error
async def DeleteError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title = "Incorrect Usage",
            description = "Usage is: **.listdelete <name of list to delete>**",
            colour=discord.colour.Color.red()
        )
        argumentError(ctx,embed)
    await ctx.channel.send(embed=embed)
# -----------------------------------------------------------------------------------------------------------------------------------------------
@client.command()
async def listrandom(ctx, entered):
    check = on_check_init(ctx)

    if check == True:
        id = get_author_id(ctx)
        results = collection.find({"_id": id})
        exists = False
        for items in results:
            for item in items:
                if item == entered:
                    exists = True

        if exists == True:

            if check == True:
                id = str(ctx.author.id)
                results = collection.find({"_id": id})
                existing = False
                for x in results:
                    SubstringX = str(x)
                    SubstringX = SubstringX[30:]
                    u = SubstringX.split("],")

            for valsget in u:
                Remove1 = valsget.replace("}", '')
                if "'" + entered + "'" in Remove1:
                    targetArray = valsget
                    existing = True
            vals = ""
            # =====================================================
            if existing == True:
                targetArray = targetArray.replace("[", '')
                targetArray = targetArray.replace("]", '')
                targetArray = targetArray.replace("}", '')
                lengthToCut = 1 + len(entered)+4
                targetArray = targetArray[lengthToCut:]
                targetArray = targetArray.split(',')
            
            
            for items in targetArray:
                items = items.replace("'", '')
                items = "**" + items + "**"
                vals = vals + items + "\n"

            target = str(ctx.author)
            target = target[:-5]

            string = ""
            string = targetArray[random.randint(0,len(targetArray)-1)]
            if string == "":
                embed = discord.Embed(
                    title='There are no items in that list',
                    description='You can add items in your list with the command- **.' +
                    textPrefix + 'add <name>** ',
                    colour=discord.colour.Color.red()
                )
                embedWrong(ctx, embed)
                await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=string,
                    description='Random item from, ' + entered,
                    colour=discord.colour.Color.from_rgb(22,200,236)
                )
                embedRight(ctx, embed)
                await ctx.channel.send(embed=embed)

        else:
            embed = wronglist(entered, ctx)
            await ctx.channel.send(embed=embed)
      
    else:
        embed = on_user_not_exist(get_author_name(ctx),ctx)
        await ctx.channel.send(embed=embed)
# -----------------------------------------------------------------------------------------------------------------------------------------------
@listrandom.error
async def RandomError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title = "Incorrect Usage",
            description = "Usage is: **.listrandom <list to get random item from>**",
            colour=discord.colour.Color.red()
        )
        argumentError(ctx,embed)
    await ctx.channel.send(embed=embed)
# -----------------------------------------------------------------------------------------------------------------------------------------------
@client.command()
async def listclear(ctx, entered):
    check = on_check_init(ctx)
    if check == True:
        id = get_author_id(ctx)
        results = collection.find({"_id": id})
        exists = False
        for items in results:
            for item in items:
                if item == entered:
                    exists = True
        if exists == True:
            collection.update_one({'_id': id}, {"$set":{entered:[]}})
            embed = discord.Embed(
                title= "List cleared: " + entered + "\n" + "By user: " + get_author_name(ctx),
                description='You can create new lists with the command- **.'+textPrefix+'new <name>**',
                colour=discord.colour.Color.from_rgb(186,239,13)
            )
            embedRight(ctx, embed)
            await ctx.channel.send(embed=embed)

        else:
            embed = wronglist(entered, ctx)
            await ctx.channel.send(embed=embed)

    else:
        embed = on_user_not_exist(get_author_name(ctx),ctx)
        await ctx.channel.send(embed=embed)
# -----------------------------------------------------------------------------------------------------------------------------------------------
@listclear.error
async def ClearError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title = "Incorrect Usage",
            description = "**.listclear <name of list to clear>**",
            colour=discord.colour.Color.red()
        )
        argumentError(ctx,embed)
    await ctx.channel.send(embed=embed)
# -----------------------------------------------------------------------------------------------------------------------------------------------
@client.command()
async def deleteaccount(ctx):
    check = on_check_init(ctx)
    id = get_author_id(ctx)
    if check == True:
        collection.delete_one({ "_id": id })
        embed = discord.Embed(
            title= get_author_name(ctx) + "'s account has been deleted",
            description='You can make your account again with the **.initialize** command',
            colour=discord.colour.Color.from_rgb(255,255,255)
        )
        embedRight(ctx, embed)
        await ctx.channel.send(embed=embed)
    else:
        embed = on_user_not_exist(get_author_name(ctx),ctx)
        await ctx.channel.send(embed=embed)
# -----------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title = "Incorrect command",
            description = "The command you have entered does not exist. Type in **.listhelp** for DM of commands",
            colour=discord.colour.Color.red()
        )
        embed.set_footer(text = "Bot created by Senthu")
        embed.set_thumbnail(url = "https://i.imgur.com/kwVsyeX.png") 
        embed.set_author(name=embedname, icon_url=embedCross)
        await ctx.channel.send(embed=embed)
# ----------------------------------------------------------------------------------------------------------------------------------------------- 


client.run('NzMyMjEyNDEwODU2NzY3NjA5.XwxT8g._d-Wk92gu5_96FDQRCz5v5blpkY')
