import asyncio
import datetime as dt

from httpx import AsyncClient

from .models import Asset


class PortfolioManager:
    def __init__(self, initial_balance: float = 0) -> None:
        self._holdings = {}

        self._cash_balance = initial_balance

        self._lock = asyncio.Lock()

        self.last_updated_at = None

    async def buy_asset(
        self,
        symbol: str,
        quantity: float,
        price: float,
    ) -> Asset:
        pass

    async def sell_asset(
        self,
        symbol: str,
        quantity: float,
        price: float,
    ) -> Asset | None:
        async with self._lock:
            if symbol not in self._holdings:
                raise ValueError("Asset not found in holdings")

            if self._holdings[symbol].quantity < quantity:
                raise ValueError("Insufficient quantity in holdings")

            self._holdings[symbol].quantity -= quantity

            self._cash_balance += quantity * price

            self.last_updated_at = dt.datetime.now()

            if self._holdings[symbol].quantity == 0:
                del self._holdings[symbol]

                return None

            return self._holdings[symbol]

    async def get_portfolio_value(self) -> float:
        total = 0

        async with AsyncClient() as client:
            tasks = [
                self._fetch_current_price(client, asset)
                for asset in self._holdings.values()
            ]
            current_prices = await asyncio.gather(*tasks)

            for asset, current_price in zip(self._holdings.values(), current_prices):
                total += asset.quantity * current_price

        return self._cash_balance + total

    @staticmethod
    def _detect_asset_type(symbol: str) -> Asset.Type:
        if symbol.endswith("-USD"):
            return Asset.Type.CRYPTO
        elif symbol.startswith("REAL"):
            return Asset.Type.REAL_ESTATE

        return Asset.Type.STOCK

    @staticmethod
    async def _fetch_current_price(client: AsyncClient, _asset) -> float:
        response = await client.get(
            "https://www.random.org/decimal-fractions/?num=1&dec=8&col=1&format=plain&rnd=new"
        )
        price = float(response.text) * 100

        return price
