from fastapi import FastAPI

app = FastAPI()

# Головна сторінка
@app.get("/")
def read_root():
    return {"message": "Привіт, FastAPI!"}

# Динамічний маршрут
@app.get("/hello/{name}")
def read_item(name: str):
    return {"message": f"Привіт, {name}!"}