import time
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
import pymysql
import mysql.connector

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

    conn = mysql.connector.connect(
   user='root', password='root', host='localhost', database=f'{dbName}',port=3307)
    cursor = conn.cursor()
    # Query the database for the user with the specified username
    items_query = f"SELECT * FROM items WHERE itemNumber='{itemNumber}' AND Branch='{branch}' LIMIT 1"
    items_result =  cursor.execute(items_query)
    Allitems= cursor.fetchall()
    if Allitems:
        for items in Allitems:
            items_row= [str(item) for item in items]
            if items_row:

                    # Extract relevant fields from items_row
                id_value = items_row[0]
                
                itemName_value = items_row[1]
                itemNumber_value = items_row[2]
                description_value = items_row[3]
                
                branch_value = items_row[4]
                quantity_value = items_row[5]
                s1_value = items_row[6]
                s2_value = items_row[7]
                s3_value = items_row[8]
                handQuantity_value = 0
                vat_value = items_row[10]
                if vat_value==None:
                    vat_value=0
                sp_value = items_row[11]
                if sp_value==None:
                    sp_value="" 
        

                costPrice_value = items_row[12]
                if costPrice_value=='None':
                    costPrice_value=0
                image_value = items_row[13]
                if image_value == 'None':
                    image_value=''


                item = {
                    "id":id_value,
                    "itemName": itemName_value,
                    "itemNumber": itemNumber_value,
                    "Description":description_value,
                    "Branch": branch_value,
                    "quantity":quantity_value,
                    "S1": s1_value,
                    "S2": s2_value,
                    "S3": s3_value,
                    "handQuantity":handQuantity_value,
                    "vat": vat_value,
                    "sp": sp_value,
                    "costPrice": costPrice_value,  
                    "image": image_value
                }
        getBranchQunatity=f"""SELECT branch, SUM(quantity) as totalQuantity
FROM items
WHERE itemNumber = {itemNumber}
GROUP BY branch"""
        iq_result =  cursor.execute(getBranchQunatity)
        iq= cursor.fetchall()
        if iq:
        
            item_quantities = [{"branch": b[0], "quantity": b[1]} for b in iq]
        getTotalQunatity=f"""SELECT SUM(quantity) as totalQuantity
    FROM items
    WHERE itemNumber = '{itemNumber}'"""
        it_result =  cursor.execute(getTotalQunatity)
        it= cursor.fetchall()
        if it:
            for tot in it:
                print("total :")
                print(tot)
            totalQunatity=tot[0]
            return {"item":item,"itemQB":item_quantities,"totalQuantity":totalQunatity}             
    else:
        return {"item": "empty"} 



    # totalquantity=0

    # # Check if the user exists and the provided password matches the stored hashed password
    # if item :
    #     items = db.query(models.Items).filter(models.Items.itemNumber == itemNumber).all()
    #     if items:
    #         item_quantities = [{"branch": item.Branch, "quantity": item.quantity} for item in items]
    #         for itemx in items:
    #             totalquantity=totalquantity+itemx.quantity
    #         return {"item":item,"itemQB":item_quantities,"totalQuantity":totalquantity}  
    #     else:
    #         return {"item":item,"itemQB":[],"totalQuantity":totalquantity}  

    #         # Authentication successful
    # else:
    #     return {"item": "empty"}  # Authentication failed

    
