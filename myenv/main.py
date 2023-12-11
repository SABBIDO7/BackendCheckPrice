import bcrypt
from passlib.context import CryptContext
from fastapi import FastAPI, Depends, HTTPException,status
from pydantic import BaseModel
from typing import Annotated
import models
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import hashlib
from sqlalchemy import create_engine,func,text
from sqlalchemy.orm import sessionmaker

app = FastAPI()


# Allow all origins for testing; specify actual origins in production

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a global variable to store the database URL

global global_database_url 


# @app.post("/dbName/",status_code=status.HTTP_201_CREATED)
# def get_database_url(db_name):
#     # Assuming you have a default database URL here
#     # Modify this function to construct the URL based on the provided db_name
#     global_database_url = f'mysql+pymysql://root:root@localhost:3307/{db_name}'
#     return global_database_url



# def get_db(global_database_url):
#     db = SessionLocal(global_database_url)
#     print("ana ble getdb"+global_database_url)
#     try:
#         yield db
#     finally:
#         db.close()

# db_dependency=Annotated[Session,Depends(get_db)]

# Define a CryptContext for password hashing
#password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#models.Base.metadata.create_all(bind=engine)




@app.post("/Checkuser/",status_code=status.HTTP_201_CREATED)
async def authenticate_user(username, password, branch,dbName):
    try:
        print("falcommmmm");   # Query the database for the user with the specified username
        engine=create_engine(f'mysql+pymysql://root:root@localhost:3307/{dbName}')
        SessionLocal= sessionmaker(autocommit=False, autoflush= False, bind=engine)

        db = SessionLocal()
    
        user = db.query(models.Users).filter(models.Users.username == username,models.Users.branch==branch).first()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print(hashed_password)
        print(user.username)
        print(user.password)
        # Check if the user exists and the provide
        # d password matches the stored hashed password
        if user and user.password==hashed_password:
            return {"status":True}  # Authentication successful
        else:
            return {"status":False}  # Authentication failed
    except Exception as e:
        # Handle the error when the database doesn't exist
        return {"status": False, "error": "Database does not exist or connection failed"}
    finally:
        db.close()  # Close the database connection
@app.post("/postUser/",status_code=status.HTTP_201_CREATED)
async def create_users():
# List of Governorates in Lebanon

    username = "yara"  # Replace with the username you want to authenticate
# Hashing the password during user creation
    password = "secret_password" 
    try:
        engine=create_engine(f'mysql+pymysql://root:root@localhost:3307/fluttercheckprice')
        SessionLocal= sessionmaker(autocommit=False, autoflush= False, bind=engine)

        db = SessionLocal()
     
        db_usr = models.Users(username=username,password=password)
        db.add(db_usr)

        db.commit()
        return {"status": "user added successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error adding user")

# @app.post("/createItems/",status_code=status.HTTP_201_CREATED)
# async def create_item(db: db_dependency):
#     # Create an instance of the Item model

#     try:
        
     
#         db_usr = models.Items(   itemName="Water",
#     itemNumber="123456",
#     Description="Sohat",
#     Branch=1,
#     quantity=5,
#     S1=10.00,
#     S2=10.00,
#     S3=10.00,
# )
#         db.add(db_usr)

#         db.commit()
#         return {"Status": "item added"}
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=400, detail="Error adding item")
    


@app.get("/getItem/")
async def authenticate_user(itemNumber,branch,dbName):

    engine=create_engine(f'mysql+pymysql://root:root@localhost:3307/{dbName}')
    models.Base.metadata.create_all(bind=engine)

    SessionLocal= sessionmaker(autocommit=False, autoflush= False, bind=engine)

    db=SessionLocal()
    # Query the database for the user with the specified username

    item = db.query(models.Items).filter(models.Items.itemNumber == itemNumber,models.Items.Branch==branch).first()
    totalquantity=0

    # Check if the user exists and the provided password matches the stored hashed password
    if item :
        items = db.query(models.Items).filter(models.Items.itemNumber == itemNumber).all()
        if items:
            item_quantities = [{"branch": item.Branch, "quantity": item.quantity} for item in items]
            for itemx in items:
                totalquantity=totalquantity+itemx.quantity
            return {"item":item,"itemQB":item_quantities,"totalQuantity":totalquantity}  
        else:
            return {"item":item,"itemQB":[],"totalQuantity":totalquantity}  

            # Authentication successful
    else:
        return {"item": "empty"}  # Authentication failed

    
