from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from pydantic import BaseModel
from db import Recipe, engine


# DB接続用のセッションクラス インスタンスが作成されると接続する
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Pydanticを用いたAPIに渡されるデータの定義 ValidationやDocumentationの機能が追加される
class RecipeIn(BaseModel):
    title: str
    making_time: str
    serves: str
    ingredients: str
    cost: int


# 単一のTodoを取得するためのユーティリティ
def get_recipe(db_session: Session, recipe_id: int):
    return db_session.query(Recipe).filter(Recipe.id == recipe_id).first()


# DB接続のセッションを各エンドポイントの関数に渡す
def get_db(request: Request):
    return request.state.db


# このインスタンスをアノテーションに利用することでエンドポイントを定義できる
app = FastAPI()


@app.get("/", status_code=404)
def do_nothing():
    return {}


# Recipeの全取得
@app.get("/recipes/")
def read_recipes(db: Session = Depends(get_db)):
    recipes = db.query(Recipe).all()
    return recipes


# 単一のRecipeを取得
@app.get("/recipes/{recipe_id}")
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = get_recipe(db, recipe_id)
    return recipe


# Recipeを登録
@app.post("/recipes/")
async def create_recipe(recipe_in: RecipeIn, db: Session = Depends(get_db)):
    recipe = Recipe(
        title=recipe_in.title,
        making_time=recipe_in.making_time,
        serves=recipe_in.serves,
        ingredients=recipe_in.ingredients,
        cost=recipe_in.cost)
    db.add(recipe)
    db.commit()
    recipe = get_recipe(db, recipe.id)
    return recipe


# Recipeを更新
@app.put("/recipes/{recipe_id}")
async def update_recipe(recipe_id: int, recipe_in: RecipeIn, db: Session = Depends(get_db)):
    recipe = get_recipe(db, recipe_id)
    recipe.title = recipe_in.title
    recipe.done = recipe_in.done
    db.commit()
    recipe = get_recipe(db, recipe_id)
    return recipe


# Todoを削除
@app.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = get_recipe(db, recipe_id)
    db.delete(recipe)
    db.commit()


# リクエストの度に呼ばれるミドルウェア DB接続用のセッションインスタンスを作成
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response
