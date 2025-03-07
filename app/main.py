import datetime as dt

from fastapi import FastAPI, HTTPException
from httpx import AsyncClient

from .portfolio import PortfolioManager
from .schemas import AssetSchema
from .models import Asset

app = FastAPI()

portfolio_manager = PortfolioManager(1000.0)


async def record_audit_log(action: str, symbol: str, quantity: float) -> None:
    async with AsyncClient(timeout=10) as client:
        response = await client.get(
            "https://baconipsum.com/api/?type=meat-and-filler&sentences=1"
        )
        response.raise_for_status()
        audit_comment = response.json()[0]

    print(
        f"AUDIT LOG - Action: {action}, Symbol: {symbol}, Quantity: {quantity}, Comment: {audit_comment}"
    )


@app.post("/buy")
async def buy(body):
    pass


@app.post("/sell")
async def sell(body: AssetSchema) -> dict[str, str | Asset | None]:
    try:
        asset_holding = await portfolio_manager.sell_asset(
            body.symbol,
            body.quantity,
            body.price,
        )

        await record_audit_log("sell", body.symbol, body.quantity)

        return {
            "status": "success",
            "asset": asset_holding,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/portfolio")
async def get_portfolio() -> dict[str, dict[str, Asset] | float | dt.datetime | None]:
    holdings = portfolio_manager._holdings
    total_value = await portfolio_manager.get_portfolio_value()
    last_updated_at = portfolio_manager.last_updated_at

    return {
        "holdings": holdings,
        "total_value": total_value,
        "last_updated_at": last_updated_at,
    }
