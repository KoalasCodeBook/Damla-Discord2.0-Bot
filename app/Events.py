from discord.ext import commands
from discord.channel import TextChannel,DMChannel
import discord, asyncio
import random as rd
import sqlite3 as sql
from datetime import date

from app.func import *
from app.Commands import damla,netflix,delete,random,cfg,TimeCounter 


class onReady(commands.Cog,name="onReady"):
    def __init__(self,client:commands.Bot):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("U're online. Welcome {0.user}".format(self.client))
        await self.client.change_presence(status=discord.Status.idle,activity=discord.Game(' with not existing penis'))
        
        global dwarfs_server_object
        global role_of_bots
        global MemberInRoom 

        MemberInRoom = {}
        dwarfs_server_object = discord.utils.get(self.client.guilds, id = 54100000000000000000)      #From Dwarf's Server ID to SERVER OBJECT
       
        
        return
    
class onMessageEvents(commands.Cog,name="onMessageEvents"):
    def __init__(self, client:commands.Bot):
        self.client = client    
        self.damla_nikname = ["damla", "damlacım", "damlacık", "damloş"]
        self.blasphemous_content = ["fuck","bitch","hoe","amk","mother fucker"]
        self.howareyou_question = ["Whats up","how are u", "wapopo"]
        self.hallihallo = ["hi","hello"]
        self.quote_sozler = ["quotes","özlü sözler","özlü söz", "günün sözü", "damla damlat bir söz"]
        self.game = ["lol", "apex", "cs ", "cs go"]
        self.sevgi = [" ...oyundan önce biraz aşk?","de beni önce bi aşıla","ama önce meme pompa?"]
        self.deniz_orospu = ["put to sea", "sea of thieves"]

    @commands.Cog.listener()
    async def on_message(self, message):
        if(isinstance(message.channel,TextChannel)):
            #if user is bot 
            if message.author.bot: 
                if message.author.id == 184405311681986560: #FredBot
                    print(fredBotPlayer(message.content))
                return False  
            #Nasılsın Soru ???!!!
            if any(word in message.content for word in self.nasilsin_icerik) and any(word in message.content for word in self.damla_nikname):
                data = nasilsin_veri_cek()
                i = rd.randrange(0, len(data))
                await message.channel.send(data[i - 1][1])
                return
            #Merhabalar
            if any(word in message.content for word in self.merhabalar) and any(word in message.content for word in self.damla_nikname):
                await message.channel.send("Hello my Sweetheart")
                return
            #Küfür içeriği  $$$$$    
            if any(word in message.content for word in self.kufur_icerik):
                if message.author.name == "Timo":
                    await message.channel.send("Fuck u Timo")
                    return
                else:
                    yazi = "Nononono I will fuck you, " + message.author.name + "!"
                    await message.channel.send(yazi)
                    return
            #Günün Özlü Sözü
            if any(word in message.content for word in self.ozlu_sozler):
                await message.channel.send(get_quote())
                return
            #oyun sorgusu
            if any(word in message.content for word in self.oyunlar):
                answer = "Comming too{}".format(random.choice(self.sevgi))
                await message.channel.send(answer)
                return
            #Sea of Thieves
            if any(word in message.content for word in self.deniz_orospu):
                await message.channel.send("Does my captain wish some entertainment? <3")
                return
            #-----Otoma. Haftanın Sikilmeliği ------    
            ##Music linkini yanlış yere gönderirse##
            if "!play" in message.content or "?play" in message.content or "+play" in message.content:
                if message.channel.id == 5700000000000657 or message.channel.id == 961000000000094:          
                    return #written in right place
                else:
                    dwarfs_server_object = discord.utils.get(self.client.guilds, id = 5480000009655)
                    role = discord.utils.get(dwarfs_server_object.roles, id = 572000000007956)

                    await message.channel.send("You retard got caught!")
                    await message.author.send("I just wanted to remind you are retarde.")
                    await message.author.send("https://fredboat.com/music-player/5485300000009655")
                                        
                    await message.author.add_roles(role)  
            #--------IMDB data processing-----------------
            #Add Movie to DB
            if message.content.startswith("https://www.imdb.com/title"):          
                user = message.author.name
                link = message.content
                veri = film_imdb_sorgula(link, user)    
                await message.author.send(veri)
                return        
            #Movie Suggestion
            if message.content == "damla movie":
                data = film_veri_listele()
                film_sayisi = len(data)
                random_sayi = rd.randrange(0, film_sayisi)
                data = data[random_sayi]
                tarih = str(data[5])
                user = data[6]

                embed = discord.Embed(title=data[1] + "(" + tarih[0:4] + ") [" +
                                    str(data[0]) + "/" + str(film_sayisi) + "]",
                                    url="https://www.imdb.com" + data[2],
                                    description=data[4],
                                    colour=discord.Colour.red())

                embed.set_image(url=data[3])
                #embed.add_field(name="Toplam Film Sayısı:", value=str(film_sayisi),inline=True)
                embed.set_footer(text="Film'i ekleyen şahsiyet:" + str(user))

                await message.channel.send(embed=embed)
                return
            #Eklenen Tüm Fimleri Listele
            if message.content == "damla all movies":
                time.sleep(0.3)
                data = film_veri_listele()
                if len(data) > 100:
                    await message.channel.send("Veri Limit aşıyor!!")
                    return
                else:
                    embed = discord.Embed(
                        title="Film Listesi",
                        colour=discord.Colour.blue(),
                    )
                    for veri in data:
                        embed.add_field(name=str(veri[0])+". "+veri[1],
                                        value="https://www.imdb.com" +
                                        str(veri[2]),
                                        inline="False")
                    
                    await message.channel.send(embed=embed)
                    return
            #------Damla----------------------------------
            if message.content in self.damla_nikname:
                embed = discord.Embed(
                    title="Merhaba benim adım Damla ",
                    description="Romanya'nın Moldova Nouă kasabasında hayat buldum. Hayatta kalabilmek için hayat kadını mesleğini öğrendim. İlk başlarda çok zorlandım fakat zamanla genişledim. ",
                    colour=discord.Colour.red())
      
                embed.set_thumbnail(url="https://media.istockphoto.com/photos/picture-of-a-sad-pet-ass-picture-id822753276")               

                embed.add_field(name="Damla Movie",
                                value="Eklenen filmlerden bir tanesi listelenir, bok da çıkabilir",
                                inline=True)  
                embed.add_field(name="?How to add Movie?",
                                value="IMBD linkini movie'ye ekle",
                                inline=True)
                embed.add_field(name="CFG",
                                value="Kayıtlı tüm CFG dosyaları listelenecek ",
                                inline=True)
                embed.add_field(name="!Damla ekle @username 1",
                                value="Bir Damla ısmarla",
                                inline=True)
                embed.add_field(name="!Damla sorgu @username",
                                value="Damla borçlarını sergiler",
                                inline=True)               
                embed.add_field(name="!Random",
                                value="Rastegele takım oluştur",
                                inline=True) 
                embed.add_field(name="özlü sözler",
                                value="Bu günün özlü sözü",
                                inline=True)     
                 

                msg = await message.channel.send(embed=embed)
                await asyncio.sleep(0.8)
                embed.set_thumbnail(url="https://id.metu.edu.tr/wp-content/uploads/2019/04/Layer-21.png")  
                await msg.edit(embed=embed)                
                return

        if(isinstance( message.channel,DMChannel)):
            if message.author.bot: 
                return False  
                        
            if message.content == "help":  
                text = """
                    !netflix
                    !delte
                    !damla
                    !random
                    !cfg
                    !timeCounter
                """
                embed=discord.Embed(title="bok")
                embed.add_field(name="1",value=text,inline=False)

                #await message.channel.send(text)      
                await message.channel.send(embed=embed)

                
            if "fredbot" in message.content:
                return await message.channel.send("https://fredboat.com/music-player/548000000109655")
        
