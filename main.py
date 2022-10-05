import dosa.toks as toks
from dosa.dosa import Dosa

if __name__ == "__main__":
    dosa = Dosa(
        guild_id=toks.guild_id,
    )
    dosa.client.start()
