import os, discord

client = discord.Client(intents=discord.Intents.default())
kanal_id, forum_url, token = "1488544646241059088", "https://sip.elfak.ni.ac.rs/", os.environ["bot"]

@client.event
async def on_ready():
    ch = await client.fetch_channel(int(kanal_id))
    async for msg in ch.history(limit=1): await msg.delete()
    
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Otvori forum", url=forum_url))

    fajl = discord.File("tabela.png")
    
    await ch.send("@everyone \nPrijava ispita je pocela !", file=fajl, view=view)
    await client.close()

client.run(token)
