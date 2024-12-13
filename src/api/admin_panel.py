from fastapi import APIRouter, Depends
from src.services.auth import get_current_admin_user
from src.database.models import User

router = APIRouter(prefix="/admin_panel", tags=["admin_panel"])


@router.get("/admin")
def read_admin(current_user: User = Depends(get_current_admin_user)):
    return {"message": f"Вітаємо, {current_user.username}! Це адміністративний маршрут"}