@app.post("/handeQuantity_update/")
async def handQuantity_update(itemNumber,handQuantity:int,branch,dbName, inventory,oldHandQuantity:int):
    conn = mysql.connector.connect(
   user='root', password='root', host='localhost', database=f'{dbName}',port=3307)
    cursor = conn.cursor()


    try:

        
        totalHandQuantity=handQuantity+oldHandQuantity

        if totalHandQuantity<0:
            totalHandQuantity=0
        update=f"""UPDATE {inventory} SET handQuantity = {totalHandQuantity}
WHERE itemNumber='{itemNumber}' AND Branch={branch}"""
        r=cursor.execute(update)
        conn.commit()
        return {"status": True, "message": "Hand Quantity updated successfully"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    

    


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
    conn = mysql.connector.connect(
   user='root', password='root', host='localhost', database=f'{dbName}',port=3307)
    cursor = conn.cursor()
    # Query the database for the user with the specified username
    try:
        distinct_branches="SELECT DISTINCT branch FROM items"
        cursor.execute(distinct_branches)
        rows= cursor.fetchall()
        branches = [item[0] for item in distinct_branches]
        print(branches)
        return {"branches": branches}

    except Exception as e:
        print(f"Error: {e}")
        return {"error": "An error occurred while fetching branches"}
    finally:
        conn.close()

@app.get("/getInventories/")
async def list_inventories(dbName,username):
    conn = mysql.connector.connect(
   user='root', password='root', host='localhost', database=f'{dbName}',port=3307)
    cursor = conn.cursor()
    query = f"SELECT table_name FROM information_schema.tables WHERE table_name LIKE '{username}\\_%'"

    try:

        result =  cursor.execute(query)
     
        rows= cursor.fetchall()
        if rows:
            # for name in rows:
            #     print(name[0])
            #     tables_names.append(name[0])
            table_names = [row[0] for row in rows]
            print(table_names)
            return {"status":True,"message": f"Tables starting with '{username}_': {"tabe_names"}","result":table_names}
        else:

            return {"status":False,"message": f"No tables found starting with '{username}_'","result":[]}
    except Exception as e:
        return {"message": f"Error checking tables: {str(e)}"}
    # Query the database for the user with the specified username
    finally:
        conn.close()

@app.get("/getInventoryItem/")
async def list_ItemInventories(itemNumber,branch,dbName,username,inventory):
    conn = mysql.connector.connect(
   user='root', password='root', host='localhost', database=f'{dbName}',port=3307)
    cursor = conn.cursor()


    try:
        query = f"SELECT * FROM {inventory} WHERE itemNumber='{itemNumber}' AND Branch='{branch}' LIMIT 1"
        result =  cursor.execute(query)
        rows = cursor.fetchall()
        conn.commit()
        print(query)
        if rows:
            # for name in rows:
            #     print(name[0])
            #     tables_names.append(name[0])
            for row in rows:
                item = {
                    "id":row[0],
                    "itemName": row[1],
                    "itemNumber": row[2],
                    "Description":row[3],
                    "Branch": row[4],
                    "quantity":row[5],
                    "S1": row[6],
                    "S2": row[7],
                    "S3": row[8],
                    "handQuantity": row[9],
                    "vat": row[10],
                    "sp": row[11],
                    "costPrice": row[12],  
                    "image": row[13]
                }

                return {"status":True,"message":"The item is fetched from the inventory table","item":item}     
        else:
            items_query = f"SELECT * FROM items WHERE itemNumber='{itemNumber}' AND Branch='{branch}' LIMIT 1"
            items_result =  cursor.execute(items_query)
            Allitems= cursor.fetchall()
            if Allitems:
                for items in Allitems:
                    items_row= [str(item) for item in items]
                    if items_row:

                            # Extract relevant fields from items_row
                        id_value = items_row[0]
                        
                        itemName_value = items_row[1]
                        itemNumber_value = items_row[2]
                        description_value = items_row[3]
                        
                        branch_value = items_row[4]
                        quantity_value = items_row[5]
                        s1_value = items_row[6]
                        s2_value = items_row[7]
                        s3_value = items_row[8]
                        handQuantity_value = 0
                        vat_value = items_row[10]
                        if vat_value==None:
                            vat_value=0
                        sp_value = items_row[11]
                        if sp_value==None:
                            sp_value="" 
                
        
                        costPrice_value = items_row[12]
                        if costPrice_value=='None':
                            costPrice_value=0
                        image_value = items_row[13]
                        if image_value == 'None':
                            image_value=''
                        print(image_value)
            
                        table_name=f"{username}_{inventory}"
                        # Insert into john_abc table
                        insert_query = (
                            f"INSERT INTO {inventory} (id, itemName, itemNumber, Description, Branch, quantity, S1, S2, S3, handQuantity, vat, sp, costPrice, image)" 
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        )

                        data = (
                            id_value,
                            itemName_value,
                            itemNumber_value,
                            description_value,
                            branch_value,
                            quantity_value,
                        s1_value,
                            s2_value,
                            s3_value,
                            handQuantity_value,
                            vat_value,
                        sp_value,
                            costPrice_value,
                            image_value
                            
                        )
                        try:
                            res2 = cursor.execute(insert_query, data)
                            conn.commit()

                        except Exception as e:
                            conn.rollback()
                            return {"message": f"Error checking tables: {str(e)}","item":"empty"}
                            


                        
                        try:
                            queryGetItem=f"SELECT * FROM {inventory} WHERE itemNumber=%s AND Branch=%s LIMIT 1"
                            data=(itemNumber,branch)
                            cursor.execute(queryGetItem,data)
                            
                            itemRow= cursor.fetchone()

                            conn.commit()
                            if itemRow:
                                item = {
                                "id":itemRow[0],
                                "itemName": itemRow[1],
                                "itemNumber": itemRow[2],
                                "Description":itemRow[3],
                                "Branch": itemRow[4],
                                "quantity":itemRow[5],
                                "S1": itemRow[6],
                                "S2": itemRow[7],
                                "S3": itemRow[8],
                                "handQuantity": itemRow[9],
                                "vat": itemRow[10],
                                "sp": itemRow[11],
                                "costPrice": itemRow[12], 
                                "image": itemRow[13]
                                }
                                
                                return {"status":True,"message":"The item is fetched from the inventory table","item":item}
                            else:
                                return {"status":False,"message":"The item is not found from the inventory table","item":"empty"}
                            

                        except Exception as e:
                            conn.rollback()
                            return {"message": f"Error in getting item: {str(e)}","item":"empty"}
            else:
                return{"status":False,"item":"empty","message":"not Found in the main table"}

    except Exception as e:
        return {"message": f"Error checking tables: {str(e)}","item":"empty"}
    # Query the database for the user with the specified username
    finally:
        conn.close()


@app.post("/createInventory/")
async def list_ItemInventories(dbName,username,inventory):
    engine=create_engine(f'mysql+pymysql://root:root@localhost:3307/{dbName}')
    SessionLocal= sessionmaker(autocommit=False, autoflush= False, bind=engine)
    db=SessionLocal()
    query = text(f"SELECT table_name FROM information_schema.tables WHERE table_name = '{username}_{inventory}'")


    try:

        result =  db.execute(query)
        row=result.fetchone()
        if row:
            
            return {"status":False,"message": f"Table name already exsists","result":row[0]}
        else:
            print("heyy you can create")
            create_query=text(f"""CREATE TABLE `{username}_{inventory}` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`itemName` VARCHAR(120) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`itemNumber` VARCHAR(200) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`Description` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`Branch` INT(11) NULL DEFAULT NULL,
	`quantity` INT(11) NULL DEFAULT NULL,
	`S1` DOUBLE NULL DEFAULT NULL,
	`S2` DOUBLE NULL DEFAULT NULL,
	`S3` DOUBLE NULL DEFAULT NULL,
	`handQuantity` INT(11) NULL DEFAULT NULL,
	`vat` DOUBLE NULL DEFAULT NULL,
	`sp` VARCHAR(5) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`costPrice` DOUBLE NULL DEFAULT NULL,
    `image` VARCHAR(300) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `id` (`itemNumber`, `Branch`)
)
""")
        create_result =  db.execute(create_query)

        if create_result:
            return {"status":True,"message": f"No tables found starting with '_'","result":[]}
    except Exception as e:
        return {"message": f"Error checking tables: {str(e)}"}
    # Query the database for the user with the specified username
    finally:
        db.close()

