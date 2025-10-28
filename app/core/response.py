from datetime import datetime
import json
from typing import Any, Optional
from fastapi import Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.dtos.response_dto import AppResponse

def serialize_data(data: Any) -> Any:
    """Recursively serialize data for JSONResponse."""
    if isinstance(data, BaseModel):
        return data.model_dump(by_alias=True)
    elif isinstance(data, list):
        return [serialize_data(item) for item in data]
    elif isinstance(data, dict):
        return {k: serialize_data(v) for k, v in data.items()}
    return data

def format_response(
    success: bool,
    data: Optional[Any] = None,
    message: str = "",
    code: int = 200
) -> JSONResponse:
    if isinstance(data, BaseModel):
        data = data.model_dump(by_alias=True)
    response_dict = {
        "success": success,
        "data": serialize_data(data),
        "message": message,
    }
    response_json = json.dumps(response_dict,indent=4, sort_keys=True, default=str)
    return Response(status_code=code, content=response_json, media_type="application/json")


def success_response(
    data: Optional[Any] = None,
    message: str = "OK",
    code: int = 200,
) -> JSONResponse:
    return format_response(
        success=True, data=data, message=message, code=code
    )


def error_response(
    message: str = "Error",
    code: int = 500,
    data: Optional[Any] = None,
) -> JSONResponse:
    return format_response(
        success=False, data=data, message=message, code=code
    )
