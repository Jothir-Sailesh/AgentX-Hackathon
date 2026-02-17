from app.models.payloads import MatchRequest, MatchResponse, MatchStatus, Discrepancy

class ThreeWayValidator:
    def validate(self, request: MatchRequest) -> MatchResponse:
        discrepancies = []
        
        # Simple total amount check (naive implementation)
        # In production this would check line-by-line tolerance
        inv_total = request.invoice.total_amount
        po_total = sum(item.total_amount for item in request.purchase_order.items)
        
        if inv_total != po_total:
             discrepancies.append(Discrepancy(
                 item_id="TOTAL",
                 issue="Total amount mismatch",
                 expected=str(po_total),
                 actual=str(inv_total)
             ))

        # Check PO Number
        if request.invoice.po_number != request.purchase_order.id:
             discrepancies.append(Discrepancy(
                 item_id="HEADER",
                 issue="PO Number mismatch",
                 expected=request.purchase_order.id,
                 actual=request.invoice.po_number
             ))

        status = MatchStatus.MISMATCH if discrepancies else MatchStatus.MATCH
        
        return MatchResponse(
            status=status,
            confidence_score=1.0 if status == MatchStatus.MATCH else 0.0,
            discrepancies=discrepancies
        )
