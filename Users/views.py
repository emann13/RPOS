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

@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def login(request):
    print("herrrrre")
    connection, cursor = get_sql_anywhere_connection()

    try:
        username = request.data['username']
        passw = request.data['passw']
        print(request.data)
      
        # try:
            # validate_email(username)
        # except ValidationError:
        #     return JsonResponse({"error": "Invalid email address"}, status=400)

        sha256 = hashlib.sha256()
        sha256.update(passw.encode('utf-8'))
        hashed_password = sha256.hexdigest()
        print(hashed_password)

        cursor.execute("SELECT password FROM Admins WHERE username = ?", (username,))
        result = cursor.fetchone()
        print(result)

        if result:
            db_hashed_password = result.password
            print(db_hashed_password)

            if hashed_password == db_hashed_password:
                print("Login successful!")
                cursor.execute("SELECT UID FROM Admins WHERE username = ?", (username,))
                print("cursor")
                # print(cursor.fetchall())
                result = cursor.fetchone()
                print(result)
                
                cursor.execute("SELECT * FROM permissions_admins WHERE UID = ?", (result.UID,))
                result = cursor.fetchall()
                # rows_list = [dict(zip([column[0] for column in cursor.description], row)) for row in result]
                # print(rows_list)
                print(result)
                p={}
                for i in result:
                    print(i[1])
                    p[i[1]] = True
                print(p)
                cursor.execute("SELECT UID FROM Admins WHERE username = ?", (username,))
                result1 = cursor.fetchone()

                cursor.execute("SELECT is_initial FROM Admins WHERE username = ?", (username,))
                result = cursor.fetchone()
                print(result)
                print("resulttt")
                cursor.execute("SELECT status FROM Admins WHERE username = ?", (username,))
                result_status = cursor.fetchone()
                print(result_status)
                print("resulttt")
                cursor.execute("SELECT Org_ID FROM Admins WHERE username = ?", (username,))
                result_org = cursor.fetchone()
                print("gggggg")

                print(result_org)

                print(result[0])
                return JsonResponse({"message": "Logged in successfully!","permissions":p,"initial":result[0], "UID" :result1[0],"Org" : result_org[0], "status":result_status[0]},status=200)
            else:
                print("Invalid password.")
                return JsonResponse({"message": "Invalid password!"}, status=401)

        else:
            print("User not found.")
            return JsonResponse({"message": "User not found!"}, status=404)

    except Exception as e:
        print("errorrr", str(e))
        return JsonResponse({"error": "Failed Successfully!", "details": str(e)}, status=500)



@api_view(['GET'])
@permission_classes([AllowAny])
def fetch_admins(request):
    print("adminss")
    connection, cursor = get_sql_anywhere_connection()
    try:
      query = "SELECT * FROM \"dba\".\"Admins\""
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
def add_admin(request):

    connection, cursor = get_sql_anywhere_connection()
    print(request.data)
    try:
        if  not request.data['username'] or not request.data['email'] :
            print("not f3ln")
            return JsonResponse({"error": "Failed successfully, Please fill all the required fields!"})
        print("not not ")
        p="123"
        sha256 = hashlib.sha256()
        sha256.update(p.encode('utf-8'))
        hashed_password = sha256.hexdigest()
        print(hashed_password)
        permissions = request.data['permissions']
        admin_data = {
            # 'UID': request.data['UID'],
            'username': request.data['username'],
            'email': request.data['email'],
            'first_name': request.data['f_name'],
            'last_name': request.data['l_name'],
            'status': request.data['storeStat'],
            'password': hashed_password,
            
        }
        query = f"""
            INSERT INTO "dba"."Admins" ({', '.join(admin_data.keys())})
            VALUES ({', '.join(['?' for _ in admin_data.values()])})
        """
        cursor.execute(query, list(admin_data.values()))
        connection.commit()
        cursor.execute("SELECT @@IDENTITY AS U_ID")
        print("result")

        result = cursor.fetchone()
        print(result)
        uID = result.U_ID if result else None
        
        print(uID)

        for i in permissions:
            print(i)
            cursor.execute(f"INSERT INTO \"dba\".\"permissions_admins\" (PID , UID) VALUES (? , ?)", [i , uID])
            connection.commit()  

        print("Data inserted successfully.")
        return JsonResponse({"message": "Added successfully!"}, status=200)

    except pyodbc.Error as e:
        print("failed")
        error_message = str(e)
        print(f"Error inserting data: {error_message}")
        return JsonResponse({"error": f"Failed to insert data: {error_message}"}, status=500)

    finally:
        cursor.close()
        connection.close()


