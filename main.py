from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from models import product
from database import engine,session
import database_models
from sqlalchemy.orm import Session

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"]
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")

def greet():
    return "welcome to my environment"

products = [
    product(id=1,name='Phone',description='Low Budget',price=99,quantity=10),
    product(id=2,name='Laptop',description='Gaming Laptop',price=999,quantity=6),
    product(id=3,name='Airpods',description='Perimum airpods',price=999,quantity=12),
    product(id=4,name='Smart Watch',description='High Quality',price=60,quantity=5)
]

def get_db():
    db=session()
    try:
        yield db
    finally :
        db.close()

def init_db():
    db=session()
    count=db.query(database_models.product).count

    if count == 0:

        for product in products:
           db.add(database_models.product(**product.model_dump()))

        db.commit()

init_db()

@app.get("/products")
def Get_All_Product(db:Session = Depends(get_db)):
    db_products = db.query(database_models.product).all()
    return db_products

@app.get("/products/{id}")
def Get_Product_by_ID (id:int,db:Session = Depends(get_db)):
    db_product = db.query(database_models.product).filter(database_models.product.id == id).first()
    if db_product:
        return db_product
    return "Product Not Found"

@app.post("/products")
def Add_Product(product : product,db:Session = Depends(get_db)):
    db.add(database_models.product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products")
def Update_Product(id:int,product : product,db:Session = Depends(get_db)) :
    db_product = db.query(database_models.product).filter(database_models.product.id == id).first()
    if db_product :
        db_product.name = products.name
        db_product.description = products.description
        db_product.PRICE = products.PRICE
        db_product.quantity = products.quantity
        db.commit()
        return "product Updated Successfully"
    else:
         return "No Produte Found"

@app.delete("/products")
def Delete_Product(id: int,db:Session = Depends(get_db)):
    db_product = db.query(database_models.product).filter(database_models.product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted Successfully"
    else:
        return "Product Not Found"