from typing import Any


def success_response(data: Any = None, message: str = "Success") -> dict:
    return {
        "success": True,
        "data": data if data is not None else {},
        "message": message,
    }


def error_response(message: str, error: str, data: Any = None) -> dict:
    return {
        "success": False,
        "data": data if data is not None else {},
        "message": message,
        "error": error,
    }
