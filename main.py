from contextlib import asynccontextmanager

from fastapi import Body, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from db import Base, add_requests_data, engine, get_user_requests
from gemini_client import get_answer_from_gemini

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    print("All table created")
    yield

app = FastAPI(
        title="AIHub",
        lifespan=lifespan,
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def serve_frontend():
    return FileResponse("index.html")


@app.get("/requests")
def get_my_requests(request: Request):
    user_ip_address = request.client.host if request.client else "unknown"
    print(f"{user_ip_address=}")
    user_requests = get_user_requests(ip_address=user_ip_address)
    return user_requests


@app.post("/requests")
def send_prompt(
    request: Request,
    prompt: str = Body(embed=True),
):
    user_ip_address = request.client.host if request.client else "unknown"
    answer = get_answer_from_gemini(prompt) or ""
    add_requests_data(
        ip_address=user_ip_address,
        promt=prompt,
        response=answer,
    )
    return {"answer": answer}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)