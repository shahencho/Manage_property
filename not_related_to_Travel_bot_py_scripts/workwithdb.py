# import MySQLdb
import mysql.connector
from datetime import datetime

import settings

def initiate_connection():
    mydb = mysql.connector.connect(
    host='localhost',
    user='shahencho',
    password='Myelea82!',
    database='shahencho_mydatabase'
    )
    return mydb

# print (settings.Cell_To_Find)


def realize_table_to_use(bot_id_param):
      
      if bot_id_param==7072468689:
        print("Innova Management 7072468689  ")
        Use_table_name= "Innova_User_History" 

      elif bot_id_param==5946410507:
        print("Carav is called u 5946410507 ")
        Use_table_name= "Carav_User_History" 
      elif bot_id_param==7256193277:
        print("dev82 is called u 7256193277 ")
        Use_table_name= "dev82_User_History" 
    
      else:        
        print("Unknown bot called you")

      return Use_table_name


def if_user_is_new(teleg_id, bot_id):

    Use_table_name = realize_table_to_use(bot_id)


    # global Cell_To_Find
    print ("Cell to find in the beginning of if_user_is_new function ")
    # print (settings.Cell_To_Find)

    try:
        mydb = initiate_connection()
        mycursor = mydb.cursor()

        select_text = "SELECT count(id_telegram) FROM " + Use_table_name +" where id_telegram = '{}'"
        Query_with_id = select_text.format(teleg_id)

        print(Query_with_id)
        mycursor.execute(Query_with_id)

        myresult = mycursor.fetchone()
        print(myresult)

        for row_count in myresult:
            print("Print_row_count_from_fucntionif_user_is_new - >>>>>  " + str(row_count))

        if row_count==0:
            if_user_is_new=True

        else:
            if_user_is_new = False
            # this_will_return_array = []
            select_text = "SELECT bill_code FROM " + Use_table_name +"  where id_telegram = '{}'"
            Query_with_id = select_text.format(teleg_id)
            print(Query_with_id)
            temp_var = mycursor.execute(Query_with_id)
            print(temp_var) #none
            # print("Cell_To_Find = ")
            # print(Cell_To_Find)
            fetchoneresult  = mycursor.fetchone()

            print ("we are in if_user_is_new  function and this blocks sais that user is not new, fetchoneresult was not 0 \n ")
            # print (settings.Cell_To_Find)


            print("fetchoneresult [0]  is : ")

            print(fetchoneresult[0] )






    except mysql.connector.Error as error:
        print("Failed to update table record: {}".format(error))

    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed")


    # rewrite with trey
    return if_user_is_new

# SELECT dept_now FROM User_History where id_telegram = '449708378'


def print_table_for_me():
    mydb = initiate_connection()
    mycursor = mydb.cursor()
    mycursor.execute("Select * from User_History")
    myresult = mycursor.fetchall()
    print(myresult)
    mycursor.close()
    mydb.close()
    return myresult

def add_new_user_to_db(teleg_id, f_name, l_name, bot_id ) :

    Use_table_name_based_on_bot_id = realize_table_to_use(bot_id)

    print("we are now in add_new_user_to_db function ")

    try:
        mydb = initiate_connection()
        mycursor = mydb.cursor()

        current_Date = datetime.now()
        formatted_date = current_Date.strftime('%Y-%m-%d %H:%M:%S')

        print("Before insert  a record print - we suppose should be empty ")
        sql_select_query = "select * from "+Use_table_name_based_on_bot_id +" where id_telegram = '{}'"
        sql_select_query = sql_select_query.format(teleg_id)
        mycursor.execute(sql_select_query)
        record = mycursor.fetchone()
        print(record)

        # myresult = mycursor.fetchone()
        # print(myresult)

        # for row_count in record:
            # print("Print_row_count_from_fucntion add_new_user_to_db - >>>>>  " + str(row_count))

        if record is None:
            # Insert single record now
            print("we are inside [add_new_user_to_db] function and fetchone gets =  [None] that means we must insert new row")


            sql_insert_query = "INSERT INTO " +  Use_table_name_based_on_bot_id + " (id, id_telegram,first_name, last_name, dept_last_month, dept_now, last_date_requested, bill_code, building ,f_n_p, col3) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s )"
            value_to_insert =  ( 0, teleg_id, f_name, l_name, formatted_date, "dept_now", formatted_date, "bill_code", "building", "f_n_p", "col3" )


            print(sql_insert_query)
            print (value_to_insert)
            mycursor.execute(sql_insert_query,value_to_insert )
            mydb.commit()
            print("Record Inserted  successfully ")

            print("After insert record , we suppose should be more than 1 :) ")
            mycursor.execute(sql_select_query)
            record = mycursor.fetchone()
            print(record)
        else:
            print("we have already such row in db - i will not be inserting - ALAAAAAARM")
            value_to_insert = " Shahen - to review, this should not happen accorinding to current logic"


    except mysql.connector.Error as error:
        print("Failed to update table record: {}".format(error))

    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed")





    return value_to_insert

