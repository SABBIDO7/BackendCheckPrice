import base64
from annotated_types import UpperCase
from fastapi import FastAPI, HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import mysql.connector
from datetime import datetime

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/Checkuser/",status_code=status.HTTP_201_CREATED)
async def authenticate_user(username, branch,dbName):
    try:
        print("falcommmmm");   # Query the database for the user with the specified username
        conn = mysql.connector.connect(
   user='root', password='root', host='localhost', database=f'{dbName}',port=3307)
        cursor = conn.cursor()

        return {"status":True}
    except Exception as e:
        # Handle the error when the database doesn't exist
        return {"status": False, "error": "Database does not exist or connection failed"}
    finally:
        conn.close()

    
@app.get("/getItem/")
async def authenticate_user(itemNumber,branch,dbName):

    conn = mysql.connector.connect(
   user='root', password='root', host='localhost', database=f'{dbName}',port=3307)
    cursor = conn.cursor()
    
    # Query the database for the user with the specified username
    items_query = f"""SELECT * FROM DC_items WHERE itemNumber=UPPER('{itemNumber}') LIMIT 1"""
    items_result =  cursor.execute(items_query)
    Allitems= cursor.fetchall()
    if Allitems:
        for items in Allitems:
            items_row= [str(item) for item in items]
            if items_row:

                    # Extract relevant fields from items_row
               
                
                itemName_value = items_row[2]
                itemNumber_value = items_row[0]
                goid_value = items_row[1]
                
                branch_value = items_row[3]
                quantity_value = items_row[4]
                s1_value = items_row[5]
                s2_value = items_row[6]
                s3_value = items_row[7]
                handQuantity_value = 0
                vat_value = items_row[9]
                if vat_value=="None":
                    vat_value=0
                sp_value = items_row[10]
                if sp_value=="None":
                    sp_value="" 
        

                costPrice_value = items_row[11]
                if costPrice_value=='None':
                    costPrice_value=0
                image_value = items_row[12]
                if image_value == 'None':
                    image_value=''


                else:
                    try:
                        with open(image_value,"rb") as image_file:
                            image_binary = image_file.read()
                            image_base64 = base64.b64encode(image_binary).decode("utf-8")
                            image_value=image_base64
                    except :
                        image_value=''

                disc1_value=items_row[13]
                if disc1_value=='None':
                    disc1_value=0
                disc2_value=items_row[14]
                if disc2_value=='None':
                    disc2_value=0
                disc3_value=items_row[15]
                if disc3_value=='None':
                    disc3_value=0
                qUnit_value=items_row[16]
                if qUnit_value=='None':
                    qUnit_value=0
                item = {
                    
                    "itemName": itemName_value,
                    "itemNumber": itemNumber_value,
                    "GOID":goid_value,
                    "Branch": branch_value,
                    "quantity":quantity_value,
                    "S1": s1_value,
                    "S2": s2_value,
                    "S3": s3_value,
                    "handQuantity":handQuantity_value,
                    "vat": vat_value,
                    "sp": sp_value,
                    "costPrice": costPrice_value,  
                    "image": image_value,
                    "Disc1": float(disc1_value),
                    "Disc2": float(disc2_value),
                    "Disc3": float(disc3_value),
                    "Qunit": float(qUnit_value)
                }
        getBranchQunatity=f"""SELECT branch, SUM(quantity) as totalQuantity
FROM DC_items
WHERE itemNumber = UPPER('{itemNumber}') GROUP BY branch"""
        iq_result =  cursor.execute(getBranchQunatity)
        iq= cursor.fetchall()
        if iq:
        
            item_quantities = [{"branch": b[0], "quantity": b[1]} for b in iq]
            branches_number = len(item_quantities)
            print(branches_number)
        getTotalQunatity=f"""SELECT SUM(quantity) as totalQuantity
    FROM DC_items
    WHERE itemNumber = UPPER('{itemNumber}')"""
        it_result =  cursor.execute(getTotalQunatity)
        it= cursor.fetchall()
        if it:
            for tot in it:
                print("total :")
                print(tot)
            totalQunatity=tot[0]
            print(item)
            return {"item":item,"itemQB":item_quantities,"totalQuantity":totalQunatity,"branches_number":branches_number}             
    else:
        return {"item": "empty"} 


    
