from app.func import *

from discord.ext import commands
from unicodedata import decimal
from datetime import date

import sqlite3 as sql
import discord
import asyncio 




 
class netflix(commands.Cog,name="Netflix Login Information"):
    def __init__(self,client:commands.Bot):
        self.client = client
        self.netflixUsers = ["29***********60","29**************17","49************80"] #MyFamily
        self.link = "https://www.netflix.com/tr-en/login"
    
    @commands.command()
    async def netflix(self,ctx:commands.Context):
        if ctx.author.id in self.netflixUsers:
            myMail = "myMail@outlook.com"
            password = "myPassword"
          
            embed = discord.Embed(title="Netflix Login Information")
            embed.add_field(name="username", value=myMail, inline="False")      
            embed.add_field(name="password", value=password, inline="False")
            myMessage = await ctx.author.send(embed=embed)    
            await asyncio.sleep(2)

            embed = discord.Embed(title="auto destroy in 8 sec ....")
            embed.add_field(name="username", value=myMail, inline="False")      
            embed.add_field(name="password", value=password, inline="False")
            await myMessage.edit(embed=embed)
            await asyncio.sleep(3)

            embed = discord.Embed(title="auto destroy in 5 sec ....")
            embed.add_field(name="username",value=myMail, inline="False")      
            embed.add_field(name="password", value=password, inline="False")
            await myMessage.edit(embed=embed)
            await asyncio.sleep(5)

            embed = discord.Embed(title="too late")
            embed.add_field(name="username", value=myMail, inline="False")      
            embed.add_field(name="password", value="******", inline="False")
            await myMessage.edit(embed=embed)
            return
        else:
            await ctx.author.send("you are not authorized")
        return  

class delete(commands.Cog,name="Delete Message"):
    def __init__(self,client:commands.Bot,*args):
        self.client = client
        self.args = args
    
    @commands.command()
    async def delete(self,ctx:commands.Context,*args):
        if ctx.author.name == "Mr.Koala":
            if len(args) == 1:
                try:
                    sayi = int(args[0])
                    await ctx.channel.purge(limit=sayi)
                    return
                except:
                    await ctx.send("!delete <int>")
           
        else:
            ctx.send("you are not authorized")     

class damla(commands.Cog,name="Damla add/request"):
    def __init__(self,client:commands.Bot,*args):
        self.client = client
        self.args = args

    @commands.command()
    async def damla(self,ctx:commands.Context,*args):   
        con = sqlite3.connect("app/data/database.db")
        cursor = con.cursor()   

        if args[0] == "add":   #!damla add @mrkoala 1             
            if "<@" in args[1]:
                kime = user_duzenle(args[1])
            else:
                return await ctx.send("Damla borçlarını sadece bir Kullancıya atılabilir")
            kimden = ctx.author.id
            date = "Null"

            try:
                adet = int(args[2])
            except:
                return await ctx.send("Bir sayı girilmeli")            
                                                        
            cursor.execute("CREATE TABLE IF NOT EXISTS damla_sozler(from_user TEXT,to_user TEXT,date DATE)")            
            for i in range(0,int(adet)):
                cursor.execute("INSERT INTO damla_sozler VALUES(?,?,?)",(kimden,kime,date))
            con.commit()

            return await ctx.send("Damla borçları kayda geçmiştir")
        elif args[0] == "request": #!damla request / !damla request <@userID>
            if len(args) == 1: #!damla sorgu 
                authorID = ctx.author.id    
            if len(args) == 2: #!damla sorgu <@userID>
                authorID = user_duzenle(args[1])
  
            cursor.execute("SELECT * FROM damla_sozler where to_user = ?",(authorID,))    
            borcuOlanlar = cursor.fetchall()
            borcuOlanlarTemp = []

            cursor.execute("SELECT * FROM damla_sozler where from_user = ?",(authorID,))    
            borcluOldugun = cursor.fetchall()
            borcluOldugunTemp = []

            #sana borçlu olanlar
            for i in borcuOlanlar:
                borcuOlanlarTemp.append(i[0])
            #senin borçlu olduğun
            for i in borcluOldugun:
                borcluOldugunTemp.append(i[1])
                        
            borcuOlanlarResult = ""
            for i in set(borcuOlanlarTemp):
                borcuOlanlarResult += "<@" + str(i)+ ">  " + str(borcuOlanlarTemp.count(i)) + "  _|_  "

            borcluOldugunResult = ""
            for i in set(borcluOldugunTemp):
                adet = borcluOldugunTemp.count(i)
                borcluOldugunResult += "<@" + str(i)+ ">  " + str(adet) + "  _|_  "


            #sayma algoritması 
            if len(borcuOlanlarResult) == 0 :
                borcuOlanlarResult="Bulunamadı"
            if len(borcluOldugunResult) == 0:
                borcluOldugunResult = "Bulunamadı"

            embed=discord.Embed(title="Damla Borçları")
            embed.add_field(name="Sana Borcu olanlar", value=borcuOlanlarResult, inline=False)
            embed.add_field(name="Senin Borçlu oldukların", value=borcluOldugunResult, inline=False)
            await ctx.send(embed=embed)
        else:
            return await ctx.send("Wronge answers to wronge questions")
  
class random(commands.Cog,name="Create Random Teams"):
    def __init__(self,client:commands.Bot):
        self.client = client

    @commands.command()
    async def random(self,ctx:commands.Context):   #!random 
        try:
            memberList = list(ctx.author.voice.channel.voice_states.keys())
            embed = randomUser(memberList)    
            if embed:
                await ctx.channel.send(embed=embed)
            else:
                await ctx.channel.send("go playing alone")
        except AttributeError:
            await ctx.channel.send("first join a room")   
            
class cfg(commands.Cog,name="CS:GO cfg"):
    def __init__(self,client:commands.Bot):
        self.client = client

    @commands.command()
    async def cfg(self,ctx:commands.Context):  
        await ctx.send(file=discord.File('app/data/cfg/koala.rar'))
        return

class TimeCounter(commands.Cog,name="TimeCounter"):
    def __init__(self,client:commands.Bot):
        self.client = client

    @commands.command()
    async def timeCounter(self,ctx:commands.Context):  
        MemberID = ctx.author.id

        con = sql.connect("app/data/database.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM connectionCounter WHERE memberId=?",(MemberID,))
        data = cursor.fetchall()
        
        if len(data)!=0:
            data = data[0]
            inSecond = int(data[2])
            inMinutes = int(inSecond/60)
            inHours = int(inMinutes/60)

            if inHours>0:
                result = "Cücelerin Diyarında **{} saatini** heba etmişsin.".format(inHours)
            elif inMinutes>0:
                result = "Cücelerin Diyarında **{} dakikanı** heba etmişsin.".format(inMinutes) 
            else:
                result = "Daha kaynaşmamışsın ki bile, ama yine de utanmadan elini sağ sola sokuyorsun!"  

            await ctx.send(result)
        
        else:           
            await ctx.send("Veri tabanı kayıdın bulunamadı. Odaya tekrar bağlan. ")   
        return


