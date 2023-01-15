import uvicorn
from fastapi import FastAPI, Response
from database import *
from sqlalchemy.orm import Session
from sqlalchemy import update
from sqlalchemy import select
from sqlalchemy import insert

app = FastAPI()

DEFAULT_WAY: str = "/";


@app.get(DEFAULT_WAY)
async def root():
    return {"message": "Hello World"}


# Создает меню
@app.post(DEFAULT_WAY + "api/v1/menus")
async def create_menu(name: str = 'My menu 1', description: str = 'My menu description 1'):
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
        return menu


# Просматривает список меню
@app.get(DEFAULT_WAY + "api/v1/menus")
async def menu_list():
    all_menus: list = list()
    with Session(engine) as session:
        for next_menu in session.query(Menu):
            all_menus.append(next_menu)
        return all_menus


# Просматривает определенное меню
@app.get(DEFAULT_WAY + "api/v1/menus/{target_menu_id}")
async def get_menu(target_menu_id: int):
    with Session(engine) as session:
        for next_menu in session.query(Menu).where(Menu.id == target_menu_id):
            return next_menu


# Обновляет меню
@app.patch(DEFAULT_WAY + "api/v1/menus/{target_menu_id}")
async def update_menu(target_menu_id: int):
    update_stmt = (
        update(Menu)
        .where(Menu.id == target_menu_id)
        .values(name="Patrick the Star")
        .returning(Menu.id, Menu.name, Menu.description)
    )
    return update_stmt

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