@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_admin(request):

    if not request.data['UID'] or not request.data['username'] or not request.data['email'] :
            print("not f3ln")
            return JsonResponse({"error": "Failed successfully, Please fill all the required fields!"})
      
    connection, cursor = get_sql_anywhere_connection()
    try:
        admin_id = request.data['UID']
        print(admin_id)
        print(request.data)
        query_fetch = f"SELECT * FROM \"dba\".\"Admins\" WHERE \"UID\" = ?"
        cursor.execute(query_fetch, [admin_id])
        # print(cursor.fetchone())
        existing_data = cursor.fetchone()

        # print(cursor.fetchone())
        # if not existing_data :
        #    print("nottt")
        if existing_data :
            print("ystahel el daga dii f3lannnn")

            admin_data = {
            'UID': request.data['UID'],
            'username': request.data['username'],
            'email': request.data['email'],
            'first_name': request.data['f_name'],
            'last_name': request.data['l_name'],
            'status': request.data['storeStat'],
            }
            # print(admin_data)
            permissions = request.data['permissions']

            print(permissions)
            update_columns = ', '.join([f'"{col}" = ?' for col in admin_data.keys()])
            query_update = f"UPDATE \"dba\".\"Admins\" SET {update_columns} WHERE \"UID\" = ?"
            cursor.execute(query_update, list(admin_data.values()) + [admin_id])
            connection.commit()
            # for i in permissions :
            query = "SELECT * FROM \"dba\".\"permissions_admins\" WHERE UID = ? "
            cursor.execute(query, (request.data['UID']))
            result = cursor.fetchall()
            print(result)
            if result:
                c=0
                # print( result[1][1])
                for i in result:
                    print("herererer")
                    print(i[1])
                    query = "DELETE FROM \"dba\".\"permissions_admins\" WHERE UID = ? AND PID = ?"
                    cursor.execute(query, (request.data['UID'] , i[1]))
                    connection.commit()
                    print("deleted", i)
                    # c=c+1
                    # continue
                # else :
                #    cursor.execute(f"INSERT INTO \"dba\".\"permissions_admins\" (PID , UID) VALUES (? , ?)", [i , request.data['UID']])
                #    connection.commit()  
            for i in permissions :
                # query = "SELECT * FROM \"dba\".\"permissions_admins\" WHERE UID = ? AND PID = ?"
                # cursor.execute(query, (request.data['UID'] , i))
                # result = cursor.fetchone()
                # print(result)
                # if result:
                #     query = "DELETE FROM \"dba\".\"permissions_admins\" WHERE UID = ? AND PID = ?"
                #     cursor.execute(query, (request.data['UID'] , i))
                #     print("deleted", i)
                #     continue
                # else :
                   cursor.execute(f"INSERT INTO \"dba\".\"permissions_admins\" (PID , UID) VALUES (? , ?)", [i , request.data['UID']])
                   connection.commit()  

            return JsonResponse({"message": "Admin updated successfully!"}, status=200)
        else:
            return JsonResponse({"error": f"Admin with ID {admin_id} not found."}, status=404)

    except Exception as e:
        return JsonResponse({"error": f"Failed to update admin: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()



@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_admin(request):
    try:
        connection, cursor = get_sql_anywhere_connection()
        User_id = request.data['User']
        print(User_id)
        query = "SELECT * FROM \"dba\".\"permissions_admins\" WHERE UID = ? "
        cursor.execute(query, (User_id))
        result = cursor.fetchall()
        print(result)
        if result:
            # print( result[1][1])
            for i in result:
                    print("herererer")
                    print(i[1])
                    query = "DELETE FROM \"dba\".\"permissions_admins\" WHERE UID = ? AND PID = ?"
                    cursor.execute(query, (User_id , i[1]))
                    print("deleted", i)
        cursor.execute(f"DELETE FROM \"dba\".\"Admins\" WHERE \"UID\" = ?", [User_id])
        connection.commit()  

        return JsonResponse({"message": "Admin deleted successfully."})
    except pyodbc.Error as e:
        return JsonResponse({"error": f"Failed to delete Admin: {str(e)}"}, status=500)
    finally:
        cursor.close()
        connection.close()




@api_view(['PUT'])
@permission_classes([AllowAny])
def reset_pass_admin(request):

    connection, cursor = get_sql_anywhere_connection()
    print(request.data)
    try:
        if not request.data['pass'] :
            print("not f3ln")
            return JsonResponse({"error": "Failed successfully, Please fill all the required fields!"})
        print("not not ")
        p=  request.data['pass']
        sha256 = hashlib.sha256()
        sha256.update(p.encode('utf-8'))
        hashed_password = sha256.hexdigest()
        print(hashed_password)
        username = request.data['username']
        cursor.execute(f"UPDATE \"dba\".\"Admins\" SET \"password\" = ? WHERE \"username\" = ?", [hashed_password , username])
        connection.commit()
        cursor.execute(f"UPDATE \"dba\".\"Admins\" SET \"is_initial\" = ? WHERE \"username\" = ?", [0 , username])
        connection.commit()

        print("Data inserted successfully.")
        return JsonResponse({"message": "Added successfully!"}, status=200)

    except pyodbc.Error as e:
        print("failed")
        error_message = str(e)
        print(f"Error inserting data: {error_message}")
        return JsonResponse({"error": f"Failed to insert data: {error_message}"}, status=500)

    finally:
        cursor.close()
        connection.close()





@api_view(['GET'])
@permission_classes([AllowAny])
def fetch_permissions(request):
    print("permissionnss")
    connection, cursor = get_sql_anywhere_connection()
    try:
      query = "SELECT * FROM \"dba\".\"Permissions\""
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
def fetch_Roles(request):
    print("Roless")
    connection, cursor = get_sql_anywhere_connection()
    try:
      query = "SELECT * FROM \"dba\".\"USR_Role\""
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
def fetch_Auths(request):
    print("Auth")
    connection, cursor = get_sql_anywhere_connection()
    try:
      query = "SELECT * FROM \"dba\".\"USR_Auth\""
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
def add_role(request):

    connection, cursor = get_sql_anywhere_connection()
    print(request.data)
    try:
        # if not request.data['UID'] or not request.data['username'] or not request.data['email'] :
        #     print("not f3ln")
        #     return JsonResponse({"error": "Failed successfully, Please fill all the required fields!"})
        print("not not ")
        auths = request.data['auths']
        data = {
            'Role_Text': request.data['name'],
            'Role_Desc': request.data['desc'],
            'Cash_reg_req': request.data['cash'],
            
        }
        query = f"""
            INSERT INTO "dba"."USR_Role" ({', '.join(data.keys())})
            VALUES ({', '.join(['?' for _ in data.values()])})
        """
        cursor.execute(query, list(data.values()))
        connection.commit()
        print("before")

        cursor.execute("SELECT @@IDENTITY AS Role_ID")
        print("result")

        result = cursor.fetchone()
        print(result)
        role_id = result.Role_ID if result else None
        # print("harry pottaaa")
        print(role_id)


        for i in auths:
            print(i)
            # print(cursor.lastrowid)
            cursor.execute(f"INSERT INTO \"dba\".\"USR_Role_Auth\" (Auth_ID , Role_ID) VALUES (? , ?)", [i , role_id])
            connection.commit()  

        print("Data inserted successfully.")
        return JsonResponse({"message": "Added successfully!"}, status=200)

    except pyodbc.Error as e:
        print("failed")
        error_message = str(e)
        print(f"Error inserting data: {error_message}")
        return JsonResponse({"error": f"Failed to insert data: {error_message}"}, status=500)

    finally:
        cursor.close()
        connection.close()




@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_role(request):

    # if not request.data['UID'] or not request.data['username'] or not request.data['email'] :
    #         print("not f3ln")
    #         return JsonResponse({"error": "Failed successfully, Please fill all the required fields!"})
      
    connection, cursor = get_sql_anywhere_connection()
    try:
        rid = request.data['RID']
        print(rid)
        print(request.data)
        query_fetch = f"SELECT * FROM \"dba\".\"USR_Role\" WHERE \"Role_ID\" = ?"
        cursor.execute(query_fetch, [rid])
        # print(cursor.fetchone())
        existing_data = cursor.fetchone()

        # print(cursor.fetchone())
        # if not existing_data :
        #    print("nottt")
        if existing_data :
            print("ystahel el daga dii f3lannnn")

            auths = request.data['auths']
            data = {
            'Role_Text': request.data['name'],
            'Role_Desc': request.data['desc'],
            'Cash_reg_req': request.data['cash'],
            
        }            

            update_columns = ', '.join([f'"{col}" = ?' for col in data.keys()])
            query_update = f"UPDATE \"dba\".\"USR_Role\" SET {update_columns} WHERE \"Role_ID\" = ?"
            cursor.execute(query_update, list(data.values()) + [rid])
            connection.commit()

            query = "SELECT * FROM \"dba\".\"USR_Role_Auth\" WHERE Role_ID = ? "
            cursor.execute(query, (request.data['RID']))
            result = cursor.fetchall()
            print(result)
            if result:
                c=0
                # print( result[1][1])
                for i in result:
                    print("herererer")
                    print(i[1])
                    query = "DELETE FROM \"dba\".\"USR_Role_Auth\" WHERE Role_ID = ? AND Auth_ID = ?"
                    cursor.execute(query, (request.data['RID'] , i[1]))
                    connection.commit()
                    print("deleted", i)
            for i in auths :
                   cursor.execute(f"INSERT INTO \"dba\".\"USR_Role_Auth\" (Role_ID , Auth_ID) VALUES (? , ?)", [request.data['RID'],i])
                   connection.commit()  

            return JsonResponse({"message": "Role updated successfully!"}, status=200)
        else:
            return JsonResponse({"error": f"Role with ID {admin_id} not found."}, status=404)

    except Exception as e:
        return JsonResponse({"error": f"Failed to update Role: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()



@api_view(['GET'])
@permission_classes([AllowAny])
def fetch_R_Auths(request):
    print("Auth")
    connection, cursor = get_sql_anywhere_connection()
    try:
      query = "SELECT * FROM \"dba\".\"USR_Role_Auth\""
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




@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_role(request):
    try:
        connection, cursor = get_sql_anywhere_connection()
        Rid = request.data['Role']
        print(Rid)
        cursor.execute(f"DELETE FROM \"dba\".\"USR_Role\" WHERE \"Role_ID\" = ?", [Rid])
        
        connection.commit()  

        return JsonResponse({"message": "Role deleted successfully."})
    except Exception as e:
        return JsonResponse({"error": f"Failed to delete Role: {str(e)}"}, status=500)
    finally:
        cursor.close()
        connection.close()

@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def get_ecs_admin(request):
    p = "pass@1234"
    sha256 = hashlib.sha256()
    sha256.update(p.encode('utf-8'))
    hashed_password = sha256.hexdigest()
    print(hashed_password)
    passw = request.data['passw']
    sha256 = hashlib.sha256()
    sha256.update(passw.encode('utf-8'))
    hashed_password2 = sha256.hexdigest()
    if hashed_password2 == hashed_password:

     return JsonResponse({"message":"Access Allowed!"}, status=200)
    return JsonResponse({"error":"Access denied!"}, status=401)
 
@api_view(['GET'])
@permission_classes([AllowAny])
def fetch_users_p (request):
    print("permissions_admins")
    connection, cursor = get_sql_anywhere_connection()
    try:
      query = "SELECT * FROM \"dba\".\"permissions_admins\""
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


#------------------------------- USERS Functions ---------------------------------


@permission_classes([AllowAny])
def add_user(request):

    connection, cursor = get_sql_anywhere_connection()
    print(request.data)
    try:
        if not request.data['UserName'] or not request.data['Role_ID']  :
            print("not f3ln")
            return JsonResponse({"error": "Failed successfully, Please fill all the required fields!"})
        print("not not ")
        p = "123"
        # sha256 = hashlib.sha256()
        # sha256.update(p.encode('utf-8'))
        # hashed_password = sha256.hexdigest()
        # print(hashed_password)
        # permissions = request.data['permissions']
        data = {
            # 'UID': request.data['UID'],
            'UserName': request.data['UserName'],
            'UserEmail': request.data['UserEmail'],
            'FullName': request.data['FullName'],
            'EncryptedPassword': p,
            'Locked': request.data['Locked'],
            'Role_ID' : request.data['Role_ID'],
            'UserActive' : 0,
            'IsInitial' : 1,
            'Store_ID' : request.data['Store_ID'],


        }
        print("plzz workkkk", data)

        query = f"""
            INSERT INTO "dba"."Users" ({', '.join(data.keys())})
            VALUES ({', '.join(['?' for _ in data.values()])})
        """
        cursor.execute(query, list(data.values()))
        connection.commit()

        print("Data inserted successfully.")
        return JsonResponse({"message": "Added successfully!"}, status=200)

    except pyodbc.Error as e:
        print("failed")
        error_message = str(e)
        print(f"Error inserting data: {error_message}")
        return JsonResponse({"error": f"Failed to insert data: {error_message}"}, status=500)

    finally:
        cursor.close()
        connection.close()



@api_view(['GET'])
@permission_classes([AllowAny])
def fetch_users(request):
    print("adminss")
    connection, cursor = get_sql_anywhere_connection()
    try:
      query = "SELECT * FROM \"dba\".\"Users\""
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
def edit_user(request):

    if not request.data['UserName'] or not request.data['Role_ID']  :        
            print("not f3ln")
            return JsonResponse({"error": "Failed successfully, Please fill all the required fields!"})
      
    connection, cursor = get_sql_anywhere_connection()
    try:
         uid = request.data['UID']
         print(uid)
         print(request.data)
         query_fetch = f"SELECT * FROM \"dba\".\"Users\" WHERE \"UserID\" = ?"
         cursor.execute(query_fetch, [uid])
         # print(cursor.fetchone())
         existing_data = cursor.fetchone()

        # print(cursor.fetchone())
        # if not existing_data :
        #    print("nottt")
         if existing_data :
          print("ystahel el daga dii f3lannnn")
          if  request.data['pass']  != '' :
            # if 'pass' in request.data:
             print("db")
             data = {
            # 'UID': request.data['UID'],
            'UserName': request.data['UserName'],
            'UserEmail': request.data['UserEmail'],
            'FullName': request.data['FullName'],
            'Locked': request.data['Locked'],
            'Role_ID' : request.data['Role_ID'],
            'Store_ID' : request.data['Store_ID'],
            'IsInitial' : 1,
            'EncryptedPassword' : request.data['pass']

        }
          else :
             print("or not db")
             p ="123"
             data = {
            # 'UID': request.data['UID'],
            'UserName': request.data['UserName'],
            'UserEmail': request.data['UserEmail'],
            'FullName': request.data['FullName'],
            'Locked': request.data['Locked'],
            'Role_ID' : request.data['Role_ID'],
            'Store_ID' : request.data['Store_ID'],



        }
            # print(admin_data)
            # permissions = request.data['permissions']

          print(data)
          update_columns = ', '.join([f'"{col}" = ?' for col in data.keys()])
          query_update = f"UPDATE \"dba\".\"Users\" SET {update_columns} WHERE \"UserID\" = ?"
          cursor.execute(query_update, list(data.values()) + [uid])
          connection.commit()
            # for i in permissions :

          return JsonResponse({"message": "User updated successfully!"}, status=200)
         else:
            return JsonResponse({"error": f"User with ID {uid} not found."}, status=404)

    except Exception as e:
        print (str(e))
        return JsonResponse({"error": f"User to update admin: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()



@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_user(request):
    try:
        connection, cursor = get_sql_anywhere_connection()
        uid = request.data['uid']
        print(uid)
        cursor.execute(f"DELETE FROM \"dba\".\"Users\" WHERE \"UserID\" = ?", [uid])
        
        connection.commit()  

        return JsonResponse({"message": "User deleted successfully."})
    except Exception as e:
        return JsonResponse({"error": f"Failed to delete User: {str(e)}"}, status=500)
    finally:
        cursor.close()
        connection.close()


from django.db import connection

@api_view(['GET'])
@permission_classes([AllowAny])
def count_active_users(request):
    print("tybbbb here??")
    connection, cursor = get_sql_anywhere_connection()
    print("tyb here??")
    try:

        cursor.execute("SELECT COUNT(*) FROM Users WHERE UserActive = 1")
        print("did we pass??")
        row = cursor.fetchone()
        print(row)
        active_user_count = row[0] if row else 0
        cursor.execute("SELECT COUNT(*) FROM Stores WHERE Status = 1")
        print("did we pass??")
        row = cursor.fetchone()
        print(row)
        active_store_count = row[0] if row else 0

        return JsonResponse({"message": "Users count fetched successfully.","users_count":active_user_count,"stores_count":active_store_count})

    except Exception as e:
        print(str(e))
    # return active_user_count
        return JsonResponse({"error": f"Failed to fetch User count: {str(e)}"}, status=500)
    finally:
        cursor.close()
        connection.close()



@api_view(['GET'])
@permission_classes([AllowAny])
def get_License(request):
    print("tybbbb here??")
    connection, cursor = get_sql_anywhere_connection()
    print("tyb here??")
    try:
        query = "SELECT * FROM \"dba\".\"License\""

        cursor.execute(query)
        print("did we pass??")
        rows = cursor.fetchall()
        print(rows)
        rows_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

        return JsonResponse({"message": " License Fetched successfully!", "data": rows_list})


    except Exception as e:
        print(f"Error fetching data: {e}")
        return JsonResponse({"error": "Failed successfully!", "message": str(e)})

    finally:
        cursor.close()
        connection.close()

@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_license(request):

    if not request.data['key'] or not request.data['type']:
      return JsonResponse({"error": "Failed successfully, Please fill all the required fields!"})
      
    connection, cursor = get_sql_anywhere_connection()
    try:
        l_type = request.data['type']

        query_fetch = f"SELECT * FROM \"dba\".\"license\" WHERE \"Type\" = ?"
        cursor.execute(query_fetch, [l_type])
        existing_data = cursor.fetchone()
        print(request.data)
        if existing_data:
            store_data = {
                'Key': request.data['key'],
                'Type': request.data['type'],
            }

            update_columns = ', '.join([f'"{col}" = ?' for col in store_data.keys()])
            query_update = f"UPDATE \"dba\".\"License\" SET {update_columns} WHERE \"Type\" = ?"

            cursor.execute(query_update, list(store_data.values()) + [l_type])
            connection.commit()

            return JsonResponse({"message": "License updated successfully!"}, status=200)
        else:
            return JsonResponse({"error": f"License with Type {l_type} not found."}, status=404)

    except Exception as e:
        return JsonResponse({"error": f"Failed to update License: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()

