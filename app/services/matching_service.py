from app.models.payloads import MatchRequest, MatchResponse, MatchStatus
from app.validators.three_way_validator import ThreeWayValidator
from app.agents.matcher_agent import MatcherAgent

class MatchingService:
    def __init__(self):
        self.validator = ThreeWayValidator()
        self.agent = MatcherAgent()

    async def process_match(self, request: MatchRequest) -> MatchResponse:
        # Step 1: Deterministic Validation
        validation_result = self.validator.validate(request)
        
        if validation_result.status == MatchStatus.MATCH:
            return validation_result
            
        # Step 2: Agentic Analysis for Mismatches
        # If there are discrepancies, use the agent to analyze them (e.g. strict string matching failed, but semantic match might pass)
        agent_result = await self.agent.analyze_discrepancy(request, validation_result)
        
        return agent_result
