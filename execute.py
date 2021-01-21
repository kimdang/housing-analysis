import pymysql 
import credentials



def run_query(query, fetch=False, fetch_option='fetchone'):
    conn = pymysql.connect(host=credentials.db_host, 
                        user=credentials.db_username,
                        password=credentials.db_password,
                        charset="utf8mb4",
                        db=credentials.db_name,
                        cursorclass=pymysql.cursors.DictCursor)


    with conn.cursor() as cursor:
        cursor.execute(query)
        if fetch==True:
            if fetch_option == "fetchone":
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()

        conn.commit()
        cursor.close()

    conn.close()    

    if fetch==True:
        return result
    else:
        return    