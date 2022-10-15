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
        result, response = Dosa.dnd.new_quest(name, descr)
        await ctx.send(response)


    @staticmethod
    @client.command(
        name="join",
        description="Join a posted quest.",
        options = [
            interactions.Option(
                name="quest_id",
                description="The id of the quest you want to join.",
                type=interactions.OptionType.STRING,
                required=True,
            ),
            interactions.Option(
                name="character_name",
                description="The name of character you'd like to join quest as.",
                type=interactions.OptionType.STRING,
            ),
        ],
    )
    async def join_command(ctx: CommandContext, quest_id: str, character_name: str):
        result, response = Dosa.dnd.join_quest(ctx.user.id if not character_name else character_name, quest_id)
        await ctx.send(response, ephemeral=True)


    @staticmethod
    @client.command(
        name="leave",
        description="Leave a quest you've joined.",
        options = [
            interactions.Option(
                name="quest_id",
                description="The id of the quest you want to leave.",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def leave_command(ctx: CommandContext, quest_name: str):
        await ctx.send(f"{ctx.author.name} wants to leave quest: {quest_name}! Fill in functionality.")
    
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
        result, response = Dosa.dnd.new_character(character_name, ctx.user.id)
        await ctx.send(response)

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
        await ctx.send(f"{ctx.user.username} wants to play as {character_name}.")