@app.post("/handeQuantity_update/")
async def handQuantity_update(itemNumber,handQuantity:float,branch,dbName, inventory,oldHandQuantity:float):
    conn = mysql.connector.connect(
   user='root', password='root', host='localhost', database=f'{dbName}',port=3307)
    cursor = conn.cursor()


    try:

        
        totalHandQuantity=handQuantity+oldHandQuantity

        print(totalHandQuantity)
        update=f"""UPDATE {inventory} SET handQuantity = {totalHandQuantity}
WHERE itemNumber=UPPER('{itemNumber}')"""
        print(update)
        r=cursor.execute(update)
        conn.commit()
        return {"status": True, "message": "Hand Quantity updated successfully"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    

    


@app.post("/updateBranch/", status_code=status.HTTP_201_CREATED)
async def change_branch(username, password, newbranch, dbName):
    # Query the database for the user with the specified username
    conn = mysql.connector.connect(
   user='root', password='root', host='localhost', database=f'{dbName}',port=3307)
    cursor = conn.cursor()

    try:

        # Check if the user exists and the provided password matches the stored hashed password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print("nnn")
        print(newbranch)
        checkBranch=f"""SELECT * FROM DC_items WHERE Branch='{newbranch}' LIMIT 1"""
        r=cursor.execute(checkBranch)
        print("kkk")
        it= cursor.fetchall()
        conn.commit()
        print("ds")
        if it:
            print("salammm")
            update=f"""UPDATE DC_users SET branch = '{newbranch}'
WHERE username='{username}' AND password='{hashed_password}'"""
            r=cursor.execute(update)
            conn.commit()
            return {"status": "True"}
        else:
            return {"status": "noBranchFound"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
               
    finally:
        conn.close()



@app.get("/getBranches/")
async def list_branches(dbName):
    conn = mysql.connector.connect(
   user='root', password='root', host='localhost', database=f'{dbName}',port=3307)
    cursor = conn.cursor()
    # Query the database for the user with the specified username
    try:
        distinct_branches="SELECT DISTINCT branch FROM DC_items"
        cursor.execute(distinct_branches)
        rows= cursor.fetchall()
        branches = [item[0] for item in rows]
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
    query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{dbName}' AND table_name LIKE UPPER('DC_{username}\\_%')"

    try:

        result =  cursor.execute(query)
     
        rows= cursor.fetchall()
        if rows:


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
    print(inventory)

    try:
        query = f"""SELECT * FROM {inventory} WHERE itemNumber=UPPER('{itemNumber}')AND Branch=UPPER('{branch}') LIMIT 1"""
        print(query)

        cursor.execute(query)


        rows = cursor.fetchall()
        conn.commit()
        print(query)
        if rows:


            for row in rows:
                try:

                    with open(row[12],"rb") as image_file:
                        image_binary = image_file.read()
                        image_base64 = base64.b64encode(image_binary).decode("utf-8")
                        image_value=image_base64

                except :
                    image_value=''
                    print('henege')
                item = {
                    "itemName": row[2],
                    "itemNumber": row[0],
                    "GOID":row[1],
                    "Branch": row[3],
                    "quantity":row[4],
                    "S1": row[5],
                    "S2": row[6],
                    "S3": row[7],
                    "handQuantity": row[8],
                    "vat": row[9],
                    "sp": row[10],
                    "costPrice": row[11],  
                    "image": image_value,
                    "Disc1":row[13],
                    "Disc2":row[14],
                    "Disc3":row[15],
                    "Qunit":row[16]
                }
                print(item)
                return {"status":True,"message":"The item is fetched from the inventory table","item":item}     
        else:
            ifound='1'

            items_query = f"""SELECT * FROM DC_items WHERE itemNumber=UPPER('{itemNumber}') AND Branch=UPPER('{branch}') LIMIT 1"""
    
            items_result =  cursor.execute(items_query)
            Allitems= cursor.fetchall()
            if Allitems==[]:
                ifound='2'
                items_query = f"""SELECT * FROM DC_items WHERE itemNumber=UPPER('{itemNumber}') LIMIT 1"""
    
            items_result =  cursor.execute(items_query)
            Allitems= cursor.fetchall()

            if Allitems:
                print("sahih")
                for items in Allitems:
                    items_row= [str(item) for item in items]
                    if items_row:         
                        itemName_value = items_row[2]
                        itemNumber_value = items_row[0]
                        goid_value = items_row[1]
                        branch_value= branch
                        if ifound=='1':
                            quantity_value = items_row[4]
                        else:
                            quantity_value=0
                        s1_value = items_row[5]
                        s2_value = items_row[6]
                        s3_value = items_row[7]
                        handQuantity_value = 0
                        vat_value = items_row[9]
                        if vat_value=='None':
                            vat_value=0
                        sp_value = items_row[10]
                        if sp_value=='None':
                            sp_value="" 
                
        
                        costPrice_value = items_row[11]
                        if costPrice_value=='None':
                            costPrice_value=0
                        image_value = items_row[12]

                        if image_value == 'None':
                            print('kkkkk')
                            image_value=''
                        Disc1=items_row[13]
                        Disc2=items_row[14]
                        Disc3=items_row[15]
                        Qunit=items_row[16]
                        if Qunit=='None':
                            Qunit=0
                   
                            

                        
                        
                        
                        

            
                        table_name=f"{username}_{inventory}"
                        # Insert into john_abc table
                        print(inventory)
                        print(itemNumber_value)
                        print(image_value)
                        print("mNTahhhhhhh")
                        insert_query = (
                            f"INSERT INTO {inventory} (itemName, itemNumber, GOID, Branch, quantity, S1, S2, S3, handQuantity, vat, sp, costPrice, image, Disc1, Disc2, Disc3, Qunit)" 
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        )
                        print(insert_query)
                        print("rtf")
                        data = (
                        itemName_value,
                        itemNumber_value,
                        goid_value,
                        branch_value,
                        quantity_value,
                        s1_value,
                        s2_value,
                        s3_value,
                        handQuantity_value,
                        vat_value,
                        sp_value,
                        costPrice_value,
                        image_value,
                        Disc1,
                        Disc2,
                        Disc3,
                        Qunit
                        )
                        print(insert_query)
                        try:
                            print('llll')
                            print(insert_query)
                            res2 = cursor.execute(insert_query, data)
                            conn.commit()
                            

                        except Exception as e:
                            conn.rollback()
                            return {"message": f"Error checking tables: {str(e)}","item":"empty"}
                            


                        
                        try:
                            queryGetItem=f"SELECT * FROM {inventory} WHERE itemNumber=%s AND Branch=%s LIMIT 1"
                            data=(itemNumber.upper(),branch.upper())
                            print("hkm")
                            
                            cursor.execute(queryGetItem,data)
                            print(queryGetItem)
                            itemRow= cursor.fetchone()
                            print("sde")
                            conn.commit()
                            if itemRow:
                                print("eeee")
                                try:
                                    with open(image_value,"rb") as image_file:
                                        image_binary = image_file.read()
                                        image_base64 = base64.b64encode(image_binary).decode("utf-8")
                                        image_value=image_base64
                                except:
                                    image_value=''
                                print("ssssss")
                                item = {
                                
                                "itemName": itemRow[2],
                                "itemNumber": itemRow[0],
                                "GOID":itemRow[1],
                                "Branch": itemRow[3],
                                "quantity":itemRow[4],
                                "S1": itemRow[5],
                                "S2": itemRow[6],
                                "S3": itemRow[7],
                                "handQuantity": itemRow[8],
                                "vat": itemRow[9],
                                "sp": itemRow[10],
                                "costPrice": itemRow[11], 
                                "image": image_value,
                                "Disc1":itemRow[13],
                                "Disc2":itemRow[14],
                                "Disc3":itemRow[15],
                                "Qunit":itemRow[16]
                                }
                                print(item)    
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
async def create_Inventory(dbName,username,inventory):
    conn = mysql.connector.connect(
   user='root', password='root', host='localhost', database=f'{dbName}',port=3307)
    cursor = conn.cursor()

    query = f"""SELECT table_name FROM information_schema.tables WHERE table_schema = '{dbName}' AND table_name like UPPER('DC_{username}_{inventory}%')"""
    current_datetime = datetime.now()
    print(query)
    abbreviated_day = current_datetime.strftime("%a")[:2]
    formatted_datetime = current_datetime.strftime(f"{abbreviated_day}%Y%m%d_%H%M%S")
    print(formatted_datetime)

    try:

        result =  cursor.execute(query)
        rows = cursor.fetchall()
        conn.commit()
        if rows:
            print("fet")
            for row in rows:
                table_name=row[0]
                print("hohohoho")
                print(table_name)
            
                return {"status":False,"message": f"Table name already exsists","result":table_name}
        else:
            print("heyy you can create")
            username=username.upper()
            inventory=inventory.upper()
            formatted_datetime=formatted_datetime.upper()
            print(username)
            create_query=f"""CREATE TABLE `DC_{username}_{inventory}_{formatted_datetime}` (
	`itemNumber` VARCHAR(20) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`GOID` VARCHAR(20) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`itemName` VARCHAR(120) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`Branch` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`quantity` DOUBLE NULL DEFAULT NULL,
	`S1` DOUBLE NULL DEFAULT NULL,
	`S2` DOUBLE NULL DEFAULT NULL,
	`S3` DOUBLE NULL DEFAULT NULL,
	`handQuantity` DOUBLE NULL DEFAULT NULL,
	`vat` DOUBLE NULL DEFAULT NULL,
	`sp` VARCHAR(5) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`costPrice` DOUBLE NULL DEFAULT NULL,
	`image` VARCHAR(150) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
    `Disc1` DOUBLE NULL DEFAULT NULL,
	`Disc2` DOUBLE NULL DEFAULT NULL,
	`Disc3` DOUBLE NULL DEFAULT NULL,
	`Qunit` DOUBLE NULL DEFAULT NULL
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;
"""
        print(create_query)
        create_result =  cursor.execute(create_query)
        conn.commit()

        checkQuery=f"""SELECT table_name FROM information_schema.tables WHERE table_schema = '{dbName}' AND table_name like UPPER('DC_{username}_{inventory}%')"""
        check_result= cursor.execute(checkQuery)
        rows = cursor.fetchall()
        print(rows)
        if rows:
            return {"status":True,"message": f"No tables found starting with '_'","result":rows[0]}
    except Exception as e:
        return {"message": f"Error checking tables: {str(e)}"}
    # Query the database for the user with the specified username
    finally:
        conn.close()




@app.post("/createItem/")
async def create_Item(itemNumber,itemName,inventory,dbName,branch,handQuantity):
    conn = mysql.connector.connect(
   user='root', password='root', host='localhost', database=f'{dbName}',port=3307)
    cursor = conn.cursor()


    insert_query = (f"INSERT INTO {inventory} (itemName, itemNumber, GOID, Branch, quantity, S1, S2, S3, handQuantity, vat, sp, costPrice, image, Disc1, Disc2, Disc3, Qunit)" 
"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    itemNumber_value=itemNumber.upper()
    goid_value=itemNumber.upper()
    itemName_value=itemName.upper()
    branch_value=branch.upper()
    handQuantity_value=handQuantity
    Qunit=1
    data = (
    itemName_value,
    itemNumber_value,
    goid_value,
    branch_value,
    0,
    0,
    0,
    0,
    handQuantity_value,
    0,
    "",
    0,
    "",
    0,
    0,
    0,
    Qunit
    )
    print(insert_query)
    try:
        print('llll')
        print(insert_query)
        cursor.execute(insert_query, data)
        conn.commit()
        return {"status": True,"message":"Item inserted successfully"}
        

    except Exception as e:
        conn.rollback()
        return {"status":False,"message": f"Error checking tables: {str(e)}","item":"empty"}