# ========================
#SET dept_now='{}' in db for given user.

def update_bill_code_for_given_user_to_db(teleg_id, updated_bill_code, bot_id):
    Use_table_name_based_on_bot_id = realize_table_to_use(bot_id)

    mydb = initiate_connection()
    mycursor = mydb.cursor()

    try:
        mydb = initiate_connection()
        mycursor = mydb.cursor()

        print("Before updating a record ")
        sql_select_query = "select * from "+ Use_table_name_based_on_bot_id + " where id_telegram = '{}'"
        sql_select_query = sql_select_query.format(teleg_id)
        mycursor.execute(sql_select_query)
        record = mycursor.fetchone()
        print(record)

# ------------------
#         current_Date = datetime.now()
#         formatted_date2 = current_Date.strftime('%Y-%m-%d %H:%M:%S')


#         # Insert single record now
#         sql_insert_query = "INSERT INTO User_History (id, id_telegram,first_name, last_name, dept_last_month, dept_now, last_date_requested, bill_code, building ,f_n_p, col3) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s )"
#         value_to_insert =  ( 0, teleg_id, f_name, l_name, formatted_date, "dept_now", formatted_date, "bill_code", "building", "f_n_p", "col3" )

#         # Update single record now
#         sql_update_query = "UPDATE User_History SET dept_now='{}',  last_date_requested = '{} where id_telegram ='{}'"
#         sql_update_query = sql_update_query.format(updated_bill_code,formatted_date2,  teleg_id)
#         print(sql_update_query)
#         mycursor.execute(sql_update_query)
#         mydb.commit()
#         print("Record Updated successfully ")

# =============

        current_Date = datetime.now()
        formatted_date2 = current_Date.strftime('%Y-%m-%d %H:%M:%S')
        sql_update_query = "UPDATE " + Use_table_name_based_on_bot_id + " SET dept_now='{}',  last_date_requested = '{}' where id_telegram ='{}'"
        sql_update_query = sql_update_query.format(updated_bill_code,formatted_date2,  teleg_id)


        # Update single record now
        # sql_update_query = "UPDATE User_History SET dept_now='{}' where id_telegram ='{}'"
        # sql_update_query = sql_update_query.format(updated_bill_code, teleg_id)
        print(sql_update_query)
        mycursor.execute(sql_update_query)
        mydb.commit()
        print("Record Updated successfully ")

        print("After updating record ")
        mycursor.execute(sql_select_query)
        record = mycursor.fetchone()
        print(record)

    except mysql.connector.Error as error:
        print("Failed to update table record: {}".format(error))

    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            print("MySQL connection is closed")

    return sql_update_query


# update slection of buiding in DB .

def update_selection_of_building_to_db(teleg_id, current_building, bot_id):
    Use_table_name_based_on_bot_id = realize_table_to_use(bot_id)

    
    mydb = initiate_connection()
    mycursor = mydb.cursor()

    try:
        mydb = initiate_connection()
        mycursor = mydb.cursor()

        print("update_selection_of_building_to_db - > Before updating a record ")
        sql_select_query = "select * from "+ Use_table_name_based_on_bot_id + " where id_telegram = '{}'"
        sql_select_query = sql_select_query.format(teleg_id)
        mycursor.execute(sql_select_query)
        record = mycursor.fetchone()
        print(record)

        # Update single record now
        sql_update_query = "UPDATE " + Use_table_name_based_on_bot_id + " SET building ='{}' where id_telegram ='{}'"
        sql_update_query = sql_update_query.format(current_building, teleg_id)
        print(sql_update_query)
        mycursor.execute(sql_update_query)
        mydb.commit()
        print("Record Updated successfully ")

        print("After updating record ")
        mycursor.execute(sql_select_query)
        record = mycursor.fetchone()
        print(record)

    except mysql.connector.Error as error:
        print("this is fucntion update_selection_of_building_to_db - > Failed to update table record: {}".format(error))

    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            print("update_selection_of_building_to_db - > MySQL connection is closed")

    return sql_update_query