@app.post("/handeQuantity_update/")
async def handQuantity_update(itemNumber,handQuantity,branch,dbName):
    engine=create_engine(f'mysql+pymysql://root:root@localhost:3307/{dbName}')
    SessionLocal= sessionmaker(autocommit=False, autoflush= False, bind=engine)
    db=SessionLocal()
    # Query the database for the user with the specified username
    item = db.query(models.Items).filter(models.Items.itemNumber == itemNumber,models.Items.Branch==branch).first()
    # Check if the item exists
    if item:
        try:
            # Update the handQuantity for the item
            item.handQuantity = handQuantity
            db.commit()
            return {"status": True, "message": "Hand Quantity updated successfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    else:
        return {"status": False, "message": "Item not found"}
    

    


@app.post("/updateBranch/", status_code=status.HTTP_201_CREATED)
async def change_branch(username, password, newbranch, dbName):
    # Query the database for the user with the specified username
    engine = create_engine(f'mysql+pymysql://root:root@localhost:3307/{dbName}')
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    try:
        db = SessionLocal()

        user = db.query(models.Users).filter(models.Users.username == username).first()

        # Check if the user exists and the provided password matches the stored hashed password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if user and user.password == hashed_password:
            checkBranch = db.query(models.Items).filter(models.Items.Branch == newbranch).first()
            if checkBranch:
                user.branch = newbranch
                db.commit()
                return {"status": "True"}  # Authentication successful
            else:
                return {"status": "noBranchFound"}
        else:
            return {"status": "False"}  # Authentication failed
    except Exception as e:
        return {"status": "Error", "message": str(e)}
    finally:
        db.close()



@app.get("/getBranches/")
async def list_branches(dbName):
    engine=create_engine(f'mysql+pymysql://root:root@localhost:3307/{dbName}')
    SessionLocal= sessionmaker(autocommit=False, autoflush= False, bind=engine)
    db=SessionLocal()
    # Query the database for the user with the specified username
    try:
        distinct_branches = db.query(func.distinct(models.Items.Branch)).all()
        branches = [item[0] for item in distinct_branches]
        print(branches)
        return {"branches": branches}

    except Exception as e:
        print(f"Error: {e}")
        return {"error": "An error occurred while fetching branches"}
    finally:
        db.close()

@app.get("/getInventories/")
async def list_inventories(dbName,username):
    engine=create_engine(f'mysql+pymysql://root:root@localhost:3307/{dbName}')
    SessionLocal= sessionmaker(autocommit=False, autoflush= False, bind=engine)
    db=SessionLocal()
    query = text(f"SELECT table_name FROM information_schema.tables WHERE table_name LIKE '{username}\\_%'")

    try:

        result =  db.execute(query)
     
        rows= result.fetchall()
        if result:
            # for name in rows:
            #     print(name[0])
            #     tables_names.append(name[0])
            table_names = [row[0] for row in rows]
            print(table_names)
            return {"status":True,"message": f"Tables starting with '{username}_': {"tabe_names"}","result":table_names}
        else:
            print("heyy")

            return {"status":False,"message": f"No tables found starting with '{username}_'","result":[]}
    except Exception as e:
        return {"message": f"Error checking tables: {str(e)}"}
    # Query the database for the user with the specified username
    finally:
        db.close()

@app.get("/getItemInventories/")
async def list_ItemInventories(dbName,inventory):
    engine=create_engine(f'mysql+pymysql://root:root@localhost:3307/{dbName}')
    SessionLocal= sessionmaker(autocommit=False, autoflush= False, bind=engine)
    db=SessionLocal()
    query = text(f"SELECT table_name FROM information_schema.tables WHERE table_name = {inventory}")

    try:

        result =  db.execute(query)
     
        rows= result.fetchall()
        if result:
            # for name in rows:
            #     print(name[0])
            #     tables_names.append(name[0])
            table_names = [row[0] for row in rows]
            print(table_names)
            return {"status":True,"message": f"Tables starting with '_': {"tabe_names"}","result":table_names}
        else:
            print("heyy")

            return {"status":False,"message": f"No tables found starting with '_'","result":[]}
    except Exception as e:
        return {"message": f"Error checking tables: {str(e)}"}
    # Query the database for the user with the specified username
    finally:
        db.close()