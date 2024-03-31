from django.shortcuts import render
from  database_connection import get_sql_anywhere_connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
import hashlib
from django.core.files.storage import default_storage
import base64
from io import BytesIO
from PIL import Image
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.conf import settings
import base64

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

@api_view(['PUT'])
@permission_classes([AllowAny])
def fetch_cat(request):
    print("catsss")
    connection, cursor = get_sql_anywhere_connection()
    try:
      query = "SELECT * FROM \"dba\".\"Categories\" WHERE \"Org_ID\" = ?"
      org_Id = request.data['org_id']
      cursor.execute(query, org_Id)  
      rows = cursor.fetchall()
      rows_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
      print("lllll")
      print(rows_list)
      return JsonResponse({"message": "Fetched successfully!", "data": rows_list})


    except Exception as e:
        print(f"Error fetching data cats: {e}")
        return JsonResponse({"error": "Failed successfully!", "message": str(e)})

    finally:
        cursor.close()
        connection.close()



@api_view(['PUT'])
@permission_classes([AllowAny])
def fetch_p_cat(request):
    print("catsss")
    connection, cursor = get_sql_anywhere_connection()
    try:
      query = "SELECT * FROM \"dba\".\"Categories\" WHERE \"Org_ID\" = ? AND \"Parent_id\" = ?"
      org_Id = request.data['org_id']
      cursor.execute(query, [org_Id , 0])  
      rows = cursor.fetchall()
      rows_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

      return JsonResponse({"message": "Fetched successfully!", "data": rows_list})


    except Exception as e:
        print(f"Error fetching data cats: {e}")
        return JsonResponse({"error": "Failed successfully!", "message": str(e)})

    finally:
        cursor.close()
        connection.close()        




@api_view(['PUT'])
@permission_classes([AllowAny])
def fetch_sub_cat(request):
    print("catsss")
    connection, cursor = get_sql_anywhere_connection()
    try:
      query = "SELECT * FROM \"dba\".\"Categories\" WHERE \"Org_ID\" = ? AND \"Parent_id\" != ?"
      org_Id = request.data['org_id']
      cursor.execute(query, [org_Id , 0])  
      rows = cursor.fetchall()
      rows_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

      return JsonResponse({"message": "Fetched successfully!", "data": rows_list})


    except Exception as e:
        print(f"Error fetching data cats: {e}")
        return JsonResponse({"error": "Failed successfully!", "message": str(e)})

    finally:
        cursor.close()
        connection.close()   

@api_view(['PUT'])
@permission_classes([AllowAny])
def fetch_disc_types(request):

    print("discss")
    connection, cursor = get_sql_anywhere_connection()
    try:
      query = "SELECT * FROM \"dba\".\"Discount_Type\" WHERE \"Org_ID\" = ?"
      org_Id = request.data['org_id']
      cursor.execute(query, org_Id)  
      rows = cursor.fetchall()
      rows_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

      return JsonResponse({"message": "Fetched successfully!", "data": rows_list})


    except Exception as e:
        print(f"Error fetching data cats: {e}")
        return JsonResponse({"error": "Failed successfully!", "message": str(e)})

    finally:
        cursor.close()
        connection.close()




@api_view(['PUT'])
@permission_classes([AllowAny])
def fetch_settings(request):
    print("fetch_settings")
    connection, cursor = get_sql_anywhere_connection()
    try:
      query = "SELECT * FROM \"dba\".\"Organizations\" WHERE \"Org_ID\" = ?"
      org_Id = request.data['org_id']
      cursor.execute(query, org_Id)  
      rows = cursor.fetchall()

      rows_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
      print(rows_list)

      query = "SELECT * FROM \"dba\".\"Screen_image\" WHERE \"Org_ID\" = ?"
      org_Id = request.data['org_id']
      cursor.execute(query, org_Id)  
      rows = cursor.fetchall()

      rows_list2 = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
      print(rows_list2)

      return JsonResponse({"message": "Fetched successfully!", "data": rows_list, "images": rows_list2})


    except Exception as e:
        print(f"Error fetching data cats: {e}")
        return JsonResponse({"error": "Failed successfully!", "message": str(e)})

    finally:
        cursor.close()
        connection.close()


@api_view(['PUT'])
@permission_classes([AllowAny])
def fetch_uom(request):
    print("uommm")
    connection, cursor = get_sql_anywhere_connection()
    try:
      org_id = request.data['org_id']   
      query = "SELECT * FROM \"dba\".\"UOM\" WHERE Org_ID = ?"
      cursor.execute(query,[org_id])  
      rows = cursor.fetchall()
      rows_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

      return JsonResponse({"message": "Fetched successfully!", "data": rows_list})


    except Exception as e:
        print(f"Error fetching data UOM: {e}")
        return JsonResponse({"error": "Failed successfully!", "message": str(e)})

    finally:
        cursor.close()
        connection.close()



