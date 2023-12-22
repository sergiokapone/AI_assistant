from datetime import datetime

import uvicorn
from database.db_helper import db_helper
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

app = FastAPI(
    debug=True,
    title="Snapshot Exchange",
)

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
    # dependencies=[Depends(RateLimiter(times=2, seconds=5))]
)
async def root():
    return {
        "name": "Snapshot Exchange REST API!",
        "version": "Version 1.0",
        "description": "This API provides access to Snapshot Exchange services.",
        "authors": [
            {
                "name": "Sergiy Ponomarenko (aka sergiokapone)",
                "github": "https://github.com/sergiokapone",
                "additional_info": "Team Lead of Project",
            }
        ],
        "license": "This API is distributed under the MIT License.",
    }


@app.get("/api/healthchecker", tags=["Root"])
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


@app.get("/list", tags=["Root"])
def get_all_urls_from_request(request: Request) -> list[dict]:
    routes = [
        {
            "path": str(request.base_url)[:-1] + route.path,
            "name": route.name,
            "method": route.methods,
            "description": route.description,
        }
        for route in request.app.routes
        if hasattr(route, "description") and route.description is not None
    ]
    return routes


if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 8000
    uvicorn.run(app="main:app", host=HOST, port=PORT, reload=True)
