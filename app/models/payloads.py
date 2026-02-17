from pydantic import BaseModel, Field, condecimal
from typing import List, Optional
from datetime import date
from enum import Enum

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"

class LineItem(BaseModel):
    item_id: str
    description: str
    quantity: float = Field(..., gt=0)
    unit_price: condecimal(max_digits=10, decimal_places=2)
    total_amount: condecimal(max_digits=12, decimal_places=2)

class Invoice(BaseModel):
    id: str
    po_number: str
    vendor_id: str
    date: date
    currency: Currency
    items: List[LineItem]
    total_amount: condecimal(max_digits=12, decimal_places=2)

class PurchaseOrder(BaseModel):
    id: str
    vendor_id: str
    items: List[LineItem]
    is_approved: bool

class GoodsReceipt(BaseModel):
    id: str
    po_id: str
    items: List[LineItem]
    received_date: date

class MatchRequest(BaseModel):
    invoice: Invoice
    purchase_order: PurchaseOrder
    goods_receipt: GoodsReceipt

class MatchStatus(str, Enum):
    MATCH = "MATCH"
    MISMATCH = "MISMATCH"
    PARTIAL = "PARTIAL"

class Discrepancy(BaseModel):
    item_id: str
    issue: str
    expected: str
    actual: str

class MatchResponse(BaseModel):
    status: MatchStatus
    confidence_score: float
    discrepancies: List[Discrepancy] = []
    agent_analysis: Optional[str] = None
