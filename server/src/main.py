from datetime import datetime

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from .config.settings import settings
from .database.db_helper import db_helper
from .routes.auth import router as auth_router
from .routes.chat import router as chat_router
from .routes.upload_pdf import router as upload_router

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

app = FastAPI(
    debug=True,
    title="AI assistant",
)

app.include_router(auth_router, prefix=f"/{settings.api_prefix}")
app.include_router(chat_router, prefix=f"/{settings.api_prefix}")
app.include_router(upload_router, prefix=f"/{settings.api_prefix}")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get(
    "/",
    tags=["Root"],
    include_in_schema=False,
)
async def root():
    return {
        "name": "AI Assistant",
        "version": "Version 1.0",
        "description": "This API provides access to AI Assistant services.",
        "license": "This API is distributed under the MIT License.",
    }


@app.get(f"/{settings.api_prefix}/healthchecker", tags=["Root"])
async def healthchecker(session: AsyncSession = Depends(db_helper.session_dependency)):
    try:
        result = await session.execute(text("SELECT 1"))
        rows = result.fetchall()
        if not rows:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database Connection Error",
            )

        return {
            "status": "healthy",
            "message": "You successfully connected to the database!",
            "server_time": current_time,
        }

    except Exception as e:
        raise e


if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 8000
    uvicorn.run(app, host=HOST, port=PORT, reload=True)
