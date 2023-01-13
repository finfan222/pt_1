import uvicorn
from fastapi import FastAPI
from database import *
from sqlalchemy.orm import Session
from sqlalchemy import select

app = FastAPI()

DEFAULT_WAY: str = "/";


@app.get(DEFAULT_WAY)
async def root():
    return {"message": "Hello World"}


@app.post(DEFAULT_WAY + "api/v1/menus")
async def createMenu(name: str = 'My menu 1', description: str = 'My menu description 1'):
    with Session(engine) as session:
        menu = Menu(
            name=name,
            description=description,
            submenus=[
                SubMenu(
                    name="MySubMenu",
                    dishes=[
                        Dish(
                            name="Курица с говном",
                            price=500,
                            weight=150
                        )
                    ]
                )
            ]
        )
        session.add(menu)
        session.commit()


@app.get(DEFAULT_WAY + "api/v1/menus")
async def getMenus():
    with Session(engine) as session:
        stmt = select(Menu).where(Menu.id.in_(["spongebob", "sandy"]))


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
