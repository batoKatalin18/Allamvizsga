from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import search  # majd csináljuk meg

app = FastAPI()

# Engedjük a frontendet
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fejlesztéshez
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Regisztráljuk a route-okat
app.include_router(search.router)
