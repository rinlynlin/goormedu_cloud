import csv
from contextlib import asynccontextmanager
from fastapi import FastAPI

def load_gyul_data():
    with open("./data/gyul.csv","r")as f:
        reader = csv.DictReader(f, delimiter = ",")
        result = {
            int(row.pop("year")):row for row in reader
        }

    return result

gyul_stats = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    global gyul_stats
    gyul_stats = load_gyul_data()

    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return{"message":"Hello, world!"}

@app.get("/stats")
async def gyul_all_stats():
    return gyul_stats

@app.get("/stats/{year}")
async def get_year_stats(year: int):
    return gyul_stats[year]