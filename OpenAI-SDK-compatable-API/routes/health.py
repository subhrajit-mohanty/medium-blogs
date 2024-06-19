from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/health")
async def healthCheck():
    return {"message": "success"}