from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.get("")
async def event_details():
    return {"hello": "world"}
