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

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

@api_view(['GET'])
@permission_classes([AllowAny])
def fetch_cat(request):
    print("catsss")
    connection, cursor = get_sql_anywhere_connection()
    try:
      query = "SELECT * FROM \"dba\".\"Categories\""
      cursor.execute(query)  
      rows = cursor.fetchall()
      rows_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

      return JsonResponse({"message": "Fetched successfully!", "data": rows_list})


    except Exception as e:
        print(f"Error fetching data: {e}")
        return JsonResponse({"error": "Failed successfully!", "message": str(e)})

    finally:
        cursor.close()
        connection.close()

@api_view(['GET'])
@permission_classes([AllowAny])
def fetch_uom(request):
    print("uommm")
    connection, cursor = get_sql_anywhere_connection()
    try:
      query = "SELECT * FROM \"dba\".\"UOM\""
      cursor.execute(query)  
      rows = cursor.fetchall()
      rows_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

      return JsonResponse({"message": "Fetched successfully!", "data": rows_list})


    except Exception as e:
        print(f"Error fetching data: {e}")
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
        print(request.data)
        if existing_data:
            data = {
                # 'id': request.data['catID'],
                'Parent_id': request.data['Parent_id'],
                # 'Created_By': request.data['created_by'],
                'View_Order': request.data['view'],
                # 'RegKey': request.data['storeRegKey'],
                'LChange_By': request.data['LChange_By'],
                'LChange_On': request.data['LChange_On'],
                'Status': request.data['Stat'],
                'Name': request.data['name'],
                'Description': request.data['Desc'],
            }
            print("existing_data")  

            print(existing_data)  
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
        data = {
                'Parent_id': request.data['Parent_id'],
                'Created_By': request.data['created_by'],
                'Created_on': request.data['created_on'],
                'Org_ID': request.data['org_Id'],
                'View_Order': request.data['view'],
                'LChange_By': request.data['LChange_By'],
                'LChange_On': request.data['LChange_On'],
                'Status': request.data['Stat'],
               
                'Name': request.data['name'],
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
        print(cid)
        query = "SELECT * FROM \"dba\".\"Categories\" WHERE Parent_id = ? "
        cursor.execute(query, (cid))
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


@api_view(['PUT'])
@permission_classes([AllowAny])
def add_product(request):

    connection, cursor = get_sql_anywhere_connection()
    print(request.data)
    try:
        if not request.data['code'] :
            print("not f3ln")
            return JsonResponse({"error": "Failed successfully, Please fill all the required fields!"}, status=400)
        print("not not ")
        data = {
                'Code': request.data['code'],
                'Created_By': request.data['created_by'],
                'Created_on': request.data['created_on'],
                # 'Org_ID': request.data['org_Id'],
                'Base_UOM': request.data['Base_UOM'],
                'Lchange_By': request.data['LChange_By'],
                'Lchange_On': request.data['LChange_On'],
                'Status': request.data['Stat'],               
                'Name': request.data['name'],
                'DescriptionEN': request.data['DescEN'],
                'DescriptionAR': request.data['DescAR'],
                'Category_Id': request.data['Category_Id'],
                # 'Current_Stock' : request.data['Current_Stock'],
                'Prod_Date' : request.data['Prod_Date'],
                'Expiry_Date' : request.data['Expiry_Date'],
                'Type' : request.data['type'],
                'Note' : request.data['note'],
                'Unit_Price' : request.data['unit'],





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
            if not i['altUnit'] :
            # or i['base'] or i['qty']:
                continue
            cursor.execute(f"INSERT INTO \"dba\".\"Product_Uom\" (Product_Id , UOM, Conv_Factor, UOMBaseQty, Org_ID) VALUES (?, ?, ?, ?, ?)", 
            [cID, i['altUnit'] ,i['base'], i['qty'], 1])
            connection.commit()  

        for i in stores:
            print(i)
            if not i['Store_ID'] :
            # or i['base'] or i['qty']:
                continue
            cursor.execute(f"INSERT INTO \"dba\".\"Product_Store_Stock\" (Product_id , Store_Id, Stock, Org_ID) VALUES (?, ?, ?, ?)", 
            [cID, i['Store_ID'] ,i['Stock'], 1])
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


@api_view(['GET'])
@permission_classes([AllowAny])
def fetch_products(request):
    print("fetch_products")
    connection, cursor = get_sql_anywhere_connection()
    try:
      query = "SELECT * FROM \"dba\".\"Product\""
      cursor.execute(query)  
      rows = cursor.fetchall()
      rows_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

      return JsonResponse({"message": "Fetched successfully!", "data": rows_list})


    except Exception as e:
        print(f"Error fetching data: {e}")
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
        print(cid)
        query = "SELECT * FROM \"dba\".\"Product\" WHERE Code = ? "
        cursor.execute(query, (cid))
        # result = cursor.fetchall()
        # cursor.execute(query)  
        rows = cursor.fetchall()
        print(rows)
        data_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]


        query = "SELECT * FROM \"dba\".\"Product_Uom\" WHERE Product_Id = ? "
        cursor.execute(query, (cid))
        # result = cursor.fetchall()
        # cursor.execute(query)  
        rows_alt = cursor.fetchall()
        # print(rows)

        alt_data_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows_alt]
        print("thezzze r altsss")

        print(alt_data_list)


        query = "SELECT * FROM \"dba\".\"Product_Store_Stock\" WHERE Product_Id = ? "
        cursor.execute(query, (cid))
        # result = cursor.fetchall()
        # cursor.execute(query)  
        rows_stores = cursor.fetchall()
        # print(rows)

        stores_data_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows_stores]
        print("thezzze r storess")

        print(stores_data_list)

        return JsonResponse({"message": "Fetched successfully.", "data" : data_list, "alts": alt_data_list, "stores": stores_data_list})
    except Exception as e:
        return JsonResponse({"error": f"Failed to delete Category: {str(e)}"}, status=500)
    finally:
        cursor.close()
        connection.close()