#get building selection from db  based on telg id.

# update selection of flat/nkugg/Parking  in DB .

def update_selection_of_F_N_P_to_db(teleg_id, column_id, value_of_column, bot_id ):
    Use_table_name_based_on_bot_id = realize_table_to_use(bot_id)

    mydb = initiate_connection()
    mycursor = mydb.cursor()

    try:
        mydb = initiate_connection()
        mycursor = mydb.cursor()

        print("update_selection_of_F_N_P_to_db      - > Before updating a record ")
        sql_select_query = "select * from " + Use_table_name_based_on_bot_id + " where id_telegram = '{}'"
        sql_select_query = sql_select_query.format(teleg_id)
        mycursor.execute(sql_select_query)
        record = mycursor.fetchone()
        print(record)

        # Update single record now
        sql_update_query = "UPDATE " + Use_table_name_based_on_bot_id + " SET " + str(column_id) +  "='{}' where id_telegram ='{}'"
        sql_update_query = sql_update_query.format(value_of_column, teleg_id)
        print (sql_update_query)


        mycursor.execute(sql_update_query)
        mydb.commit()
        print("Record Updated successfully ")

        print("After updating record ")
        mycursor.execute(sql_select_query)
        record = mycursor.fetchone()
        print(record)

    except mysql.connector.Error as error:
        print("this is fucntion update_selection_of_F_N_P_to_db  - > Failed to update table record: {}".format(error))

    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            print("update_selection_of_F_N_P_to_db  - > MySQL connection is closed")

    return sql_update_query

# ENd of update selection of flat/nkugg/Parking  in DB .




#get building selection from db  based on telg id.



def get_selection_of_building_from_db_by_teleg_id (teleg_id, column_id, bot_id):

    Use_table_name_based_on_bot_id = realize_table_to_use(bot_id)
    # global Cell_To_Find
    print ("get_selection_of_building_from_db_by_teleg_id   in the beginning of if_user_is_new function ")
    # print (settings.Cell_To_Find)

    try:
        mydb = initiate_connection()
        mycursor = mydb.cursor()

        select_text = "SELECT count(id_telegram) FROM " + Use_table_name_based_on_bot_id + " where id_telegram = '{}'"
        Query_with_id = select_text.format(teleg_id)

        print(Query_with_id)
        mycursor.execute(Query_with_id)

        myresult = mycursor.fetchone()
        print(myresult)

        for row_count in myresult:
            print("get_selection_of_building_from_db_by_teleg_id  -  row_count = >>>>>  " + str(row_count))

        if row_count==0:
            selection_of_building_from_db = "row_cunt_is_0"
            print("get_selection_of_building_from_db_by_teleg_id fucntion - >>> there is no such row  in Db.   ")
            print("selection_of_building_from_db = " +str(selection_of_building_from_db))


        else:
            selection_of_building_from_db = "row_cunt_is_1"
            # this_will_return_array = []
            select_text = "SELECT {} FROM " + Use_table_name_based_on_bot_id + " where id_telegram = '{}'"
            Query_with_id = select_text.format( column_id, teleg_id)
            print(Query_with_id)
            temp_var = mycursor.execute(Query_with_id)
            print(temp_var) #none
            # print("Cell_To_Find = ")
            # print(Cell_To_Find)
            fetchoneresult  = mycursor.fetchone()

            print ("get_selection_of_building_from_db_by_teleg_id fucntion is called  0-           >>>>> ")

            selection_of_building_from_db  = fetchoneresult[0]

            print("fetchoneresult [0] = selection_of_building_from_db and   is : ")

            print(fetchoneresult[0] )






    except mysql.connector.Error as error:
        print("get_selection_of_building_from_db_by_teleg_id futnion - > Failed to update table record: {}".format(error))

    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            print("get_selection_of_building_from_db_by_teleg_id futnion ------- >  MySQL connection is closed")


    # rewrite with trey
    return selection_of_building_from_db



