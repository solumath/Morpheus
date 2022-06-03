from disnake.ext import commands
import json
import requests
import time
import keys

class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="count", description="Count all messages from everyone")
    @commands.has_permissions(administrator=True)
    async def message_count(self, ctx):
        member_ids = [member.id for member in ctx.guild.members]
        messages_count = {}
        headers = {
                    'authorization': keys.authorization
                    }
        for ids in member_ids:
            r = requests.get(f'https://discord.com/api/v9/guilds/{ctx.guild.id}/messages/search?author_id={ids}&include_nsfw=true', headers=headers)
            data = json.loads(r.text)
            username = ctx.guild.get_member(ids)

            messages_count.update({ids : data['total_results']})
            await ctx.send(f"**Jméno** = {username}; **ID** ={ids} ; **počet zpráv** = {data['total_results']}")
            # prevent rate limit
            time.sleep(2)

        with open(f"servers/{ctx.guild.name}/messages.json",'w', encoding='utf-8') as f:
                    json.dump(messages_count, f, ensure_ascii=False, indent=4)

def setup(bot):
    bot.add_cog(Messages(bot))
