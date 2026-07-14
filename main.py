#from fastapi import FastAPI
#from routes.chatbot import router

#app = FastAPI()

#app.include_router(router)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- Import the CORS middleware
from routes.chatbot import router as chatbot_router
from routes.login import router as login_router
from database import Base, engine
from models import ChatbotUser

app = FastAPI()

# Configure CORS Origins - Allow all origins for local development
origins = [
    "https://swiftintelli.com",
    "https://www.swiftintelli.com"
]

# Add the middleware to your FastAPI app instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],         # Allows POST, GET, OPTIONS, etc.
    allow_headers=["*"],         # Allows headers like Content-Type
)

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Include your app routers
app.include_router(chatbot_router)
app.include_router(login_router)