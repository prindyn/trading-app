from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Enum,
    Text,
    UUID,
    func,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, declarative_base
import enum
import uuid

Base = declarative_base()


# -- Enums --


class TradeStatus(str, enum.Enum):
    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class OrderType(str, enum.Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"


# -- Tables --


class Asset(Base):
    __tablename__ = "assets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    image = Column(String, default="")
    is_fiat = Column(Boolean, default=False)


class Exchange(Base):
    __tablename__ = "exchanges"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True)


class TradePair(Base):
    __tablename__ = "trade_pairs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    base_asset_id = Column(UUID, ForeignKey("assets.id"))
    quote_asset_id = Column(UUID, ForeignKey("assets.id"))


class PairAvailability(Base):
    __tablename__ = "pair_availability"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trade_pair_id = Column(UUID, ForeignKey("trade_pairs.id"))
    exchange_id = Column(UUID, ForeignKey("exchanges.id"))
    type = Column(String)  # 'spot' or 'futures'
    is_active = Column(Boolean, default=True)


class Trade(Base):
    __tablename__ = "trades"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, nullable=False)
    platform = Column(String(64), nullable=False)  # e.g., Binance, Coinbase
    symbol = Column(String(32), nullable=False)  # e.g., BTCUSD
    side = Column(String(10), nullable=False)  # BUY or SELL
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=True)  # Null for market orders
    status = Column(Enum(TradeStatus), default=TradeStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    executed_at = Column(DateTime(timezone=True), nullable=True)

    orders = relationship("Order", back_populates="trade", cascade="all, delete")


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trade_id = Column(UUID, ForeignKey("trades.id", ondelete="CASCADE"), nullable=False)
    order_type = Column(Enum(OrderType), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=True)
    placed_at = Column(DateTime(timezone=True), server_default=func.now())

    trade = relationship("Trade", back_populates="orders")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, nullable=True)
    action = Column(String(128), nullable=False)  # e.g., 'TRADE_CREATED'
    details = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class WebhookLog(Base):
    __tablename__ = "webhook_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trade_id = Column(UUID, ForeignKey("trades.id", ondelete="SET NULL"), nullable=True)
    endpoint = Column(String, nullable=False)
    payload = Column(Text, nullable=False)
    response_code = Column(Integer, nullable=True)
    response_body = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PlatformCredential(Base):
    __tablename__ = "platform_credentials"
    __table_args__ = (UniqueConstraint("user_id", "platform", name="uq_user_platform"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, nullable=False)
    platform = Column(String(64), nullable=False)  # e.g., Binance
    api_key = Column(String, nullable=False)
    api_secret = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
