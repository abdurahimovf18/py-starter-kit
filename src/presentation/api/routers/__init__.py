from fastapi import APIRouter

from . import system

router = APIRouter()
router.include_router(system.router)
