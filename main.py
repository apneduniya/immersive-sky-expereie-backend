from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import DBConnection
from contextlib import asynccontextmanager
import os
import dotenv
from routes import upload_image
from services import auth


dotenv.load_dotenv()
ORIGINS = ["*"]
MONGO_CONNECTION_URL = os.getenv("MONGO_CONNECTION_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")
db_connection = DBConnection(MONGO_CONNECTION_URL, DATABASE_NAME)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start Up Event
    db_connection.connect()
    print("\nS E R V E R   S T A R T I N G . . . . . . . . . .\n")
    yield

    # Shut Down Event
    db_connection.disconnect()
    print("\nS E R V E R   S H U T D O W N . . . . . . . . . .\n")



app = FastAPI(
#    docs_url=None, # Disable docs (Swagger UI)
#    redoc_url=None, # Disable redoc
    title="Immersive Sky Expereie API",
    description="API for Immersive Sky Experience",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#  I N C L U D E   R O U T E R S


app.include_router(auth.router, prefix="/user", tags=["USER"])
app.include_router(upload_image.router, prefix="/asset", tags=["ASSET"])


