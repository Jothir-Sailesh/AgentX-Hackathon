from fastapi import APIRouter, Depends, HTTPException
from app.models.payloads import MatchRequest, MatchResponse
from app.services.matching_service import MatchingService

router = APIRouter()

@router.post("/", response_model=MatchResponse)
async def match_invoice(
    payload: MatchRequest,
    service: MatchingService = Depends(MatchingService)
):
    try:
        result = await service.process_match(payload)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
