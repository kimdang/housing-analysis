import pymysql 



def run_query(query, fetch=False, fetch_option='fetchone'):
    conn = pymysql.connect(host="10.0.0.10", 
                        user="root",
                        password="123456",
                        charset="utf8mb4",
                        db="housing_database",
                        cursorclass=pymysql.cursors.DictCursor)

    print(query)

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