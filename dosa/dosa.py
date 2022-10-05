import interactions
from interactions import CommandContext

import dosa.toks as toks


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

    def __init__(self, guild_id: str):
        self.guild_id = guild_id

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
        enlist_button = interactions.Button(
            style=interactions.ButtonStyle.DANGER,
            label="Enlist?",
            custom_id="bulletin_enlist_button"
        )
        # TODO: Format quest
        await ctx.send(f"{name}, {descr}", components=enlist_button)

    @staticmethod
    @client.component("bulletin_enlist_button")
    async def bulletin_enlist_response(ctx: CommandContext):
        # TODO: Manage enlisted database
        await ctx.send("You've enlisted!")


    @staticmethod
    @client.command(
        name="echo",
        description="Post a new quest to the bulletin-board",
        options = [
            interactions.Option(
                name="text",
                description="Words to say",
                type=interactions.OptionType.STRING,
                required=True,
            ),
        ],
    )
    async def echo_command(ctx: CommandContext, text: str):
        await ctx.send(f"{text}")
