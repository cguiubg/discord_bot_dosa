import interactions
from interactions import CommandContext

import dosa.toks as toks
import dosa.game as game

class DosaClient(interactions.Client):
    def __init__(self, bot_token: str, guild_id: str, **kwargs):
        super().__init__(
            token=bot_token,
            default_scope=guild_id,
            kwargs=kwargs
        )


class Dosa:

    client: DosaClient = DosaClient(
        bot_token=toks.bot_token,
        guild_id=toks.guild_id
    )

    dnd = game.Game()


    @staticmethod
    @client.command(
        name="post",
        description="Post a new quest"
        
    )
    async def post(ctx: CommandContext):
        channel = await ctx.get_channel()
        if channel.id == toks.bulletin_id:
            modal = interactions.Modal(
                title="Post a quest!",
                custom_id="post_modal",
                components=[
                    interactions.TextInput( # type: ignore # COC
                        style=interactions.TextStyleType.SHORT,
                        label="Quest name:",
                        custom_id="name",
                        max_length=30,
                    ),
                    interactions.TextInput( # type: ignore # COC
                        style=interactions.TextStyleType.PARAGRAPH,
                        label="description:",
                        custom_id="descr",
                        max_length=140,
                    )
                ],
            )
            await ctx.popup(modal)
        else:
            guild = await ctx.get_guild()
            channels = await guild.get_all_channels()
            bulletin_channel = [ch.name for ch in channels if ch.id == toks.bulletin_id]
            if len(bulletin_channel) > 0:
                await ctx.send(f"This command can only be run in {bulletin_channel[0]}", ephemeral=True)
            else:
                await ctx.send("No bulletin board set up. Ask your admin do create one!")

    @staticmethod
    @client.modal("post_modal")
    async def post_modal_response(ctx: CommandContext, name: str, descr: str):
        _, response = Dosa.dnd.new_quest(name, descr, ctx.user.id)
        await ctx.send(response)


    @staticmethod
    @client.command(
        name="take_down_quest",
        description="Remove a quest from the bulletin board.",
        options = [
            interactions.Option(
                name="quest_id",
                description="Quest id of the quest to remove.",
                type=interactions.OptionType.INTEGER,
                required=True,
            )
        ],
    )
    async def take_down_quest_command(ctx: CommandContext, quest_id: int):
        channel = await ctx.get_channel()
        if channel.id == toks.bulletin_id:
            result, response = Dosa.dnd.remove_quest(quest_id, ctx.user.id)
            if not result:
                await ctx.send(response, ephemeral=True)
                return
            else:
                history = await channel.get_history()
                history = [] if not history else history
                for message in history:
                    if message.content.startswith(f"#{quest_id}"):
                        await message.delete()
                await ctx.send(response, ephemeral=True)
                return
        else:
            guild = await ctx.get_guild()
            channels = await guild.get_all_channels()
            bulletin_channel = [ch.name for ch in channels if ch.id == toks.bulletin_id]
            if len(bulletin_channel) > 0:
                await ctx.send(f"This command can only be run in {bulletin_channel[0]}", ephemeral=True)
            else:
                await ctx.send("No bulletin board set up. Ask your admin do create one!", ephemeral=True)
        


    @staticmethod
    @client.command(
        name="join",
        description="Join a posted quest.",
        options = [
            interactions.Option(
                name="quest_id",
                description="The id of the quest you want to join.",
                type=interactions.OptionType.INTEGER,
                required=True,
            ),
            interactions.Option(
                name="character_name",
                description="The name of character you'd like to join quest as.",
                type=interactions.OptionType.STRING,
                required=False,
            ),
        ],
    )
    async def join_command(ctx: CommandContext, quest_id: str, character_name: str | None = None):
        if character_name:
            _, response = Dosa.dnd.join_quest_by_character(quest_id, ctx.user.id, character_name)
        else:
            _, response = Dosa.dnd.join_quest_by_id(quest_id, ctx.user.id)
        
        await ctx.send(response, ephemeral=True)


    @staticmethod
    @client.command(
        name="leave",
        description="Leave a quest you've joined.",
        options = [
            interactions.Option(
                name="quest_id",
                description="The id of the quest you want to leave.",
                type=interactions.OptionType.INTEGER,
                required=True,
            ),
        ],
    )
    async def leave_command(ctx: CommandContext, quest_id: int):
        await ctx.send(f"{ctx.author.name} wants to leave quest: {quest_id}! Fill in functionality.")


    # Character Management Commands
    
    @staticmethod
    @client.command(
        name="new_character",
        description="Create a new player character.",
        options = [
            interactions.Option(
                name="character_name",
                description="The name of your new character",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def new_character_command(ctx: CommandContext, character_name: str):
        print(ctx.user.id)
        _, response = Dosa.dnd.new_character(ctx.user.id, character_name)
        await ctx.send(response, ephemeral=True)

    @staticmethod
    @client.command(
        name="switch_character",
        description="Switch your current playable character.",
        options = [
            interactions.Option(
                name="character_name",
                description="Name of character you want to play.",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def switch_character_command(ctx: CommandContext, character_name: str):
        print(ctx.user.id)
        result, response = Dosa.dnd.switch_character(ctx.user.id, character_name)
        if result:
            try:
                # change user nickname
                guild = await ctx.get_guild()
                await guild.modify_member(ctx.user.id, nick=character_name)
            except:
                response += " Cannot change your nickname."

        await ctx.send(response, ephemeral=True)

    @staticmethod
    @client.command(
        name="list_characters",
        description="Get a list of your registered characters."
    )
    async def list_characters_command(ctx: CommandContext):
        print(ctx.user.id)
        _, response = Dosa.dnd.list_characters(ctx.user.id)
        await ctx.send(response, ephemeral=True)

    @staticmethod
    @client.command(
        name="remove_character",
        description="Remove a character you have registered.",
        options= [
            interactions.Option(
                name="character_name",
                description="Name of character you want to remove",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def remove_character_command(ctx: CommandContext, character_name: str):
        _, response = Dosa.dnd.remove_character(ctx.user.id, character_name)
        if character_name == ctx.author.nick:
            # change user nickname
            pass
        await ctx.send(response, ephemeral=True)
