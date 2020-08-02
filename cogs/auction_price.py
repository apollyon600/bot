from discord.ext import commands

from utils import Embed, get_item_price_stats, get_item_id


class AuctionPrice(commands.Cog, name='Auction'):
    """
    View average prices for items aswell as past auctions for any player.
    """

    emoji = '💸'

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10.0, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
    async def price(self, ctx, *, item_name):
        """
        Displays the average price for any item on the auction.
        """
        item_id = await get_item_id(item_name, session=self.bot.http_session)
        if not item_id:
            return await ctx.send(f'{ctx.author.mention}, There is no item called `{" ".join(item_name)}`.\n'
                                  f'Or there was a problem connecting to https://auctions.craftlink.xyz/.')

        item_price_stats = await get_item_price_stats(item_id[0]['_id'], session=self.bot.http_session)
        if not item_price_stats:
            return await ctx.send(f'{ctx.author.mention}, There is no item called `{" ".join(item_name)}`.\n'
                                  f'Or there was a problem connecting to https://auctions.craftlink.xyz/.')

        _deviation = item_price_stats.get("deviation", 0.00)
        _average = item_price_stats.get("average", 0.00)
        _averageBids = item_price_stats.get("averageBids", 0.00)

        await Embed(
            ctx=ctx,
            title=f'{item_price_stats.get("name", item_name)}'
        ).add_field(
            name='Deviation',
            value=f'```{_deviation or 0.00:.2f}```'
        ).add_field(
            name='Average',
            value=f'```{_average or 0.00:.2f}```'
        ).add_field().add_field(
            name='Median',
            value=f'```{item_price_stats.get("median", 0)}```',
        ).add_field(
            name='Mode',
            value=f'```{item_price_stats.get("mode", 0)}```'
        ).add_field().add_field(
            name='Average bids',
            value=f'```{_averageBids or 0.00:.2f}```'
        ).add_field(
            name='Average quantity',
            value=f'```{item_price_stats.get("averageQuantity", 0)}```'
        ).add_field().add_field(
            name='Total sales',
            value=f'```{item_price_stats.get("totalSales", 0)}```'
        ).add_field(
            name='Total bids',
            value=f'```{item_price_stats.get("totalBids", 0)}```'
        ).add_field().set_footer(
            text='Powered by https://auctions.craftlink.xyz.'
        ).send()


def setup(bot):
    bot.add_cog(AuctionPrice(bot))
