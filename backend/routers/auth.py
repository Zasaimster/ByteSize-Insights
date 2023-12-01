from fastapi import APIRouter
from datetime import date

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("signUp")
async def get_summaries(
    start_time: date,
    end_time: date,
):
    return {"message": f"summaries/filter from {start_time} to {end_time}"}
