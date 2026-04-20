from fastapi import APIRouter

router = APIRouter()

@router.post("/models/upload")
async def upload_model():
    pass

@router.get("/models")
async def list_models():
    pass

@router.get("/models/{id}")
async def get_model(id: int):
    pass

@router.delete("/models/{id}")
async def delete_model(id: int):
    pass
