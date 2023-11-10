from fastapi import APIRouter
from datetime import date

router = APIRouter(prefix="/summaries", tags=["summaries"])


@router.get("/filter")
async def get_summaries(
    start_time: date,
    end_time: date,
):
    return {"message": f"summaries/filter from {start_time} to {end_time}"}
