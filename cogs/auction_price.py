from discord.ext import commands

from lib import get_item_price_stats, get_item_id
from utils import Embed


class AuctionPrice(commands.Cog, name='Auction'):
    """
    View average prices for items aswell as past auctions for any player.
    """

    emoji = '💸'

    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session

    @commands.command()
    async def price(self, ctx, *, item_name):
        """
        Displays the average price for any item on the auction.
        """
        item_id = await get_item_id(item_name, session=self.session)
        if not item_id:
            return await ctx.send(f'{ctx.author.mention}, There is no item called `{" ".join(item_name)}`.\n'
                                  f'Or there was a problem connecting to https://auctions.craftlink.xyz/.')

        item_price_stats = await get_item_price_stats(item_id[0]['_id'], session=self.session)
        if not item_price_stats:
            return await ctx.send(f'{ctx.author.mention}, There is no item called `{" ".join(item_name)}`.\n'
                                  f'Or there was a problem connecting to https://auctions.craftlink.xyz/.')

        await Embed(
            ctx=ctx,
            title=f'{item_price_stats["name"]}'
        ).add_field(
            name='Deviation',
            value=f'```{item_price_stats["deviation"]:.2f}```'
        ).add_field(
            name='Average',
            value=f'```{item_price_stats["average"]:.2f}```'
        ).add_field().add_field(
            name='Median',
            value=f'```{item_price_stats["median"]}```',
        ).add_field(
            name='Mode',
            value=f'```{item_price_stats["mode"]}```'
        ).add_field().add_field(
            name='Average bids',
            value=f'```{item_price_stats["averageBids"]:.2f}```'
        ).add_field(
            name='Average quantity',
            value=f'```{item_price_stats["averageQuantity"]}```'
        ).add_field().add_field(
            name='Total sales',
            value=f'```{item_price_stats["totalSales"]}```'
        ).add_field(
            name='Total bids',
            value=f'```{item_price_stats["totalBids"]}```'
        ).add_field().set_footer(
            text='Powered by https://auctions.craftlink.xyz'
        ).send()


def setup(bot):
    bot.add_cog(AuctionPrice(bot))
