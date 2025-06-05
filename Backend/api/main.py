from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import search, upload, stats_routes 

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
app.include_router(upload.router)
app.include_router(stats_routes.router)