class onMemberUpdate(commands.Cog,name="onMemberUpdate"):
    def __init__(self, client:commands.Bot):
        self.client = client  
    
    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        MemberId = member.id
        MemberName = member.name

        con = sql.connect("app/data/database.db")
        cursor = con.cursor()       
        cursor.execute("CREATE TABLE IF NOT EXISTS connectionCounter(memberName TEXT,memberId TEXT,time TEXT,creatingData TEXT)");con.commit()
        
      
        if before.channel == None and after.channel != None:
            #moved in    
            MemberInRoom[member.id] = int(time.time())
        
        elif before.channel != None and after.channel == None:
            #has leaved
            try:
                newCounts = int(time.time()) - int(MemberInRoom[member.id])

                cursor.execute("SELECT * FROM connectionCounter WHERE MemberId = ?",(member.id,))
                timeCounter = cursor.fetchall()

                oldCounts = int(timeCounter[0][2])
                result = oldCounts + newCounts

                if len(timeCounter) == 0:
                    cursor.execute("INSERT INTO connectionCounter VALUES (?,?,?,?)",(str(member.name),str(member.id),str(result),str(date.today())));con.commit()
                else:
                    cursor.execute("UPDATE connectionCounter SET time = ? WHERE memberId = ?",(str(result),str(member.id)));con.commit()

            except:
                pass
            finally:
                MemberInRoom[member.id] = ""
            
        return
  



    