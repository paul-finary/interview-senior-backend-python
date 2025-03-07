import pytest

from app.portfolio import PortfolioManager


@pytest.mark.asyncio
async def test_buy_asset():
    pass


@pytest.mark.asyncio
async def test_sell_asset():
    portfolio = PortfolioManager(1000)

    await portfolio.buy_asset("AAPL", 5, 150)

    # Test sell transaction
    await portfolio.sell_asset("AAPL", 3, 170)

    assert "AAPL" in portfolio._holdings
    assert portfolio._holdings["AAPL"].quantity == 2


@pytest.mark.asyncio
async def test_invalid_sell_asset():
    portfolio = PortfolioManager()

    with pytest.raises(ValueError):
        await portfolio.sell_asset("AAPL", 2, 180)