@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_mat(request):

    # if not request.data['catID'] or not request.data['org_Id'] :
    #   return JsonResponse({"error": "Failed successfully, Please fill all the required fields!"})
      
    connection, cursor = get_sql_anywhere_connection()
    try:
        code = request.data['code']
        # org_Id = request.data['org_Id']
        # query_fetch = f"SELECT * FROM \"dba\".\"Product\" WHERE \"Code\" = ? "
        # cursor.execute(query_fetch, [catID ])
        # existing_data = cursor.fetchone()
        # print(request.data)
        # if existing_data:
        data = {
                'Code': request.data['code'],
                # 'Created_By': request.data['created_by'],
                # 'Created_on': request.data['created_on'],
                # 'Org_ID': request.data['org_Id'],
                'Base_UOM': request.data['Base_UOM'],
                'Lchange_By': request.data['LChange_By'],
                'Lchange_On': request.data['LChange_On'],
                'Status': request.data['Stat'],               
                'Name': request.data['name'],
                'DescriptionEN': request.data['DescEN'],
                'DescriptionAR': request.data['DescAR'],
                'Category_Id': request.data['Category_Id'],
                # 'Current_Stock' : request.data['Current_Stock'],
                'Prod_Date' : request.data['Prod_Date'],
                'Expiry_Date' : request.data['Expiry_Date'],
                'Type' : request.data['type'],
                'Note' : request.data['note'],
                'Unit_Price' : request.data['unit'],
            }
        print("existing_data")  
        print(request.data['alts'])
        # print(existing_data)  
        update_columns = ', '.join([f'"{col}" = ?' for col in data.keys()])
        query_update = f"UPDATE \"dba\".\"Product\" SET {update_columns} WHERE \"Code\" = ?"
        cursor.execute(query_update, list(data.values()) + [code])
        connection.commit()


        alts = request.data['alts']
        stores = request.data['stores']

        print(code)
        print(alts)

        query = "SELECT * FROM \"dba\".\"Product_Uom\" WHERE Product_Id = ? "
        cursor.execute(query, code)
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
                    query = "DELETE FROM \"dba\".\"Product_Uom\" WHERE Product_Id = ? AND UOM = ?"
                    cursor.execute(query, (code , i[1]))
                    connection.commit()
                    print("thattzz i[1]", i[1])

                    print("deleted", i)
                    # c=c+1
                    # continue
                # else :
                #    cursor.execute(f"INSERT INTO \"dba\".\"permissions_admins\" (PID , UID) VALUES (? , ?)", [i , request.data['UID']])
                #    connection.commit()  

  
        for i in alts:
            print(i)
            if not i['UOM'] :
            # or i['base'] or i['qty']:
                continue
            cursor.execute(f"INSERT INTO \"dba\".\"Product_Uom\" (Product_Id , UOM, Conv_Factor, UOMBaseQty, Org_ID) VALUES (?, ?, ?, ?, ?)", 
            [code, i['UOM'] ,i['Conv_Factor'], i['UOMBaseQty'], 1])
            connection.commit()  


        query = "SELECT * FROM \"dba\".\"Product_Store_Stock\" WHERE Product_id = ? "
        cursor.execute(query, code)
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
                    query = "DELETE FROM \"dba\".\"Product_Store_Stock\" WHERE Product_id = ? AND Store_Id = ?"
                    cursor.execute(query, (code , i[2]))
                    connection.commit()
                    print("thattzz i[2]", i[2])

                    print("deleted", i)
                    # c=c+1
                    # continue
                # else :
                #    cursor.execute(f"INSERT INTO \"dba\".\"permissions_admins\" (PID , UID) VALUES (? , ?)", [i , request.data['UID']])
                #    connection.commit()  

  
        for i in stores:
            print(i)
            if not i['Store_Id'] :
            # or i['base'] or i['qty']:
                continue
            cursor.execute(f"INSERT INTO \"dba\".\"Product_Store_Stock\" (Product_Id , Store_Id,  Stock, Org_ID) VALUES (?, ?, ?, ?)", 
            [code, i['Store_Id'] ,i['Stock'],  1])
            connection.commit()  



        return JsonResponse({"message": "Category updated successfully!"}, status=200)
        # else:
        #     return JsonResponse({"error": f"Category with ID {catID} not found."}, status=404)

    except Exception as e:
        return JsonResponse({"error": f"Failed to update store: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()
