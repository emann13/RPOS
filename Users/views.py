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
                print("Login successfull!")
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
                print(request.data['lng'])
                if request.data['lng'] == "AR" :
                  print("Invalid password.")
                  return JsonResponse({"message": "! كلمة المرور غير صحيحة"}, status=401)

                else:
                   print("Invalid password.")
                   return JsonResponse({"message": "Invalid password!"}, status=401)
                

        else:
            print(request.data['lng'])
            if request.data['lng'] == "AR" :
              print("User not found.")
              return JsonResponse({"message": "! المستخدم غير موجود"}, status=404)
            else :  
              print("User not found.")
              return JsonResponse({"message": "User not found!"}, status=404)

    except Exception as e:
        print("errorrr", str(e))
        return JsonResponse({"error": "Failed !", "details": str(e)}, status=500)



@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def fetch_admins(request):
    print("adminss")
    connection, cursor = get_sql_anywhere_connection()
    try:
      query = "SELECT * FROM \"dba\".\"Admins\" WHERE \"Org_ID\" = ? "
      org_Id = request.data["org_id"]
      cursor.execute(query, [org_Id])  
      rows = cursor.fetchall()
      rows_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
      print("rows_list 999")

      print(rows_list)
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
            return JsonResponse({"error": "Failed, Please fill all the required fields!"})
        print("not not ")
        p = "123"
        e = request.data['email']
        org_id = request.data['org_id']
        user = request.data['username']
        cursor.execute(f"SELECT * FROM \"dba\".\"Admins\" WHERE \"email\" = ?  OR \"username\" = ? ", [e ,user])
        connection.commit()  
        result = cursor.fetchone()
        print(result)
        if result :
            print("here")
            return JsonResponse({"error": f"Failed to insert data" , "email" : 1}, status=200)

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
            'Org_ID' : request.data['org_id']
            
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
            print("i is here ")

            print(i)
            cursor.execute(f"INSERT INTO \"dba\".\"permissions_admins\" (PID , UID, Org_ID) VALUES (? , ?, ?)", [i , uID, org_id])
            connection.commit()  

        print("Data inserted successfully.")
        return JsonResponse({"message": "Added successfully!"}, status=200)

    except Exception as e:
        print("failed")
        print(str(e))
        return JsonResponse({"error": f"Failed to insert data: "}, status=500)

    finally:
        cursor.close()
        connection.close()


@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_admin(request):

    if not request.data['UID'] or not request.data['username'] or not request.data['email'] :
            print("not f3ln")
            return JsonResponse({"error": "Failed, Please fill all the required fields!"})
      
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
            # 'Org_ID' : request.data['org_id']

            }
            # print(admin_data)
            permissions = request.data['permissions']
            org_Id = request.data['org_id']
            print(permissions)
            update_columns = ', '.join([f'"{col}" = ?' for col in admin_data.keys()])
            query_update = f"UPDATE \"dba\".\"Admins\" SET {update_columns} WHERE \"UID\" = ? AND \"Org_ID\" = ?"
            cursor.execute(query_update, list(admin_data.values()) + [admin_id , org_Id])
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
                    query = "DELETE FROM \"dba\".\"permissions_admins\" WHERE UID = ? AND PID = ? AND Org_ID = ?"
                    cursor.execute(query, (request.data['UID'] , i[1], org_Id))
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
                   cursor.execute(f"INSERT INTO \"dba\".\"permissions_admins\" (PID , UID, Org_ID) VALUES ( ?, ?, ?)", [i , request.data['UID'], org_Id])
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





