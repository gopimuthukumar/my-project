from fastapi import FastAPI,Depends
from fastapi import HTTPException
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
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(database_models.product).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")
    return product

@app.post("/products/")
def Add_Product(product : product,db:Session = Depends(get_db)):
    db_product = database_models.product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/products/{id}")
def Update_Product(id: int, product: product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.product)\
                   .filter(database_models.product.id == id)\
                   .first()

    if not db_product:
        raise HTTPException(status_code=404, detail="No Product Found")

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity

    db.commit()
    db.refresh(db_product)

    return {"message": "Product Updated Successfully", "product": db_product}


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.product).filter(database_models.product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product Not Found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product Deleted"}