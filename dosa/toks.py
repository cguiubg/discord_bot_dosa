import yaml

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

bot_token = config["bot-token"]
guild_id = config["guild-id"]
bulletin_id = config["bulletin-id"]
