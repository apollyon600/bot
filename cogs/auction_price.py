from discord.ext import commands

from utils import Embed, get_item_price_stats, get_item_list


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
        item_list = await get_item_list(item_name, session=self.bot.http_session)
        if not item_list:
            return await ctx.send(f'{ctx.author.mention}, There is no item called `{" ".join(item_name)}`.\n'
                                  f'Or there was a problem connecting to https://auctions.craftlink.xyz/.')

        filtered_item_list = [item.get('_source', {}).get('name', None) for item in item_list[:5]]
        ans = await ctx.prompt_with_list(filtered_item_list, per_page=5,
                                         title='Which item do you want to check price?',
                                         footer='You may enter the corresponding item number.')

        item_id = item_list[ans - 1]

        item_price_stats = await get_item_price_stats(item_id['_id'], session=self.bot.http_session)
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
