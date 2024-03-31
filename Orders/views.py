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


@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def fetch_orders (request) :
    try:
        org_id = request.data['org_id']

        connection, cursor = get_sql_anywhere_connection()
        query = """
   SELECT
    o.OrderNo,
    o.Org_ID,
    o.UserID,
    o.AddID,
    o.TotalAmount,
    o.Store_ID,
    o.Mth_ID,
    o.Note,
    o.Status,
    o.Tax_Amount,
    o.Sub_Total,
    o.Created_on,
    o.Created_at,
    o.Delivered_on,
    o.Delivered_at,
    o.Service_Amount,
    o.Cancelled_by,
    o.Cancelled_on,   
    o.CancellationReason,
    o.DriverID AS driver_id,
    u.FullName AS user_fullname,
    u.PhoneNo AS user_phonenumber,
    a.Address AS user_address,
    p.OrderNo,
    MAX(CASE WHEN p.Mth_ID = 1 THEN p.Amount ELSE 0 END) AS has_cash,
    MAX(CASE WHEN p.Mth_ID = 2 THEN p.Amount ELSE 0 END) AS has_visa,
    MAX(CASE WHEN p.Mth_ID = 3 THEN p.Amount ELSE 0 END) AS has_voucher
FROM
    "Order_HD" o
INNER JOIN
    "Users_HD" u ON o."UserID" = u.UserID AND u."Org_ID" = o."Org_ID"
INNER JOIN
    "Users_Address" a ON o."AddID" = a."AddID" AND a."Org_ID" = o."Org_ID"
INNER JOIN
    "Order_pay" p ON o."OrderNo" = p."OrderNo" AND p."Org_ID" = o."Org_ID"

WHERE
    o."Org_ID" = ?
GROUP BY
    o.OrderNo,
    o.Org_ID,
    o.UserID,
    o.AddID,
    o.TotalAmount,
    o.Store_ID,
    o.Mth_ID,
    o.Note,
    o.Status,
    o.Tax_Amount,
    o.Sub_Total,
    o.Created_on,
    o.Cancelled_by,
    o.Cancelled_on,
    o.CancellationReason,

    o.Created_at,
    o.Delivered_on,
    o.Delivered_at,
    o.Service_Amount,
    o.DriverID,
    
    u.FullName,
    u.PhoneNo,
    a.Address,
    p.OrderNo;
"""


        with connection.cursor() as cursor:
            cursor.execute(query, (org_id,))
            rows = cursor.fetchall()
            # print(rows)
            columns = [col[0] for col in cursor.description]
            rows_list = [dict(zip(columns, row)) for row in rows]
        print("rowsss")
        print(rows_list)
        return JsonResponse({"message": "Fetched successfully!", "data": rows_list})


    except Exception as e:
        print(str(e))
        return JsonResponse({"error": f"Failed to fetch orders: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()

@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def fetch_order_items(request):
    try:
        connection, cursor = get_sql_anywhere_connection()
        print("ciddd")
        cid = request.data['id']
        print(cid)
        org_id = request.data['org_id']
        query = """
            SELECT O.*, P.Name AS p_name, U.UOM_AName
            FROM "dba"."Order_Item" AS O
            INNER JOIN "dba"."Product" AS P ON O.ProductID = P.ProductID
            LEFT JOIN "dba"."UOM" AS U ON O.UOMStandardCode = U.UOMStandardCode
            WHERE O.OrderNo = ? AND O.Org_ID = ? AND P.Org_ID = ? AND  U.Org_ID = ?
        """

        # query = "SELECT * FROM \"dba\".\"Order_Item\" WHERE OrderNo = ? AND Org_ID = ?"
        cursor.execute(query, (cid, org_id, org_id , org_id))
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        data_list = [dict(zip(columns, row)) for row in rows]
        print("ORDERRR'S data_list")

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
def assign_order(request):
    connection, cursor = get_sql_anywhere_connection()
    org_id = request.data['org_id']

    try:
        orders = request.data['orders']
        driver = request.data['driver']
        print("here 45454")
        print(orders) 
        print(driver)
        c=0
        for order_no in orders:
            c = c+1
            print("order_noorder_noorder_no")
            print(order_no)
            # cursor.execute(
            #     "SELECT COUNT(*) FROM \"dba\".\"order_driver\" WHERE \"OrderNo\" = ? AND \"Org_ID\" = ?",
            #     [order_no, org_id]
            # )
            # count = cursor.fetchone()[0]

            # if count > 0:
            #     print(f"Order number {order_no} already assigned to a driver.")
            #     cursor.execute(
            #         "UPDATE \"dba\".\"order_driver\" SET \"UserID\" = ? WHERE \"OrderNo\" = ? AND \"Org_ID\" = ?",
            #         [driver, order_no, org_id]
            #     )
            #     connection.commit()
            # else :    
            #  cursor.execute(
            #     "INSERT INTO \"dba\".\"order_driver\" (\"OrderNo\", \"UserID\", \"Org_ID\") VALUES (?, ?, ?)",
            #     [order_no, driver, org_id]
            # )
            #  connection.commit()

            cursor.execute(
                "UPDATE \"dba\".\"Order_HD\" SET \"Status\" = ? , \"DriverID\" = ? WHERE \"OrderNo\" = ? AND \"Org_ID\" = ?",
                ["I", driver, order_no, org_id]
            )
            connection.commit()
        return JsonResponse({"message": "assigned successfully."})

    except Exception as e:
        print(str(e))
        return JsonResponse({"error": f"Failed to assign orders: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()



@api_view(['PUT'])
@permission_classes([AllowAny])
def cancel_order(request):
    connection, cursor = get_sql_anywhere_connection()
    org_id = request.data['org_id']
    order_no = request.data['OrderNo']
    Cancelled_by = request.data['Cancelled_by']
    Cancelled_on = request.data['Cancelled_on']
    CancellationReason = request.data['CancellationReason']

    try:

            
            cursor.execute(
        "UPDATE \"dba\".\"Order_HD\" SET \"Status\" = ?, \"Cancelled_by\" = ?, \"Cancelled_on\" = ?, \"CancellationReason\" = ? WHERE \"OrderNo\" = ? AND \"Org_ID\" = ?",
        ["C", Cancelled_by, Cancelled_on, CancellationReason, order_no, org_id]
    )

            connection.commit()
            return JsonResponse({"message": "cancelled successfully."})

    except Exception as e:
        print(str(e))
        return JsonResponse({"error": f"Failed to assign orders: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()





@api_view(['PUT'])
@permission_classes([AllowAny])
def change_stat(request):
    connection, cursor = get_sql_anywhere_connection()
    org_id = request.data['org_id']

    try:
        orders = request.data['orders']
        stat = request.data['stat']
        if stat is "D":
            d = request.data['date']
        else :
            d = ""

        for order_no in orders:
            print("order_no000")
             
            print(order_no)
            cursor.execute(
                "UPDATE \"dba\".\"Order_HD\" SET \"Status\" = ? , \"Delivered_on\" = ? WHERE \"OrderNo\" = ? AND \"Org_ID\" = ?",
                [stat, d, order_no, org_id]
            )
            connection.commit()
        return JsonResponse({"message": "updated successfully."})

    except Exception as e:
        print(str(e))
        return JsonResponse({"error": f"Failed to assign orders: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()


