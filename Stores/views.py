from django.shortcuts import render
from  database_connection import get_sql_anywhere_connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse

@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_store(request):

    if not request.data['storeID'] or not request.data['storeNameEN'] or not request.data['storeNumR']:
      return JsonResponse({"error": "Failed successfully, Please fill all the required fields!"},status=500)
    print(request.data)

    connection, cursor = get_sql_anywhere_connection()
    try:
        store_id = request.data['storeID']
        org_id = request.data['org_id']

        query_fetch = f"SELECT * FROM \"dba\".\"Stores\" WHERE \"Store\" = ? AND \"Org_ID\" = ? "
        cursor.execute(query_fetch, [store_id , org_id])
        existing_data = cursor.fetchone()
        print(request.data)
        if existing_data:
            store_data = {
                'store': request.data['storeID'],
                'ip': request.data['storeIP'],
                'store_name': request.data['storeNameEN'],
                'store_name_ar': request.data['storeNameAR'],
                # 'RegKey': request.data['storeRegKey'],
                'Lat': request.data['long'],
                'Lan': request.data['lat'],
                'number_range': request.data['storeNumR'],
                'region_id': request.data['storeRegion'],
                'delivery': request.data['storeDel'],
                'isTouristic':request.data['storeTouristic'],
                'status': request.data['storeStat'],
                'NetworkType': request.data['storeNetType'],
                'store_location': request.data['storeLoc'],
            }

            update_columns = ', '.join([f'"{col}" = ?' for col in store_data.keys()])
            query_update = f"UPDATE \"dba\".\"Stores\" SET {update_columns} WHERE \"Store\" = ? AND \"Org_ID\" = ? "

            cursor.execute(query_update, list(store_data.values()) + [store_id , org_id])
            connection.commit()

            return JsonResponse({"message": "Store updated successfully!"}, status=200)
        else:
            return JsonResponse({"error": f"Store with ID {store_id} not found."}, status=404)

    except Exception as e:
        print(str(e))
        return JsonResponse({"error": f"Failed to update store: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_store(request):
    try:
        connection, cursor = get_sql_anywhere_connection()
        store_id = request.data['Store']
        org_id = request.data['org_id']
    
        print(store_id)
        cursor.execute(f"DELETE FROM \"dba\".\"Stores\" WHERE \"Store\" = ? AND \"Org_ID\" = ?", [store_id, org_id])
        
        connection.commit()  

        return JsonResponse({"message": "Store deleted successfully."})
    except Exception as e:
        return JsonResponse({"error": f"Failed to delete store: {str(e)}"}, status=500)
    finally:
        cursor.close()
        connection.close()

from django.http import JsonResponse

@api_view(['PUT'])
@permission_classes([AllowAny])
def add_store(request):

    connection, cursor = get_sql_anywhere_connection()
   
    try:
        if not request.data['storeNameEN'] or not request.data['storeNumR'] or not request.data['org_id']:
            return JsonResponse({"error": "Failed successfully, Please fill all the required fields!"})
        org_id = request.data['org_id']
        print(request.data)
        store_data = {
            'store': request.data['storeID'],
            'ip': request.data['storeIP'],
            'store_name': request.data['storeNameEN'],
            'store_name_ar': request.data['storeNameAR'],
            'number_range': request.data['storeNumR'],
            'region_id': request.data['storeRegion'],
            'delivery': request.data['storeDel'],
            'isTouristic':1 if request.data['storeTouristic'] == "true" else 0,
            'status': request.data['storeStat'],
            'NetworkType': request.data['storeNetType'],
            'store_location': request.data['storeLoc'],
            'Lat': 0 if request.data['long'] == '' else float(request.data['long']),
            'Lan': 0 if request.data['lat'] == '' else float(request.data['lat']),
            'Org_ID' : org_id
        }

        query = f"""
            INSERT INTO "dba"."Stores" ({', '.join(store_data.keys())})
            VALUES ({', '.join(['?' for _ in store_data.values()])})
        """
        cursor.execute(query, list(store_data.values()))
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


from django.http import JsonResponse

@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def fetch_stores(request):
    connection, cursor = get_sql_anywhere_connection()

    try:
        org_id = request.data['org_id']
        # query = "SELECT * FROM \"dba\".\"Stores\" "
        if 'active' in request.data:
            cursor.execute(f"SELECT * FROM \"dba\".\"Stores\" WHERE \"Org_ID\" = ? AND \"Status\" = 1", [org_id])
        else:
            cursor.execute(f"SELECT * FROM \"dba\".\"Stores\" WHERE \"Org_ID\" = ?", [org_id])

        # cursor.execute(query)

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

def fetch_regions(request):
    connection, cursor = get_sql_anywhere_connection()
    try:
      query = "SELECT * FROM \"dba\".\"Regions\""
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
 