@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_cat(request):

    if not request.data['catID'] or not request.data['org_Id'] :
      return JsonResponse({"error": "Failed successfully, Please fill all the required fields!"})
      
    connection, cursor = get_sql_anywhere_connection()
    try:
        catID = request.data['catID']
        org_Id = request.data['org_Id']
        query_fetch = f"SELECT * FROM \"dba\".\"Categories\" WHERE \"id\" = ? "
        cursor.execute(query_fetch, [catID ])
        existing_data = cursor.fetchone()
        print("data in here")
        print(request.data)
        if existing_data:
         if 'Img' in request.FILES:
          avatar = request.FILES['Img']
          print(request.data['Stat'])   
          print("imgimgi") 
          print(request.data['Stat'])   
          if request.data['Stat'] == "true" or  request.data['Stat'] == "1":
                print("stat is true")


        # if avatar == "http://127.0.0.1:8000"+ str(user.Img.url):
        #   image_path=user.Img.url
        # else:  
          org_id = request.data['org_Id']

          image_path = default_storage.save('images/ORG'+ org_id +'/'+avatar.name, ContentFile(avatar.read()))
        #  path = settings.MEDIA_ROOT + image_path
        #  image_path = default_storage.save('images/' + avatar.name, ContentFile(avatar.read()))
        #  path = settings.MEDIA_ROOT+image_path
          data = {
                # 'id': request.data['catID'],
                'Parent_id': request.data['Parent_id'],
                # 'Created_By': request.data['created_by'],
                'View_Order': request.data['view'],
                # 'RegKey': request.data['storeRegKey'],
                'LChange_By': request.data['LChange_By'],
                'LChange_On': request.data['LChange_On'],
                'Status': 1 if request.data['Stat'] == "true" or  request.data['Stat'] == "1" else 0,
                'Name': request.data['name'],
                'Name_AR': request.data['nameAR'],
                'Description': request.data['Desc'],
                'Photo' :  image_path,


          }

         else :
          print(request.data['Stat'])   
          print("jkjkjk") 
          if request.data['Stat'] == "true" or  request.data['Stat'] == "1":
                print("stat is true")

          data = {
                # 'id': request.data['catID'],
                'Parent_id': request.data['Parent_id'],
                # 'Created_By': request.data['created_by'],
                'View_Order': request.data['view'],
                # 'RegKey': request.data['storeRegKey'],
                'LChange_By': request.data['LChange_By'],
                'LChange_On': request.data['LChange_On'],
                'Status': 1 if request.data['Stat'] == "true" or  request.data['Stat'] == "1" else 0,
                'Name': request.data['name'],
                'Name_AR': request.data['nameAR'],

                'Description': request.data['Desc'],
            }
         print("existing_data")  

         print(existing_data)  
         print("22222wdata")
         print(data)  

         update_columns = ', '.join([f'"{col}" = ?' for col in data.keys()])
         query_update = f"UPDATE \"dba\".\"Categories\" SET {update_columns} WHERE \"id\" = ?"

         cursor.execute(query_update, list(data.values()) + [catID])
         connection.commit()

         return JsonResponse({"message": "Category updated successfully!"}, status=200)
        else:
            return JsonResponse({"error": f"Category with ID {catID} not found."}, status=404)

    except Exception as e:
        return JsonResponse({"error": f"Failed to update store: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()


@api_view(['PUT'])
@permission_classes([AllowAny])
def add_cat(request):

    connection, cursor = get_sql_anywhere_connection()
    print(request.data)
    try:
        if not request.data['org_Id'] :
            print("not f3ln")
            return JsonResponse({"error": "Failed successfully, Please fill all the required fields!"})
        print("not not ")
        if 'Img' in request.FILES:
         avatar = request.FILES['Img']
        # if avatar == "http://127.0.0.1:8000"+ str(user.Img.url):
        #   image_path=user.Img.url
        # else:  
         org_id = request.data['org_Id']

         image_path = default_storage.save('images/ORG'+ org_id +'/'+avatar.name, ContentFile(avatar.read()))
        #  path = settings.MEDIA_ROOT + image_path
        #  image_path = default_storage.save('images/' + avatar.name, ContentFile(avatar.read()))
        #  path = settings.MEDIA_ROOT+image_path

        else :
            image_path = ""
        print( "pathhhh", image_path)    
        data = {
                'Parent_id':  0 if request.data['catID'] == [] else request.data['catID'] ,
                'Created_By': request.data['created_by'],
                'Created_on': request.data['created_on'],
                'Org_ID': request.data['org_Id'],
                'View_Order': request.data['view'],
                'LChange_By': request.data['LChange_By'],
                'LChange_On': request.data['LChange_On'],
                'Status': 1 if request.data['Stat'] == "true" else 0,
                'Photo' :  image_path,
                'Name': request.data['name'],
                'Name_AR': request.data['nameAR'],
                'Description': request.data['Desc'],
        }
        print("plzz workkkk", data)

        query = f"""
            INSERT INTO "dba"."Categories" ({', '.join(data.keys())})
            VALUES ({', '.join(['?' for _ in data.values()])})
        """
        cursor.execute(query, list(data.values()))
        connection.commit()

        print("Data inserted successfully.")
        return JsonResponse({"message": "Added successfully!"}, status=200)

    except Exception as e:
        print("failed")
        error_message = str(e)
        print(f"Error inserting data: {error_message}")
        return JsonResponse({"error": f"Failed to insert data: {error_message}"}, status=500)

    finally:
        cursor.close()
        connection.close()


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_cat(request):
    try:
        connection, cursor = get_sql_anywhere_connection()
        cid = request.data['id']
        org = request.data['org_id']

        print(cid)
        query = "SELECT * FROM \"dba\".\"Categories\" WHERE Parent_id = ? AND Org_ID = ?"
        cursor.execute(query, (cid , org))
        result = cursor.fetchall()
        print(result)
        if result:
            # print( result[1][1])
            for i in result:
                    print("herererer")
                    print(i[1])
                    query = "DELETE FROM \"dba\".\"Categories\" WHERE Parent_id = ? AND id = ?"
                    cursor.execute(query, (cid , i[0]))
                    print("deleted", i)
        cursor.execute(f"DELETE FROM \"dba\".\"Categories\" WHERE \"id\" = ?", [cid])
        connection.commit()  

        return JsonResponse({"message": "Category deleted successfully."})
    except pyodbc.Error as e:
        return JsonResponse({"error": f"Failed to delete Category: {str(e)}"}, status=500)
    finally:
        cursor.close()
        connection.close()
from PIL import Image

@api_view(['PUT'])
@permission_classes([AllowAny])
def add_product_Img(request):
    try:
        connection, cursor = get_sql_anywhere_connection()
        pid = request.data['code']
        if 'Img' in request.FILES:
            avatar = request.FILES['Img']
            org_id = request.data['org_id']

            image_path = default_storage.save('images/ORG'+ org_id +'/'+avatar.name, ContentFile(avatar.read()))
            # path = settings.MEDIA_ROOT + image_path

            # with open(path, 'rb') as image_file:
            #     data = base64.b64encode(image_file.read())
            # print(data.decode('utf-8'))
            data_dict = {
                "Photo": image_path,
                # "Photo_base64": image_path
            }

            update_columns = ', '.join([f'"{col}" = ?' for col in data_dict.keys()])
            query_update = f"UPDATE \"dba\".\"Product\" SET {update_columns} WHERE \"ProductID\" = ? AND \"Org_ID\" = ?"
            cursor.execute(query_update, list(data_dict.values()) + [pid, org_id])
            connection.commit()

            print(settings.MEDIA_ROOT + image_path)
        print("Photo inserted successfully.")
        return JsonResponse({"message": "Photo Added successfully!"}, status=200)

    except Exception as e:
        print(str(e))
        return JsonResponse({"error": f"Failed to add Product Image: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()



@api_view(['PUT'])
@permission_classes([AllowAny])
def add_product(request):

    connection, cursor = get_sql_anywhere_connection()
    print(request.data)
    org_id = request.data['org_id']

    try:
        if not request.data['code'] :
            print("not f3ln")
            return JsonResponse({"error": "Failed successfully, Please fill all the required fields!"}, status=400)
        print("not not ")
        # if 'Img' in request.FILES:
        #  avatar = request.FILES['Img']
        # # if avatar == "http://127.0.0.1:8000"+ str(user.Img.url):
        # #   image_path=user.Img.url
        # # else:  
        #  image_path = default_storage.save('images/' + avatar.name, ContentFile(avatar.read()))
        # t =  request.data['taxes'] + 0.00
        mat_id = request.data['code']
        cursor.execute(
                "SELECT COUNT(*) FROM \"dba\".\"Product\" WHERE \"ProductID\" = ? AND \"Org_ID\" = ?",
                [mat_id, org_id]
            )
        count = cursor.fetchone()[0]

        if count > 0:
                print("cannot add mat")
                return JsonResponse({"message": "Product's code already in use.", "use": "true"}, status=200)

        data = {
                'ProductID': request.data['code'],
                'Created_By': request.data['created_by'],
                'Created_on': request.data['created_on'],
                'Org_ID': org_id,
                'Base_UOM': request.data['Base_UOM'],
                'Lchange_By': request.data['LChange_By'],
                'Lchange_On': request.data['LChange_On'],
                'Status': request.data['Stat'],               
                'Name': request.data['name'],
                'Name_AR': request.data['nameAR'],

                'DescriptionEN': request.data['DescEN'],
                'DescriptionAR': request.data['DescAR'],
                'Category_Id': request.data['Category_Id'],
                # 'Current_Stock' : request.data['Current_Stock'],
                'Prod_Date' : request.data['Prod_Date'],
                'Expiry_Date' : request.data['Expiry_Date'],
                'Type' : request.data['type'],
                'Note' : request.data['note'],
                'Unit_Price' : request.data['unit'],
                'Taxes' :  request.data['taxes'] ,


        }
        print("plzz workkkk", data)

        query = f"""
            INSERT INTO "dba"."Product" ({', '.join(data.keys())})
            VALUES ({', '.join(['?' for _ in data.values()])})
        """
        cursor.execute(query, list(data.values()))
        connection.commit()
        result = request.data['code']
        print(request.data['code'])
        cID = request.data['code']
        alts = request.data['alts']
        stores = request.data['stores']

        print(cID)

        for i in alts:
            print(i)
            print("heresss altsss")
            if not i['altUnit'] :
            # or i['base'] or i['qty']:
                continue
            cursor.execute(f"INSERT INTO \"dba\".\"Product_Uom\" (Product_Id , UOM, Conv_Factor, UOMBaseQty,Price ,Org_ID) VALUES (?, ?, ?, ?,?, ?)", 
            [cID, i['altUnit'] ,i['base'], i['qty'],i['price'] ,org_id])
            connection.commit()  

        for i in stores:
            print(i)
            org_id = request.data['org_id']
            print("ksh") 
            print(org_id) 

            if not i['Store_ID'] :
            # or i['base'] or i['qty']:
                continue
            cursor.execute(f"INSERT INTO \"dba\".\"Product_Store_Stock\" (Product_id , Store_Id, Stock, Org_ID) VALUES (?, ?, ?, ?)", 
            [cID, i['Store_ID'] ,i['Stock'], org_id])
            connection.commit()  



        print("Data inserted successfully.")
        return JsonResponse({"message": "Added successfully!"}, status=200)
    
    except Exception as e:
        print("failed")
        error_message = str(e)
        print(f"Error inserting data: {error_message}")
        return JsonResponse({"error": f"Failed to insert data: {error_message}"}, status=500)

    finally:
        cursor.close()
        connection.close()

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_mat(request):
    try:
        connection, cursor = get_sql_anywhere_connection()
        mat_id = request.data['mat']
        org_id = request.data['org_id']

        print(mat_id)
        cursor.execute(
                "SELECT COUNT(*) FROM \"dba\".\"Order_Item\" WHERE \"ProductID\" = ? AND \"Org_ID\" = ?",
                [mat_id, org_id]
            )
        count = cursor.fetchone()[0]

        if count > 0:
                print("cannot delete mat")
                return JsonResponse({"message": "Product in use.", "use": "true"}, status=200)

        else :
            cursor.execute(f"DELETE FROM \"dba\".\"Product\" WHERE \"ProductID\" = ? AND Org_ID = ?", [mat_id , org_id ])        
            connection.commit() 
            cursor.execute(f"DELETE FROM \"dba\".\"Product_Store_Stock\" WHERE \"Product_Id\" = ? AND Org_ID = ?", [mat_id , org_id ])        
            connection.commit()  
            cursor.execute(f"DELETE FROM \"dba\".\"Product_Uom\" WHERE \"Product_Id\" = ? AND Org_ID = ?", [mat_id , org_id ])        
            connection.commit()  
    

            return JsonResponse({"message": "Product deleted successfully."})
    except Exception as e:
        return JsonResponse({"error": f"Failed to delete Product: {str(e)}"}, status=500)
    finally:
        cursor.close()
        connection.close()



@api_view(['PUT'])
@permission_classes([AllowAny])
def fetch_products(request):
    print("fetch_products")
    connection, cursor = get_sql_anywhere_connection()
    try:
        query = """
                    SELECT P.*, C.Name AS Cat_name, U.UOM_AName AS Base_UOM_AName
            FROM "dba"."Product" AS P
            INNER JOIN "dba"."Categories" AS C ON P.Category_Id = C.id
            LEFT JOIN "dba"."UOM" AS U ON P.Base_UOM = U.UOMStandardCode
            WHERE P.Org_ID = ? AND U.Org_ID = ?
            ORDER BY P.Status, P.ProductID ASC

        """
        org_id = request.data['org_id']
        cursor.execute(query, [org_id , org_id])
        rows = cursor.fetchall()
        rows_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
        print(rows_list[0])
        return JsonResponse({"message": "Fetched successfully!", "data": rows_list})

    except Exception as e:
        print(f"Error fetching data prods: {e}")
        return JsonResponse({"error": "Failed successfully!", "message": str(e)})

    finally:
        cursor.close()
        connection.close()



@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def fetch_a_product(request):
    try:
        connection, cursor = get_sql_anywhere_connection()
        print("ciddd")
        cid = request.data['id']
        org_id = request.data['org_id']

        print(cid)
        query = "SELECT * FROM \"dba\".\"Product\" WHERE ProductID = ? AND Org_ID = ?"
        cursor.execute(query, (cid , org_id))
        # result = cursor.fetchall()
        # cursor.execute(query)  
        rows = cursor.fetchall()
        print(rows)
        data_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]


        query = "SELECT * FROM \"dba\".\"Product_Uom\" WHERE Product_Id = ? AND Org_ID = ?"
        cursor.execute(query, (cid , org_id))
        # result = cursor.fetchall()
        # cursor.execute(query)  
        rows_alt = cursor.fetchall()    
        # print(rows)

        alt_data_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows_alt]
        print("thezzze r altsss")

        print(alt_data_list)


        query = "SELECT * FROM \"dba\".\"Product_Store_Stock\" WHERE Product_Id = ? AND Org_ID = ?"
        cursor.execute(query, (cid , org_id))
        # result = cursor.fetchall()
        # cursor.execute(query)  
        rows_stores = cursor.fetchall()
        # print(rows)

        stores_data_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows_stores]
        print("thezzze r storess")

        print(stores_data_list)

        return JsonResponse({"message": "Fetched successfully.", "data" : data_list, "alts": alt_data_list, "stores": stores_data_list})
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": f"Failed to fetch Product: {str(e)}"}, status=500)
    finally:
        cursor.close()
        connection.close()

@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def fetch_a_product_uom(request):
    try:
        connection, cursor = get_sql_anywhere_connection()
        print("ciddd uommm")
        print(request.data)
        cid = request.data['id']
        org_id = request.data['org_id']

        print(request.data)
        query = """
            SELECT U.UOM, UU.UOM_AName
            FROM "dba"."Product_Uom" AS U
            LEFT JOIN "dba"."UOM" AS UU ON U.UOM = UU.UOMStandardCode
            WHERE U.Product_Id = ? AND U.Org_ID = ? AND UU.Org_ID = ?
            
            UNION
            
            SELECT P.Base_UOM AS UOM, PU.UOM_AName
            FROM "dba"."Product" AS P
            LEFT JOIN "dba"."UOM" AS PU ON P.Base_UOM = PU.UOMStandardCode
            WHERE P.ProductID = ? AND P.Org_ID = ? AND PU.Org_ID = ? 
        """
        cursor.execute(query, (cid, org_id, org_id ,cid, org_id , org_id))
        rows = cursor.fetchall()
        data_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

        print("these are the results:")
        print(data_list)

        return JsonResponse({"message": "Fetched successfully.", "data": data_list})
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": f"Failed to fetch Product: {str(e)}"}, status=500)
    finally:
        cursor.close()
        connection.close()



@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_mat(request):

    # if not request.data['catID'] or not request.data['org_Id'] :
    #   ret urn JsonResponse({"error": "Failed successfully, Please fill all the required fields!"})
    print("rrrrequest.data")  
    print(request.data)  
    connection, cursor = get_sql_anywhere_connection()
    # mat_id = request.data['code']
    # cursor.execute(
    #             "SELECT COUNT(*) FROM \"dba\".\"Product\" WHERE \"ProductID\" = ? AND \"Org_ID\" = ?",
    #             [mat_id, org_id]
    #         )
    # count = cursor.fetchone()[0]

    # if count > 0:
    #           print("cannot add mat")
    #           return JsonResponse({"message": "Product's code already in use.", "use": "true"}, status=200)

    try:
        code = request.data['code']
        # org_Id = request.data['org_Id']
        # query_fetch = f"SELECT * FROM \"dba\".\"Product\" WHERE \"Code\" = ? "
        # cursor.execute(query_fetch, [catID ])
        # existing_data = cursor.fetchone()
        # print(request.data)
        # if existing_data:
        data = {
                'ProductID': request.data['code'],
                # 'Created_By': request.data['created_by'],
                # 'Created_on': request.data['created_on'],
                # 'Org_ID': request.data['org_Id'],
                'Base_UOM': request.data['Base_UOM'],
                'Lchange_By': request.data['LChange_By'],
                'Lchange_On': request.data['LChange_On'],
                'Status': request.data['Stat'],               
                'Name': request.data['name'],
                'Name_AR': request.data['nameAR'],

                'DescriptionEN': request.data['DescEN'],
                'DescriptionAR': request.data['DescAR'],
                'Category_Id': request.data['Category_Id'],
                # 'Current_Stock' : request.data['Current_Stock'],
                'Prod_Date' : request.data['Prod_Date'],
                'Expiry_Date' : request.data['Expiry_Date'],
                'Type' : request.data['type'],
                'Note' : request.data['note'],
                'Unit_Price' : request.data['unit'],
                'Taxes' : request.data['taxes'],
            }
        print("existing_data")
        org_id = request.data['org_id']  
        print(request.data['alts'])
        # print(existing_data)  
        update_columns = ', '.join([f'"{col}" = ?' for col in data.keys()])
        query_update = f"UPDATE \"dba\".\"Product\" SET {update_columns} WHERE \"ProductID\" = ? AND Org_ID = ?" 
        cursor.execute(query_update, list(data.values()) + [code , org_id])
        connection.commit()
        if 'Img' in request.FILES:
             avatar = request.FILES['Img']
             print("there iss imaggge")
        # if avatar == "http://127.0.0.1:8000"+ str(user.Img.url):
        #   image_path=user.Img.url
        # else:  
             image_path = default_storage.save('images/' + avatar.name, ContentFile(avatar.read()))
             path = settings.MEDIA_ROOT+image_path
             print(path)
             data = {
                    'Photo': path,
                    # 'RegKey': request.data['storeRegKey'],
                }
             update_columns = ', '.join([f'"{col}" = ?' for col in data.keys()])
             query_update = f"UPDATE \"dba\".\"Product\" SET {update_columns} WHERE \"ProductID\" = ? AND Org_ID =?"
             cursor.execute(query_update, list(data.values()) + [code , org_id])
             connection.commit()


        alts = request.data['alts']
        stores = request.data['stores']

        print(code)
        print(alts)

        query = "SELECT * FROM \"dba\".\"Product_Uom\" WHERE Product_Id = ? AND Org_ID = ?"
        cursor.execute(query, (code, org_id))
        result = cursor.fetchall()
        print("el result")

        print(result)
        if result:
                print("therez result el7")
                c=0
                # print( result[1][1])
                for i in result:
                    print("herererer")
                    print(i[1])
                    query = "DELETE FROM \"dba\".\"Product_Uom\" WHERE Product_Id = ? AND UOM = ? AND Org_ID = ?"
                    cursor.execute(query, (code , i[1], org_id))
                    connection.commit()
                    print("thattzz i[1]", i[1])

                    print("deleted", i)
                    # c=c+1
                    # continue
                # else :
                #    cursor.execute(f"INSERT INTO \"dba\".\"permissions_admins\" (PID , UID) VALUES (? , ?)", [i , request.data['UID']])
                #    connection.commit()  
        if alts:
         c = 0
         for i in alts:
            if c == 0 and i == None:
                break  
            print(i)
            c = c+1
            print("this is alt")
            if not i['UOM'] :
            # or i['base'] or i['qty']:
                continue

            if not 'Price' in i:
                print("are u here")
                price = 0
            else :
               price = i['Price']    
               print("or are u here")


            if not 'Conv_Factor' in i:
                print("are u here")
                conv = 0
            else :
               conv = i['Conv_Factor']    
               print("or are u here")

            if not 'UOMBaseQty' in i:
                print("are u here")
                base = 0
            else :
               base = i['UOMBaseQty']    
               print("or are u here")               
               

            cursor.execute(f"INSERT INTO \"dba\".\"Product_Uom\" (Product_Id , UOM, Conv_Factor, UOMBaseQty, Price, Org_ID) VALUES (?, ?, ?,?, ?, ?)", 
            [code, i['UOM'], conv, base , price, org_id])
            connection.commit() 
            c = c+1

        query = "SELECT * FROM \"dba\".\"Product_Store_Stock\" WHERE Product_id = ? AND Org_ID = ?"
        cursor.execute(query, (code ,  org_id))
        result = cursor.fetchall()
        print("el result")

        print(result)
        if result:
                print("therez result el7")
                c=0
                # print( result[1][1])
                for i in result:
                    print("herererer")
                    print(i[1])
                    query = "DELETE FROM \"dba\".\"Product_Store_Stock\" WHERE Product_id = ? AND Store_Id = ? AND Org_ID = ?"
                    cursor.execute(query, (code , i[2], org_id))
                    connection.commit()
                    print("thattzz i[2]", i[2])

                    print("deleted", i)
                    # c=c+1
                    # continue
                # else :
                #    cursor.execute(f"INSERT INTO \"dba\".\"permissions_admins\" (PID , UID) VALUES (? , ?)", [i , request.data['UID']])
                #    connection.commit()  

        if stores: 
         c = 0   
         for i in stores:
            if c == 0 and i == None:
             break
            print(i)
            c = c + 1 
            print("this is a store")
            if not i['Store_Id'] :
            # or i['base'] or i['qty']:
                continue
            cursor.execute(f"INSERT INTO \"dba\".\"Product_Store_Stock\" (Product_Id , Store_Id,  Stock, Org_ID) VALUES (?, ?, ?, ?)", 
            [code, i['Store_Id'] ,i['Stock'], org_id])
            connection.commit()  



        return JsonResponse({"message": "Category updated successfully!"}, status=200)
        # else:
        #     return JsonResponse({"error": f"Category with ID {catID} not found."}, status=404)

    except Exception as e:
        return JsonResponse({"error": f"Failed to update store: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()



@api_view(['PUT'])
@permission_classes([AllowAny])
def add_UOM(request):

    connection, cursor = get_sql_anywhere_connection()
   
    try:
        if not request.data['code'] :
            return JsonResponse({"error": "Failed , Please fill all the required fields!"})
        org_id = request.data['org_id']
        print(request.data)
        mat_id = request.data['code']
        cursor.execute(
                "SELECT COUNT(*) FROM \"dba\".\"UOM\" WHERE \"UOMStandardCode\" = ? AND \"Org_ID\" = ?",
                [mat_id, org_id]
            )
        count = cursor.fetchone()[0]

        if count > 0:
                print("cannot add UOM")
                return JsonResponse({"message": "UOM's code already in use.", "use": "true"}, status=200)

        data = {
            'UOMStandardCode': request.data['code'],
            'UOM_EName': request.data['nameEN'],
            'UOM_AName': request.data['nameAR'],
            'Org_ID' : org_id
        }

        query = f"""
            INSERT INTO "dba"."UOM" ({', '.join(data.keys())})
            VALUES ({', '.join(['?' for _ in data.values()])})
        """
        cursor.execute(query, list(data.values()))
        connection.commit()
        print("Data inserted successfully.")
        print(query , list(data.values()))
        return JsonResponse({"message": "Added successfully!"}, status=200)

    except Exception as e:
        print("failed")
        error_message = str(e)
        print(f"Error inserting data: {error_message}")
        return JsonResponse({"error": f"Failed to insert data: {error_message}"}, status=500)

    finally:
        cursor.close()
        connection.close()

@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_UOM(request):

    connection, cursor = get_sql_anywhere_connection()
   
    try:
        if not request.data['code'] :
            return JsonResponse({"error": "Failed , Please fill all the required fields!"})
        org_id = request.data['org_id']
        print(request.data)
        data = {
            'UOMStandardCode': request.data['code'],
            'UOM_EName': request.data['nameEN'],
            'UOM_AName': request.data['nameAR'],
            'Org_ID' : org_id
        }

        uom_id = request.data['uom_id']
        update_columns = ', '.join([f'"{col}" = ?' for col in data.keys()])
        query_update = f"UPDATE \"dba\".\"UOM\" SET {update_columns} WHERE \"org_Id\" = ? AND \"UOMStandardCode\" = ?"
        cursor.execute(query_update, list(data.values()) + [org_id , uom_id])
        connection.commit()
        # query = f"""
        #     INSERT INTO "dba"."UOM" ({', '.join(data.keys())})
        #     VALUES ({', '.join(['?' for _ in data.values()])})
        # """
        # cursor.execute(query, list(data.values()))
        print("Data inserted successfully.")
        return JsonResponse({"message": "Added successfully!"}, status=200)

    except Exception as e:
        print("failed")
        error_message = str(e)
        print(f"Error inserting data: {error_message}")
        return JsonResponse({"error": f"Failed to insert data: {error_message}"}, status=500)

    finally:
        cursor.close()
        connection.close()



@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_uom(request):
    try:
        connection, cursor = get_sql_anywhere_connection()
        uom_code = request.data['code']
        org_id = request.data['org_id']

        cursor.execute(f"DELETE FROM \"dba\".\"UOM\" WHERE \"UOMStandardCode\" = ? AND Org_ID = ?", [uom_code , org_id ])        
        connection.commit()  

        return JsonResponse({"message": "Product deleted successfully."})
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": f"Failed to delete Product: {str(e)}"}, status=500)
    finally:
        cursor.close()
        connection.close()





@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_settings(request):

    if not request.data['org_id'] :
      return JsonResponse({"error": "Failed, Please fill all the required fields!"})
    print("passedd")  
    connection, cursor = get_sql_anywhere_connection()
    try:
        # catID = request.data['catID']
        org_Id = request.data['org_id']
        print(org_Id)
        query_fetch = f"SELECT * FROM \"dba\".\"Organizations\" WHERE \"Org_ID\" = ? "
        cursor.execute(query_fetch, [org_Id])
        existing_data = cursor.fetchone()
        print(request.data)
        if existing_data:
            data = {
                # 'id': request.data['catID'],
                'Delivery_Amount': request.data['Delivery_Amount'],
                # 'Created_By': request.data['created_by'],
                'Service_Amount': request.data['Service_Amount'],
                # 'RegKey': request.data['storeRegKey'],
            }
            print("existing_data")  

            print(existing_data)  
            update_columns = ', '.join([f'"{col}" = ?' for col in data.keys()])
            query_update = f"UPDATE \"dba\".\"Organizations\" SET {update_columns} WHERE \"org_Id\" = ?"

            cursor.execute(query_update, list(data.values()) + [org_Id])
            connection.commit()
            h = "Settings"
            query_fetch = f"SELECT * FROM \"dba\".\"Screen_image\" WHERE \"Org_ID\" = ? AND \"name\" = ?"
            cursor.execute(query_fetch, [org_Id , h])
            existing_data = cursor.fetchone()
            print(request.data)

            if existing_data and 'Img1' in request.FILES:
             avatar = request.FILES['Img1']
             org_id = request.data['org_id']

             image_path = default_storage.save('images/ORG'+ org_id +'/'+avatar.name, ContentFile(avatar.read()))
            #  path = settings.MEDIA_ROOT + image_path

        # if avatar == "http://127.0.0.1:8000"+ str(user.Img.url):
        #   image_path=user.Img.url
        # else:  
            #  image_path = default_storage.save('images/' + avatar.name, ContentFile(avatar.read()))
            #  path = settings.MEDIA_ROOT+image_path

             data = {
                    'image_path': image_path,
                    # 'RegKey': request.data['storeRegKey'],
                }
             update_columns = ', '.join([f'"{col}" = ?' for col in data.keys()])
             query_update = f"UPDATE \"dba\".\"Screen_image\" SET {update_columns} WHERE \"name\" = ? AND Org_ID =?"
             cursor.execute(query_update, list(data.values()) + [h , org_Id])
             connection.commit()


            if existing_data and 'Img2' in request.FILES:
             avatar = request.FILES['Img2']
        # if avatar == "http://127.0.0.1:8000"+ str(user.Img.url):
        #   image_path=user.Img.url
        # else:  
             org_id = request.data['org_id']

             image_path = default_storage.save('images/ORG'+ org_id +'/'+avatar.name, ContentFile(avatar.read()))

             data = {
                    'image_path': image_path,
                    # 'RegKey': request.data['storeRegKey'],
                }
             h = "Orders"   
             update_columns = ', '.join([f'"{col}" = ?' for col in data.keys()])
             query_update = f"UPDATE \"dba\".\"Screen_image\" SET {update_columns} WHERE \"name\" = ? AND Org_ID =?"
             cursor.execute(query_update, list(data.values()) + [h , org_Id])
             connection.commit()


            if existing_data and 'Img3' in request.FILES:
             avatar = request.FILES['Img3']
        # if avatar == "http://127.0.0.1:8000"+ str(user.Img.url):
        #   image_path=user.Img.url
        # else:  
             org_id = request.data['org_id']

             image_path = default_storage.save('images/ORG'+ org_id +'/'+avatar.name, ContentFile(avatar.read()))

             data = {
                    'image_path': image_path,
                    # 'RegKey': request.data['storeRegKey'],
                }
             h="Home"   
             update_columns = ', '.join([f'"{col}" = ?' for col in data.keys()])
             query_update = f"UPDATE \"dba\".\"Screen_image\" SET {update_columns} WHERE \"name\" = ? AND Org_ID =?"
             cursor.execute(query_update, list(data.values()) + [h , org_Id])
             connection.commit()




            return JsonResponse({"message": "Organization updated successfully!"}, status=200)
        else:
            return JsonResponse({"error": f"Organization with ID {org_Id} not found."}, status=404)

    except Exception as e:
        print(str(e))
        return JsonResponse({"error": f"Failed to update Organization: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()



@api_view(['PUT'])
@permission_classes([AllowAny])
def fetch_discounts(request):
    print("catsss")
    connection, cursor = get_sql_anywhere_connection()
    try:
      query = """
                SELECT
        D.Discount_Code,
        MAX(D.Valid_To) AS Valid_To,
        MAX(D.Valid_From) AS Valid_From,
        MAX(D.UOM) AS UOM,
        MAX(D.Status) AS Status,
        MAX(D.ProductID) AS ProductID,
        MAX(D.Org_ID) AS Org_ID,
        MAX(D.is_product) AS is_product,
        MAX(D.is_customer) AS is_customer,
        MAX(D.Discount_Name) AS Discount_Name,
        MAX(D.Discount_MaxUses_User) AS Discount_MaxUses_User,
        MAX(D.Discount_MaxUses) AS Discount_MaxUses,
        MAX(D.Discount_ID) AS Discount_ID,
        MAX(D.Discount_Description) AS Discount_Description,
        MAX(D.Discount_Amount) AS Discount_Amount,
        MAX(D.Dis_type_code) AS Dis_type_code,
        MAX(D.Customer_ID) AS Customer_ID,
        MAX(D.Created_on) AS Created_on,
        MAX(D.Created_BY) AS Created_BY,
        MAX(D.Created_at) AS Created_at,
        MAX(U.UOM_AName) AS UOM_AName
        FROM
        "dba"."Discount" AS D
        LEFT JOIN
        "dba"."UOM" AS U ON D.UOM = U.UOMStandardCode
        WHERE
        D."Org_ID" = ? AND U.Org_ID = ?
        GROUP BY
        D.Discount_Code;



        """

      org_Id = request.data['org_id']
      cursor.execute(query, [org_Id , org_Id])  
      rows = cursor.fetchall()
      rows_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

      return JsonResponse({"message": "Fetched successfully!", "data": rows_list})


    except Exception as e:
        print(f"Error fetching data cats: {e}")
        return JsonResponse({"error": "Failed successfully!", "message": str(e)})

    finally:
        cursor.close()
        connection.close()



@api_view(['PUT'])
@permission_classes([AllowAny])
def add_discount(request):

    connection, cursor = get_sql_anywhere_connection()
    print("here a discount")

    print(request.data)
    try:
        if not request.data['org_id'] :
            print("not f3ln")
            return JsonResponse({"error": "Failed successfully, Please fill all the required fields!"})
        print("not not ")
        print(request.data)  
        for i in request.data['units'] :
         print("this  is 111")   
         print(i)

         if not  i['qty']:
                continue
         data = {
                # 'Parent_id':  0 if request.data['catID'] == [] else request.data['catID'] ,
                'Created_By': request.data['created_by'],
                'Created_on': request.data['created_on'],
                'Org_ID': request.data['org_id'],
                'Discount_Name': request.data['Discount_Name'],
                'Discount_Code': request.data['Discount_Code'],
                'Discount_Description': request.data['Discount_Description'],
                # 'Type': request.data['Type'],
                'ProductID': request.data['Type']['ProductID'],
                'Discount_Amount': i['qty'],
                'Valid_From': request.data['starts_at'],
                'Valid_To': request.data['expiers_at'],
                'is_customer': request.data['is_customer'],
                'Customer_ID': request.data['Customer_ID'],
                'Status' : request.data['Stat'],
                # 'is_fixed': request.data['is_fixed'],
                'Dis_type_code' : request.data['is_fixed'],
                'Discount_MaxUses_User': request.data['Discount_MaxUses_User'],
                'Discount_MaxUses': request.data['Discount_MaxUses'],
                'UOM' : i['altUnit'],

                # 'Status': 1 if request.data['Stat'] == "true" else 0,
                # 'Photo' :  image_path,
        }
         print("plzz workkkk", data)

         query = f"""
            INSERT INTO "dba"."Discount" ({', '.join(data.keys())})
            VALUES ({', '.join(['?' for _ in data.values()])})
        """
         cursor.execute(query, list(data.values()))
         connection.commit()

         print("Data inserted successfully.")
        return JsonResponse({"message": "Added successfully!"}, status=200)

    except Exception as e:
        print("failed")
        error_message = str(e)
        print(f"Error inserting data: {error_message}")
        return JsonResponse({"error": f"Failed to insert data: {error_message}"}, status=500)

    finally:
        cursor.close()
        connection.close()

@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def fetch_a_discount(request):
    try:
        connection, cursor = get_sql_anywhere_connection()
        print("ciddd discount")
        cid = request.data['id']
        org_id = request.data['org_id']

        print(cid)
        query = "SELECT * FROM \"dba\".\"Discount\" WHERE Discount_Code = ? AND Org_ID = ?"
        cursor.execute(query, (cid , org_id))
        rows = cursor.fetchall()

        uom_list = [] 
        data_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

        for row in data_list:
            uom_list.append({
                'UOM': row['UOM'],
                'Discount_Amount': row['Discount_Amount']
            })

        print('UOM List:')
        print(uom_list)

        print('Data List:')
        print(data_list)
        p = {'label': '5411 d', 'ProductID': 5411}

        return JsonResponse({"message": "Fetched successfully.", "data": data_list, "uom_list": uom_list, "p": p })
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": f"Failed to fetch Product: {str(e)}"}, status=500)
    finally:
        cursor.close()
        connection.close()


@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_discount(request):
    connection, cursor = get_sql_anywhere_connection()
    try:
        print(request.data)

        delete_query = "DELETE FROM \"dba\".\"Discount\" WHERE Discount_Code = ?"
        cursor.execute(delete_query, (request.data['Discount_Code'],))
        connection.commit()

        for i in request.data['units'] :
            print("this is 111")
            print(i)
            if  i['UOM'] == '':
               continue

            if  i['Discount_Amount'] == '':
              continue

            # else :
            #     d = i['Discount_Amount']  
            #     u = i['UOM']
            #     print("not null f3lan")


            data = {
                'Created_By': request.data['Created_By'],
                'Created_on': request.data['Created_on'],
                'Status' : request.data['Stat'],
                'Org_ID': request.data['org_id'],
                'Discount_Name': request.data['Discount_Name'],
                'Discount_Code': request.data['Discount_Code'],
                'Discount_Description': request.data['Discount_Description'],
                'ProductID': request.data['Type']['ProductID'],
                'Discount_Amount':  i['Discount_Amount'],
                'Valid_From': request.data['starts_at'],
                'Valid_To': request.data['expiers_at'],
                'is_customer': request.data['is_customer'],
                'Customer_ID': request.data['Customer_ID'],
                'Dis_type_code': request.data['is_fixed'],
                'Discount_MaxUses_User': request.data['Discount_MaxUses_User'],
                'Discount_MaxUses': request.data['Discount_MaxUses'],
                'UOM': i['UOM'],
            }

            query = f"""
                INSERT INTO "dba"."Discount" ({', '.join(data.keys())})
                VALUES ({', '.join(['?' for _ in data.values()])})
            """
            cursor.execute(query, list(data.values()))
            connection.commit()

        print("Discounts updated successfully.")
        return JsonResponse({"message": "Discounts updated successfully."}, status=200)

    except Exception as e:
        print(f"Error updating discounts: {e}")
        return JsonResponse({"error": f"Failed to update discounts: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()



@api_view(['PUT'])
@permission_classes([AllowAny])
def delete_discount(request):
    connection, cursor = get_sql_anywhere_connection()
    try:
        org_id = request.data['org_id']
        cursor.execute(
                "SELECT COUNT(*) FROM \"dba\".\"Order_Item\" WHERE \"Discount_Code\" = ? AND \"Org_ID\" = ?",
                [request.data['Discount_Code'], org_id]
            )
        count = cursor.fetchone()[0]

        if count > 0:
                print("cannot delete disc")
                return JsonResponse({"message": "disc in use.", "use": "true"}, status=200)

        else :
            delete_query = "DELETE FROM \"dba\".\"Discount\" WHERE Discount_Code = ?"
            cursor.execute(delete_query, (request.data['Discount_Code'],))
            connection.commit()

       
        print("Discounts deleted successfully.")
        return JsonResponse({"message": "Discounts updated successfully."}, status=200)

    except Exception as e:
        print(f"Error updating discounts: {e}")
        return JsonResponse({"error": f"Failed to update discounts: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()

from datetime import datetime

@api_view(['PUT'])
@permission_classes([AllowAny])
def add_bonusbuy(request):

    connection, cursor = get_sql_anywhere_connection()
    print(request.data)
    org_id = request.data['org_id']

    try:
        if not request.data['code'] :
            print("not f3ln")
            return JsonResponse({"error": "Failed , Please fill all the required fields!"}, status=400)
        print("not not ")
        # if 'Img' in request.FILES:
        #  avatar = request.FILES['Img']
        # # if avatar == "http://127.0.0.1:8000"+ str(user.Img.url):
        # #   image_path=user.Img.url
        # # else:  
        #  image_path = default_storage.save('images/' + avatar.name, ContentFile(avatar.read()))
        # t =  request.data['taxes'] + 0.00
        bonus_id = request.data['code']
        cursor.execute(
                "SELECT COUNT(*) FROM \"dba\".\"BonusBuy_HD\" WHERE \"Code\" = ? AND \"Org_ID\" = ?",
                [bonus_id, org_id]
            )
        count = cursor.fetchone()[0]

        if count > 0:
                print("cannot add bonus buy")
                return JsonResponse({"message": "Code already in use.", "use": "true"}, status=200)
        time_only = ""
        time_only2 = ""

        if  request.data['Valid_Time_From'] != '' :       
            datetime_string = request.data['Valid_Time_From']

            datetime_object = datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S.%fZ')

            time_only = datetime_object.time()

        if  request.data['Valid_Time_To'] != '' :       

            datetime_string2 = request.data['Valid_Time_To']

            datetime_object2 = datetime.strptime(datetime_string2, '%Y-%m-%dT%H:%M:%S.%fZ')

            time_only2 = datetime_object2.time()

        data = {
                'Code': request.data['code'],
                'Valid_From': request.data['Valid_From'],
                'Valid_To': request.data['Valid_To'],
                'Org_ID': org_id,
                'Valid_Time_From': time_only,
                'Offer_Amount' : request.data['offerAmount'],
                'Status' : request.data['Status'],
                'Valid_Time_To': time_only2,
                'Type': request.data['Type'],
                'Applied_On': request.data['applied_on'],               
                'Target_Quantity': request.data['Target_Quantity'],
                # 'Name_AR': request.data['nameAR'],
                'DescriptionEN': request.data['DescEN'],
                'DescriptionAR': request.data['DescAR'],
        }

        print("plzz workkkk", data)

        query = f"""
            INSERT INTO "dba"."BonusBuy_HD" ({', '.join(data.keys())})
            VALUES ({', '.join(['?' for _ in data.values()])})
        """
        cursor.execute(query, list(data.values()))
        connection.commit()

        if  int(request.data['cond_itemQty']) > 0 :
            data = {
                    'Code': request.data['code'],
                    'Type' : 1,
                    'Quantity': request.data['cond_itemQty'],
                    'Min_amount': request.data['Min_amount'],
                    'Org_ID': org_id,
                    'Restricted_Item': request.data['Restricted_Item'],
                    # 'Valid_Time_To': request.data['Valid_Time_To'],
                    # 'Type': request.data['Type'],
                    # 'Applied_On': request.data['Applied_On'],               
                    # 'Name': request.data['name'],
                    # 'Name_AR': request.data['nameAR'],
                    # 'DescriptionEN': request.data['DescEN'],
                    # 'DescriptionAR': request.data['DescAR'],
            }

            print("plzz workkkk", data)

            query = f"""
                INSERT INTO "dba"."BonusBuy_Prerequist_Condition" ({', '.join(data.keys())})
                VALUES ({', '.join(['?' for _ in data.values()])})
            """
            cursor.execute(query, list(data.values()))
            connection.commit()

        if  int(request.data['Min_amount']) > 0 :
            data = {
                    'Code': request.data['code'],
                    'Type' : 0,
                    'Quantity': request.data['cond_itemQty'],
                    'Min_amount': request.data['Min_amount'],
                    'Org_ID': org_id,
                    'Restricted_Item': request.data['Restricted_Item'],
                    # 'Valid_Time_To': request.data['Valid_Time_To'],
                    # 'Type': request.data['Type'],
                    # 'Applied_On': request.data['Applied_On'],               
                    # 'Name': request.data['name'],
                    # 'Name_AR': request.data['nameAR'],
                    # 'DescriptionEN': request.data['DescEN'],
                    # 'DescriptionAR': request.data['DescAR'],
            }

 

            query = f"""
            INSERT INTO "dba"."BonusBuy_Prerequist_Condition" ({', '.join(data.keys())})
            VALUES ({', '.join(['?' for _ in data.values()])})
        """
            cursor.execute(query, list(data.values()))
            connection.commit()


        # for i in alts:
        #     print(i)
        #     print("heresss altsss")
        #     if not i['altUnit'] :
        #     # or i['base'] or i['qty']:
        #         continue
        #     cursor.execute(f"INSERT INTO \"dba\".\"Product_Uom\" (Product_Id , UOM, Conv_Factor, UOMBaseQty,Price ,Org_ID) VALUES (?, ?, ?, ?,?, ?)", 
        #     [cID, i['altUnit'] ,i['base'], i['qty'],i['price'] ,org_id])
        #     connection.commit()  
        if request.data['ProductID'] or  request.data['CategoryID'] :
            data = {
                    'Code': request.data['code'],
                    'ProductID': request.data['ProductID'],
                    'CategoryID': request.data['CategoryID'],
                    'Quantity': request.data['itemQty'],
                    'Org_ID': org_id,

            }

            print("plzz workkkk", data)

            query = f"""
                INSERT INTO "dba"."BonusBuy_Prerequist_item" ({', '.join(data.keys())})
                VALUES ({', '.join(['?' for _ in data.values()])})
            """
            cursor.execute(query, list(data.values()))
            connection.commit()

            print("Data inserted successfully.")
        items = []
        items = request.data['items']
        print(request.data['items'])
        for i in items:
         data = {
                'Code': request.data['code'],
                'ProductID': i['value']['ProductID'] if i['Status'] == 1 else 0,
                'CategoryID':  i['value']['ProductID'] if i['Status'] == 0 else 0,
                'Quantity': i['Stock'],
                'Org_ID': org_id,
            }

         print("items r here", data)

         query = f"""
            INSERT INTO "dba"."BonusBuy_Prerequist_item" ({', '.join(data.keys())})
            VALUES ({', '.join(['?' for _ in data.values()])})
        """
         cursor.execute(query, list(data.values()))   
         connection.commit()
         print("items inserted dd") 
        if request.data['ProductID'] or  request.data['CategoryID'] :

            data = {
                    'Code': request.data['code'],
                    'ProductID': request.data['ProductID2'],
                    'CategoryID': request.data['CategoryID2'],
                    # 'Quantity': request.data['itemQty'],
                    'Org_ID': org_id,

            }

            print("plzz workkkk", data)

            query = f"""
                INSERT INTO "dba"."BonusBuy_Prerequist_target" ({', '.join(data.keys())})
                VALUES ({', '.join(['?' for _ in data.values()])})
            """
            cursor.execute(query, list(data.values()))
            connection.commit()



            print("Data inserted successfully.")
        targets = []
        targets = request.data['targets']
        print(request.data['targets'])
        for t in targets:
         data = {
                'Code': request.data['code'],
                'ProductID': t['value']['ProductID'] if t['Status'] == 1 else 0,
                'CategoryID':  t['value']['ProductID'] if t['Status'] == 0 else 0,
                # 'Quantity': i['Stock'],
                'Org_ID': org_id,
            }

         print("targetsss r here", data)

         query = f"""
            INSERT INTO "dba"."BonusBuy_Prerequist_target" ({', '.join(data.keys())})
            VALUES ({', '.join(['?' for _ in data.values()])})
        """
         cursor.execute(query, list(data.values()))   
         connection.commit()
         print("targets inserted dd") 

        
        return JsonResponse({"message": "Added successfully!"}, status=200)
    
    except Exception as e:
        print("failed")
        error_message = str(e)
        print(f"Error inserting data: {error_message}")
        return JsonResponse({"error": f"Failed to insert data: {error_message}"}, status=500)

    finally:
        cursor.close()
        connection.close()
     

@api_view(['PUT'])
@permission_classes([AllowAny])
def fetch_bonusBuy(request):
    print("fetch_bonusBuy")
    connection, cursor = get_sql_anywhere_connection()
    try:
        query = """
            SELECT B.*, D.Name AS Disc_name
            FROM "dba"."BonusBuy_HD" AS B
            INNER JOIN "dba"."Discount_Type" AS D ON B.Type = D.Dis_type_code       
            WHERE B.Org_ID = ? AND D.Org_ID = ?
        """
        org_id = request.data.get('org_id')
        if org_id is None:
            raise ValueError("org_id is missing in the request data")

        cursor.execute(query, [org_id, org_id])
        rows = cursor.fetchall()
        rows_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

        if not rows_list:
            return JsonResponse({"message": "No data found!", "data": []})

        print(rows_list[0])
        return JsonResponse({"message": "Fetched successfully!", "data": rows_list})

    except Exception as e:
        print(f"Error fetching data prods: {e}")
        return JsonResponse({"error": "Failed successfully!", "message": str(e)})

    finally:
        cursor.close()
        connection.close()




@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def fetch_a_bonusbuy(request):
    try: 
        print("function invocked")
        connection, cursor = get_sql_anywhere_connection()
        print("ciddd")
        cid = request.data['code']
        org_id = request.data['org_id']

        print(cid)
        query = "SELECT * FROM \"dba\".\"BonusBuy_HD\" WHERE Code = ? AND Org_ID = ?"
        cursor.execute(query, (cid , org_id))
        # result = cursor.fetchall()
        # cursor.execute(query)  
        rows = cursor.fetchall()
        print(rows)
        data_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]


        query = "SELECT * FROM \"dba\".\"BonusBuy_Prerequist_Condition\" WHERE Code = ? AND Org_ID = ?"
        cursor.execute(query, (cid , org_id))
        # result = cursor.fetchall()
        # cursor.execute(query)  
        rows_conds = cursor.fetchall()    
        # print(rows)

        conds_data_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows_conds]
        print("thezzze r rows_conds")

        print(conds_data_list)


        query = "SELECT * FROM \"dba\".\"BonusBuy_Prerequist_item\" WHERE Code = ? AND Org_ID = ?"
        cursor.execute(query, (cid , org_id))
        # result = cursor.fetchall()
        # cursor.execute(query)  
        rows_items = cursor.fetchall()
        # print(rows)

        itmes_data_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows_items]
        print("thezzze r items")

        print(itmes_data_list)


        query = "SELECT * FROM \"dba\".\"BonusBuy_Prerequist_target\" WHERE Code = ? AND Org_ID = ?"
        cursor.execute(query, (cid , org_id))
        # result = cursor.fetchall()
        # cursor.execute(query)  
        rows_targets = cursor.fetchall()
        # print(rows)

        targets_data_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows_targets]
        print("thezzze r items")

        print(targets_data_list)     

        return JsonResponse({"message": "Fetched successfully.", "data" : data_list, "conds": conds_data_list, "items": itmes_data_list, "targets" :targets_data_list})
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": f"Failed to fetch offer: {str(e)}"}, status=500)
    finally:
        cursor.close()
        connection.close()


@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_bonusBuy(request):

    # if not request.data['catID'] or not request.data['org_Id'] :
    #   ret urn JsonResponse({"error": "Failed successfully, Please fill all the required fields!"})
    print("rrrrequest.data")  
    print(request.data)  
    connection, cursor = get_sql_anywhere_connection()
    # mat_id = request.data['code']
    # cursor.execute(
    #             "SELECT COUNT(*) FROM \"dba\".\"Product\" WHERE \"ProductID\" = ? AND \"Org_ID\" = ?",
    #             [mat_id, org_id]
    #         )
    # count = cursor.fetchone()[0]

    # if count > 0:
    #           print("cannot add mat")
    #           return JsonResponse({"message": "Product's code already in use.", "use": "true"}, status=200)

    try:
        code = request.data['code']
        org_id = request.data['org_id']
        print("here r items 34")
        for i in request.data['targets'] :
            print("this targettts")
            print(i)
        #  print(request.data['items'])
        # query_fetch = f"SELECT * FROM \"dba\".\"Product\" WHERE \"Code\" = ? "
        # cursor.execute(query_fetch, [catID ])
        # existing_data = cursor.fetchone()
        # print(request.data)
        # if existing_data:
        time_only = ""
        time_only2 = ""

        if  request.data['Valid_Time_From'] != '' :       
            datetime_string = request.data['Valid_Time_From']

            datetime_object = datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S.%fZ')

            time_only = datetime_object.time()

        if  request.data['Valid_Time_To'] != '' :       

            datetime_string2 = request.data['Valid_Time_To']

            datetime_object2 = datetime.strptime(datetime_string2, '%Y-%m-%dT%H:%M:%S.%fZ')

            time_only2 = datetime_object2.time()

        data = {
                # 'Code': request.data['code'],
                # 'Valid_From': request.data['Valid_From'],
                # 'Valid_To': request.data['Valid_To'],
                'Org_ID': org_id,
                'Valid_Time_From': time_only,
                'Valid_Time_To': time_only2,
                'Type': request.data['Type'],
                'Applied_On': request.data['applied_on'],               
                'Target_Quantity': request.data['Target_Quantity'],
                # 'Name_AR': request.data['nameAR'],
                'DescriptionEN': request.data['DescEN'],
                'DescriptionAR': request.data['DescAR'],
        }
        
        print("existing_data")
        # print(request.data['alts'])
        # print(existing_data)  
        update_columns = ', '.join([f'"{col}" = ?' for col in data.keys()])
        query_update = f"UPDATE \"dba\".\"BonusBuy_HD\" SET {update_columns} WHERE \"Code\" = ? AND Org_ID = ?" 
        cursor.execute(query_update, list(data.values()) + [code , org_id])
        connection.commit()
        


        # alts = request.data['alts']
        # stores = request.data['stores']

        # print(code)
        # print(alts)

        query = "SELECT * FROM \"dba\".\"BonusBuy_Prerequist_Condition\" WHERE Code = ? AND Org_ID = ?"
        cursor.execute(query, (code, org_id))
        result = cursor.fetchall()
        print("el result")

        print(result)
        if result:
                print("therez result el7")
                c=0
                # print( result[1][1])
                for i in result:
                    print("herererer")
                    print(i[1])
                    query = "DELETE FROM \"dba\".\"BonusBuy_Prerequist_Condition\" WHERE Code = ? AND Org_ID = ? AND Type = ?"
                    cursor.execute(query, (code ,org_id ,i[1]))
                    connection.commit()
                    print("thattzz i[1]", i[1])

                    print("deleted", i)
                    # c=c+1
                    # continue
                # else :
                #    cursor.execute(f"INSERT INTO \"dba\".\"permissions_admins\" (PID , UID) VALUES (? , ?)", [i , request.data['UID']])
                #    connection.commit()  

        if  int(request.data['cond_itemQty']) > 0 :
            data = {
                    'Code': request.data['code'],
                    'Type' : 1,
                    'Quantity': int(request.data['cond_itemQty']),
                    'Min_amount': float(request.data['Min_amount']),
                    'Org_ID': org_id,
                    'Restricted_Item': request.data['Restricted_Item'],
                    # 'Valid_Time_To': request.data['Valid_Time_To'],
                    # 'Type': request.data['Type'],
                    # 'Applied_On': request.data['Applied_On'],               
                    # 'Name': request.data['name'],
                    # 'Name_AR': request.data['nameAR'],
                    # 'DescriptionEN': request.data['DescEN'],
                    # 'DescriptionAR': request.data['DescAR'],
            }

            print("plzz workkkk", data)

            query = f"""
                INSERT INTO "dba"."BonusBuy_Prerequist_Condition" ({', '.join(data.keys())})
                VALUES ({', '.join(['?' for _ in data.values()])})
            """
            cursor.execute(query, list(data.values()))
            connection.commit()

        if  float(request.data['Min_amount']) > 0.00 :
            data = {
                    'Code': request.data['code'],
                    'Type' : 0,
                    'Quantity': int(request.data['cond_itemQty']),
                    'Min_amount': float(request.data['Min_amount']),
                    'Org_ID': org_id,
                    'Restricted_Item': request.data['Restricted_Item'],
                    # 'Valid_Time_To': request.data['Valid_Time_To'],
                    # 'Type': request.data['Type'],
                    # 'Applied_On': request.data['Applied_On'],               
                    # 'Name': request.data['name'],
                    # 'Name_AR': request.data['nameAR'],
                    # 'DescriptionEN': request.data['DescEN'],
                    # 'DescriptionAR': request.data['DescAR'],
            }

 

            query = f"""
            INSERT INTO "dba"."BonusBuy_Prerequist_Condition" ({', '.join(data.keys())})
            VALUES ({', '.join(['?' for _ in data.values()])})
        """
            cursor.execute(query, list(data.values()))
            connection.commit()

        query = "SELECT * FROM \"dba\".\"BonusBuy_Prerequist_item\" WHERE Code = ? AND Org_ID = ?"
        cursor.execute(query, (code, org_id))
        result = cursor.fetchall()
        print("el result")

        print(result)
        if result:
                print("therez result el7")
                c=0
                # print( result[1][1])
                for i in result:
                    print("herererer")
                    print(i[1])
                    query = "DELETE FROM \"dba\".\"BonusBuy_Prerequist_item\" WHERE Code = ? AND Org_ID = ? AND item_id = ?"
                    cursor.execute(query, (code ,org_id ,i.item_id))
                    connection.commit()
                    print("thattzz i[1]", i[1])

                    print("deleted", i)
                    # c=c+1
                    # continue
                # else :
                #    cursor.execute(f"INSERT INTO \"dba\".\"permissions_admins\" (PID , UID) VALUES (? , ?)", [i , request.data['UID']])
                #    connection.commit()  
    

        items = []
        items = request.data['items']
        print(request.data['items'])
        for i in items:
         data = {
                'Code': request.data['code'],
                'ProductID': i['value']['ProductID'] if i['Status'] == 1 else 0,
                'CategoryID':  i['value']['ProductID'] if i['Status'] == 0 else 0,
                'Quantity': i['Stock'],
                'Org_ID': org_id,
            }

         print("items r here", data)

         query = f"""
            INSERT INTO "dba"."BonusBuy_Prerequist_item" ({', '.join(data.keys())})
            VALUES ({', '.join(['?' for _ in data.values()])})
        """
         cursor.execute(query, list(data.values()))   
         connection.commit()
         print("items inserted dd") 
    



        print("here comes a target")
        query = "SELECT * FROM \"dba\".\"BonusBuy_Prerequist_target\" WHERE Code = ? AND Org_ID = ?"
        cursor.execute(query, (code, org_id))
        result = cursor.fetchall()
        print("el result")

        print(result)
        if result:
                print("therez result el7")
                c=0
                # print( result[1][1])
                for i in result:
                    print("herererer")
                    print(i[1])
                    query = "DELETE FROM \"dba\".\"BonusBuy_Prerequist_target\" WHERE Code = ? AND Org_ID = ? AND item_id = ?"
                    cursor.execute(query, (code ,org_id ,i.item_id))
                    connection.commit()
                    print("thattzz target i[1]", i[1])

                    print("deleted", i)
                    # c=c+1
                    # continue
                # else :
                #    cursor.execute(f"INSERT INTO \"dba\".\"permissions_admins\" (PID , UID) VALUES (? , ?)", [i , request.data['UID']])
                #    connection.commit()  
    

        items = []
        items = request.data['targets']
        print(request.data['targets'])
        for i in items:
         data = {
                'Code': request.data['code'],
                'ProductID': i['value']['ProductID'] if i['Status'] == 1 else 0,
                'CategoryID':  i['value']['ProductID'] if i['Status'] == 0 else 0,
                # 'Quantity': i['Stock'],
                'Org_ID': org_id,
            }

         print("targetttss r here", data)

         query = f"""
            INSERT INTO "dba"."BonusBuy_Prerequist_target" ({', '.join(data.keys())})
            VALUES ({', '.join(['?' for _ in data.values()])})
        """
         cursor.execute(query, list(data.values()))   
         connection.commit()
         print("targetsss inserted dd")         


        return JsonResponse({"message": "offer updated successfully!"}, status=200)
        # else:
        #     return JsonResponse({"error": f"Category with ID {catID} not found."}, status=404)

    except Exception as e:
        print(str(e))
        return JsonResponse({"error": f"Failed to update offer: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()

