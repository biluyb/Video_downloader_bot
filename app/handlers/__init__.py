"""Telegram message handlers."""

from app.handlers.start import router as start_router
from app.handlers.help import router as help_router
from app.handlers.callbacks import router as callbacks_router

__all__ = ["start_router", "help_router", "callbacks_router"]