@api_view(['PUT'])
@permission_classes([AllowAny])
def fetch_permissions(request):
    print("permissionnss")
    connection, cursor = get_sql_anywhere_connection()
    try:
      org_id = request.data['org_id']
      query = "SELECT * FROM \"dba\".\"Permissions\" WHERE \"Org_ID\" = ?"
      cursor.execute(query , [org_id])  
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
def fetch_Roles(request):
    print("Roless")
    connection, cursor = get_sql_anywhere_connection()
    try:
      org_Id = request.data["org_id"]
      print("org iddd")
      print(org_Id)
      query = "SELECT * FROM \"dba\".\"USR_Role\" WHERE \"Org_ID\" = ?"
      cursor.execute(query,[org_Id])  
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
def fetch_Auths(request):
    print("Auth 12")
    connection, cursor = get_sql_anywhere_connection()
    try:

      org_Id = request.data["org_id"]
      query = "SELECT * FROM \"dba\".\"USR_Auth\" WHERE \"Org_ID\" = ?"
      cursor.execute(query , [org_Id])
      print("auths for auths")
      rows = cursor.fetchall()
      print(rows)  

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
        org_Id = request.data["org_id"]

        auths = request.data['auths']
        data = {
            'Role_Text': request.data['name'],
            'Role_Desc': request.data['desc'],
            'Cash_reg_req': request.data['cash'],
            'Org_ID' : org_Id,
            
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
            cursor.execute(f"INSERT INTO \"dba\".\"USR_Role_Auth\" (Auth_ID , Role_ID, Org_ID) VALUES (? , ?, ?)", [i , role_id , org_Id])
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
            org_Id = request.data["org_id"]

            auths = request.data['auths']
            data = {
            'Role_Text': request.data['name'],
            'Role_Desc': request.data['desc'],
            'Cash_reg_req': request.data['cash'],
            'Org_ID' : org_Id,

            
        }            

            update_columns = ', '.join([f'"{col}" = ?' for col in data.keys()])
            query_update = f"UPDATE \"dba\".\"USR_Role\" SET {update_columns} WHERE \"Role_ID\" = ? AND \"Org_ID\" = ?"
            cursor.execute(query_update, list(data.values()) + [rid , org_Id])
            connection.commit()

            query = "SELECT * FROM \"dba\".\"USR_Role_Auth\" WHERE Role_ID = ? AND \"Org_ID\" = ?"
            cursor.execute(query, (request.data['RID'] , org_Id))
            result = cursor.fetchall()
            print(result)
            if result:
                c=0
                # print( result[1][1])
                for i in result:
                    print("herererer")
                    print(i[1])
                    query = "DELETE FROM \"dba\".\"USR_Role_Auth\" WHERE Role_ID = ? AND Auth_ID = ? AND \"Org_ID\" = ?"
                    cursor.execute(query, (request.data['RID'] , i[1] , org_Id))
                    connection.commit()
                    print("deleted", i)
            for i in auths :
                   cursor.execute(f"INSERT INTO \"dba\".\"USR_Role_Auth\" (Role_ID , Auth_ID , Org_ID) VALUES (? , ?  , ?)", [request.data['RID'],i,org_Id])
                   connection.commit()  

            return JsonResponse({"message": "Role updated successfully!"}, status=200)
        else:
            return JsonResponse({"error": f"Role with ID {admin_id} not found."}, status=404)

    except Exception as e:
        return JsonResponse({"error": f"Failed to update Role: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()



@api_view(['PUT'])
@permission_classes([AllowAny])
def fetch_R_Auths(request):
    print("Auth")
    connection, cursor = get_sql_anywhere_connection()
    try:
      org_Id = request.data["org_id"]

      query = "SELECT * FROM \"dba\".\"USR_Role_Auth\" WHERE \"Org_ID\" = ?"
      cursor.execute(query, [org_Id])  
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
def fetch_a_role_Auths(request):
    print("Auth")
    connection, cursor = get_sql_anywhere_connection()
    try:
      uid = request.data['uid']  
      org_Id = request.data["org_id"]

      query = "SELECT * FROM \"dba\".\"USR_Role_Auth\" WHERE \"Role_ID\" = ? AND \"Org_ID\" = ?"
      cursor.execute(query,[uid , org_Id])  
      rows = cursor.fetchall()
      print("role roles rolat")
      print(rows)
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
def fetch_an_admin_Auths(request):
    print("Auth")
    connection, cursor = get_sql_anywhere_connection()
    try:
      uid = request.data['uid']  
      org_id = request.data['org_id']

      query = "SELECT * FROM \"dba\".\"permissions_admins\" WHERE \"UID\" = ? AND \"Org_ID\" = ?"
      cursor.execute(query,[uid , org_id])  
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
        org_id = request.data['org_id']

        cursor.execute(f"DELETE FROM \"dba\".\"USR_Role\" WHERE \"Role_ID\" = ? AND \"Org_ID\" = ?", [Rid, org_id])
        
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
 
@api_view(['PUT'])
@permission_classes([AllowAny])
def fetch_users_p (request):
    print("permissions_admins")
    connection, cursor = get_sql_anywhere_connection()
    try:
      org_id = request.data['org_id']
      query = "SELECT * FROM \"dba\".\"permissions_admins\" WHERE \"Org_ID\" = ? "
      cursor.execute(query, [org_id])
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

@api_view(['PUT'])
@permission_classes([AllowAny])
def add_user(request):

    connection, cursor = get_sql_anywhere_connection()
    print(request.data)
    try:
        org_id = request.data['org_id']
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
            'UserActive': request.data['Locked'],
            'Role_ID' : request.data['Role_ID'],
            'Locked' : 0,
            'IsInitial' : 1,
            'Store_ID' : request.data['Store_ID'],
            'Org_ID' : org_id


        }
        print("plzz workkkk", data)

        query = f"""
            INSERT INTO "dba"."USR_User" ({', '.join(data.keys())})
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



@api_view(['PUT'])
@permission_classes([AllowAny])
def fetch_users(request):
    print("adminss")
    connection, cursor = get_sql_anywhere_connection()
    try:
      org_id = request.data['org_id']
      print("ty")
      print(org_id)
      query = "SELECT * FROM \"dba\".\"USR_User\" WHERE \"Org_ID\" = ?"
      cursor.execute(query, [org_id])  
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
    org_Id = request.data["org_id"]
 
    connection, cursor = get_sql_anywhere_connection()
    try:
         uid = request.data['UID']
         print(uid)
         print(request.data)
         query_fetch = f"SELECT * FROM \"dba\".\"USR_User\" WHERE \"UserID\" = ?"
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
            'UserActive': request.data['UserActive'],
            'Role_ID' : request.data['Role_ID'],
            'Store_ID' : request.data['Store_ID'],
            'IsInitial' : 1,
            'EncryptedPassword' : request.data['pass'],

        }
          else :
             print("or not db")
            #  p ="123"
             data = {
            # 'UID': request.data['UID'],
            'UserName': request.data['UserName'],
            'UserEmail': request.data['UserEmail'],
            'FullName': request.data['FullName'],
            'UserActive': request.data['UserActive'],
            'Role_ID' : request.data['Role_ID'],
            'Store_ID' : request.data['Store_ID'],



        }
            # print(admin_data)
            # permissions = request.data['permissions']

          print(data)
          update_columns = ', '.join([f'"{col}" = ?' for col in data.keys()])
          query_update = f"UPDATE \"dba\".\"USR_User\" SET {update_columns} WHERE \"UserID\" = ? "
        #   print(query_update)
        #   print("query_update")

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
        org_id = request.data['org_id']
        print("here delete this")
        print(uid , org_id)

        cursor.execute(f"DELETE FROM \"dba\".\"USR_User\" WHERE \"UserID\" = ?  AND \"Org_ID\" = ?", [uid ,  org_id])
        
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

        cursor.execute("SELECT COUNT(*) FROM USR_User WHERE UserActive = 1")
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




@api_view(['PUT'])
@permission_classes([AllowAny])
def fetch_drivers(request):
    print("drivers")
    connection, cursor = get_sql_anywhere_connection()
    try:
      org_id = request.data['org_id']

      query = "SELECT * FROM \"dba\".\"Drivers\"  WHERE \"Org_ID\" = ?"
      cursor.execute(query,[org_id])  
      rows = cursor.fetchall()
      rows_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

      return JsonResponse({"message": "Fetched successfully!", "data": rows_list})


    except Exception as e:
        print(f"Error fetching data: {e}")
        return JsonResponse({"error": "Failed successfully!", "message": str(e)})

    finally:
        cursor.close()
        connection.close()

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['PUT'])
@permission_classes([AllowAny])
def add_driver(request):
    connection, cursor = get_sql_anywhere_connection()

    try:
        org_id = request.data['org_id']
        if not request.data['UserName']:
            return JsonResponse({"error": "Failed successfully, Please fill all the required fields!"})

        cursor.execute('SELECT COUNT(*) FROM "dba"."Drivers" WHERE "UserEmail" = ?', [request.data['UserEmail']])
        if cursor.fetchone()[0] > 0:
            return JsonResponse({"error": "Email is already in use!"}, status = 409)

        cursor.execute('SELECT COUNT(*) FROM "dba"."Drivers" WHERE "UserName" = ?', [request.data['UserName']])
        if cursor.fetchone()[0] > 0:
            return JsonResponse({"error": "Username is already in use!"}, status = 409)

        cursor.execute('SELECT COUNT(*) FROM "dba"."Drivers" WHERE "PhoneNo" = ?', [request.data['PhoneNo']])
        if cursor.fetchone()[0] > 0:
            return JsonResponse({"error": "Phone number is already in use!"}, status = 409)

        cursor.execute('SELECT COUNT(*) FROM "dba"."Drivers" WHERE "National_ID" = ?', [request.data['nat']])
        if cursor.fetchone()[0] > 0:
            return JsonResponse({"error": "National ID is already in use!"}, status = 409 )


        # cursor.execute('SELECT COUNT(*) FROM "dba"."Drivers" WHERE "Vehicle_no" = ?', [request.data['Vehicle_no']])
        # if cursor.fetchone()[0] > 0:
        #     return JsonResponse({"error": "Vehicle number is already in use!"}, status = 409 )

        p = "123"
        data = {
            'UserName': request.data['UserName'],
            'UserEmail': request.data['UserEmail'],
            'FullName': request.data['FullName'],
            'National_ID' : request.data['nat'],
            'EncryptedPassword': p,
            'Password': p,
            'UserActive': request.data['Locked'],
            'PhoneNo' : request.data['PhoneNo'],
            'Locked' : 0,
            'IsInitial' : 1,
            'Vehicle_no' : request.data['Vehicle_no'],
            'Org_ID' : org_id
        }
        query = f"""
            INSERT INTO "dba"."Drivers" ({', '.join(data.keys())})
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




@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_driver(request):

    if not request.data['UserName'] :        
            print("not f3ln")
            return JsonResponse({"error": "Failed successfully, Please fill all the required fields!"})
    org_Id = request.data["org_id"]
    print("drivers ssss")
    connection, cursor = get_sql_anywhere_connection()
    try:
         uid = request.data['UID']
         print(uid)
         print(request.data)
         query_fetch = f"SELECT * FROM \"dba\".\"Drivers\" WHERE \"DriverID\" = ? AND \"Org_ID\" =?"
         cursor.execute(query_fetch, [uid , org_Id])
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
            'UserActive': request.data['UserActive'],
            'PhoneNo' : request.data['PhoneNo'],
            'Vehicle_no' : request.data['Vehicle_no'],
            'Org_ID' : org_Id,           
            'National_ID' : request.data['nat'],
            'IsInitial' : 1,
            # 'EncryptedPassword' : request.data['pass'],
            'Password' : request.data['pass'],

        }
          else :
             print("or not db")
            #  p ="123"
             data = {
            # 'UID': request.data['UID'],
            'UserName': request.data['UserName'],
            'UserEmail': request.data['UserEmail'],
            'FullName': request.data['FullName'],
            'UserActive': request.data['UserActive'],
            'National_ID' : request.data['nat'],

            'PhoneNo' : request.data['PhoneNo'],
            'Vehicle_no' : request.data['Vehicle_no'],
            'Org_ID' : org_Id,            



        }
            # print(admin_data)
            # permissions = request.data['permissions']

          print(data)
          update_columns = ', '.join([f'"{col}" = ?' for col in data.keys()])
          query_update = f"UPDATE \"dba\".\"Drivers\" SET {update_columns} WHERE \"DriverID\" = ? AND Org_ID =? "
        #   print(query_update)
        #   print("query_update")

          cursor.execute(query_update, list(data.values()) + [uid , org_Id])
          connection.commit()
            # for i in permissions :
          
          return JsonResponse({"message": "Driver updated successfully!"}, status=200)
         else:
            return JsonResponse({"error": f"Driver with ID {uid} not found."}, status=404)

    except Exception as e:
        print (str(e))
        return JsonResponse({"error": f"User to update Driver: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_driver(request):
    try:
        connection, cursor = get_sql_anywhere_connection()
        uid = request.data['uid']
        print(uid)
        org_Id = request.data["org_id"]

        cursor.execute(f"DELETE FROM \"dba\".\"Drivers\" WHERE \"DriverID\" = ? AND \"Org_ID\" = ?", [uid ,  org_Id])
        
        connection.commit()  

        return JsonResponse({"message": "Driver deleted successfully."})
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": f"Failed to delete Driver: {str(e)}"}, status=500)
    finally:
        cursor.close()
        connection.close()






@api_view(['PUT'])
@permission_classes([AllowAny])
def fetch_customers(request):
    print("customers")
    connection, cursor = get_sql_anywhere_connection()
    try:
        org_id = request.data["org_id"]

        query = """
            SELECT U.*, (
                SELECT TOP 1 Address
                FROM "dba"."Users_Address" AS UA
                WHERE UA.UserID = U.UserID AND Org_ID = ?
                ORDER BY UA.AddID
            ) AS First_Address
            FROM "dba"."Users_HD" AS U
            WHERE U."Org_ID" = ?
        """

        cursor.execute(query, [org_id, org_id])
        rows = cursor.fetchall()
        rows_list = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

        print("rows_list 999")
        print(rows_list)
        return JsonResponse({"message": "Fetched successfully!", "data": rows_list})

    except Exception as e:
        print(f"Error fetching data: {e}")
        return JsonResponse({"error": "Failed !", "message": str(e)})

    finally:
        cursor.close()
        connection.close()


from django.http import HttpResponse
import pandas as pd
import io

@api_view(['PUT'])
@permission_classes([AllowAny])
def export_users_to_excel(request):
    print("customers")
    connection, cursor = get_sql_anywhere_connection()
    try:
        query = """
            SELECT U.FullName, U.PhoneNo, U.HomeNo, U.Email, UA.Address,
            UA.StreetName, UA.State, UA.Remark, UA.FloorNo, UA.BuildingNo, UA.ApartmentNo
            FROM "dba"."Users_HD" AS U
            LEFT JOIN "dba"."Users_Address" AS UA ON U.UserID = UA.UserID
            WHERE U."Org_ID" = ? AND UA."Org_ID" = ?
        """
        org_Id = request.data["org_id"]
        cursor.execute(query, [org_Id, org_Id])  
        rows = cursor.fetchall()
        
        # Replace invalid characters with None (null) values
        def replace_invalid_chars(cell):
            if isinstance(cell, str) and '\u001a' in cell:
                return None
            return cell
        
        rows_list = [dict(zip([column[0] for column in cursor.description], [replace_invalid_chars(cell) for cell in row])) for row in rows]
        print("rows_list 999")
        data = rows_list

        df = pd.DataFrame(list(data))

        excel_buffer = io.BytesIO()

        df.to_excel(excel_buffer, index=False, sheet_name='Customers')

        excel_buffer.seek(0)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=customers.xlsx'

        response.write(excel_buffer.getvalue())

        return response
    except Exception as e:
        print(f"Error fetching data: {e}")
        return JsonResponse({"error": "Failed successfully!", "message": str(e)})
    finally:
        cursor.close()
        connection.close()



@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def fetch_user_addresses(request):
    try:
        connection, cursor = get_sql_anywhere_connection()
        print("ciddd")
        cid = request.data['UserID']
        print(cid)
        org_id = request.data['org_id']
        query = """
            SELECT *
            FROM "dba"."Users_Address"          
            WHERE Org_ID = ? AND UserID = ?
        """

        # query = "SELECT * FROM \"dba\".\"Order_Item\" WHERE OrderNo = ? AND Org_ID = ?"
        cursor.execute(query, ( org_id, cid))
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        data_list = [dict(zip(columns, row)) for row in rows]
        print(data_list)
        return JsonResponse({"message": "Fetched successfully.", "data": data_list})
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": f"Failed to fetch Product: {str(e)}"}, status=500)
    finally:
        cursor.close()
        connection.close()
