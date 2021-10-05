# Noljaemon

`Noljaemon` is the private bot for the `Noljaeyo` server.

## How to run
> require python 3.9 or higher
> 
1. install dependency
```shell
pip install requirements.txt
```
2. copy `config.example.json` to `.config.json` and edit on your environment.
3. run `main.py`
```shell
python main.py
```

## Development
### How to add new commands?
1. goto `bot.exts`
2. find category what you want to add. if not exist, create one.
3. make class and inheritance `discord.ext.command.Cog`.
4. use `@command.command(name="")` decorator on method.
5. make some method with the interface like this: `def setup(bot)` and call `bot.add_cog(YOURCLASS(bot))`

Here is some example:
```python
class Latency(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(name="핑")
    async def ping(self, ctx: commands.Context) -> None:
        embed = Embed(title="Pong!")
        await ctx.send(embed=embed)

def setup(bot: Bot) -> None:
    """Load the Latency cog."""
    bot.add_cog(Latency(bot))
```
