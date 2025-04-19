from app.sources.kraken_exchange import KrakenExchange
from app.sources.okx_exchange import OKXExchange
from app.pipelines.ohlc_pipeline import OHLCPipeline
from app.pipelines.ticker_pipeline import TickerPipeline

# from app.pipelines.trades_pipeline import RecentTradesPipeline

PIPELINE_REGISTRATION_MAP = [
    {
        "source": OKXExchange,
        "pipelines": [OHLCPipeline],
        # "runner": "app.runners.scheduler",
        "interval": "*/1 * * * *",
    },
    {
        "source": KrakenExchange,
        "pipelines": [OHLCPipeline, TickerPipeline],
        # "runner": "app.runners.scheduler",
        "interval": "*/1 * * * *",
    },
]
