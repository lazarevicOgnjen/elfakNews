import os, sys, discord

client = discord.Client(intents=discord.Intents.default())
kanal_id, forum_url, token = sys.argv[1], sys.argv[2], os.environ["bot"]

@client.event
async def on_ready():
    ch = await client.fetch_channel(int(kanal_id))
    async for msg in ch.history(limit=1): await msg.delete()
    
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Otvori forum", url=forum_url))
    
    await ch.send("Forum je ažuriran !", view=view)
    await client.close()

client.run(token)
