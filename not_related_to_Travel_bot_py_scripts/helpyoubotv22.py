

# update_selection_of_building_to_db , get_selection_of_building_from_db_by_teleg_id introduced in workwithdb.py , now we will try to avoid usage of global settings.Cell_To_Find
# AM version

import gspread  # импорти библиотеку
import telebot
import time

# import pyTelegramBotAPI

import sys
print(sys.path)

import os

folder_path = os.path.dirname(os.path.abspath("workwithdb.py"))
folder_name = os.path.basename(folder_path)

print(folder_name)

from telebot import types  # для указание типов
from home.shahencho.workwithdb import *

# from workwithdb import *
from home.shahencho.workwithdb import if_user_is_new
from home.shahencho.workwithdb.Find_Dept_By_Code import Find_Dept_By_Code
from home.shahencho.workwithdb.Find_Dept_By_Code  import get_month_in_am
from home.shahencho.workwithdb.Find_Dept_By_Code import Realize_worksheet_by_building

import settings

# import logging

# logger = logging.getLogger('logger')

# time.sleep(1)

# print("time.sleep(1)")

# time.sleep(20)

# add_new_user_to_db(449708378, "shah", "kuku")

if if_user_is_new(5215699499):
    add_new_user_to_db(5215699499, "Xuan", "Fran" )



# add_new_user_to_db(4544, "A-5")
# update_new_user_to_db(4544,"A-444-444" )

# print(Find_Dept_By_Code("P-5534-22"))

# print(Find_Dept_By_Code("P-5534-22091"))


token = '5946410507:AAF5VAgSyF3DirCVWuLVEF9eqLt8yNKrqhg'
bot = telebot.TeleBot(token)
HELP = """
=============
'what address are you interested in 55 /xx , it should be one of 17, 20, 3, 33, 34 ?
->>>>>>>>>>>>>>>>>>
"""

gs = gspread.service_account(filename='credentials.json')  # подключаем файл с ключами и пр.
sh = gs.open_by_key('1w2wOpN5CCX5Xhlrqbm5e6eJWDXMchb-30j5EzvyxJBQ')  # подключаем таблицу по ID
wks = sh.get_worksheet(0)

# last_month_available_in_ggogle_doc - get it just once , use during whole time , it's -1 from where "ամսավճար"

find_cell_amsavchar="ամսավճար"
cell_amsavchar = wks.find(find_cell_amsavchar)
column_where_amsvachar_column_is = cell_amsavchar.col
print(f"{column_where_amsvachar_column_is} value of column_where_amsvachar_column_is " )
# getcell , like - > Պարտք 31.10.2022
val11 = wks.cell(1, column_where_amsvachar_column_is-1).value
get_month_by_number = val11[9:11]
get_day_date_from_google_doc = val11[5:]
current_month_am = get_month_in_am(get_month_by_number)

print("val11 = " +str(val11) + " get_month_by_number = " + str(get_month_by_number) + " get_day_date_from_google_doc = " + str(get_day_date_from_google_doc))

#endof last_month_available_in_ggogle_doc



# worksheet = sh.sheet1  # получаем первый лист
Avan_list_Adress = [17, 20, 3, 33, 34]
exist_count = 99  # some initial value
someParam = True
# col_where_it_was_found = 0


# Cell_To_Find = "undefined In Hlyoubot"

##this function will return array with row where code was found
def Find_Code_By_address(message_chat_id,kotorak, bnak_hamar, worksheet_sequence):
    wks = sh.get_worksheet(worksheet_sequence)
    # global col_where_it_was_found
    col_where_it_was_found = 0
    # global Cell_To_Find
    combined_row = "uknown2"
    if worksheet_sequence == 0 or worksheet_sequence == 2:
        # settings.Cell_To_Find = "A-55" + str(kotorak) + "-" + str(bnak_hamar)
        combined_row = "A-55" + str(kotorak) + "-" + str(bnak_hamar)

        if combined_row =="A-5520-187" or combined_row =="A-5520-188":
            combined_row = "A-5520-187-188"
            #this is beacause in google doc we have such exception , that code for flats 187 and 88 are together, so we should find code with A-5520-187-188

        print("combined_row =  BROOOOOOOOOOOOOOOOOOOOOOOO --------------------" + combined_row )

        # update_selection_of_F_N_P_to_db(message_chat_id, "f_n_p", settings.Cell_To_Find)

        # print("update_selection_of_building_to_db                     \n")
        # update_selection_of_building_to_db(message_chat_id, settings.Cell_To_Find)
        # print(update_selection_of_building_to_db(message_chat_id, settings.Cell_To_Find))

        # print(get_selection_of_building_from_db_by_teleg_id(message_chat_id, "dept_now"))

        # print("get_selection_of_building_from_db_by_teleg_id          endeeeeeeeeeeeeeeeeeeed .  \n")
        # print("get_selection_of_building_from_db_by_teleg_id(message_chat_id, 'col1222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222')")
        # print(get_selection_of_building_from_db_by_teleg_id(message_chat_id, "col1"))


    elif worksheet_sequence == 1 or worksheet_sequence == 3:
        print("nkuhg or kayanateghi")
        combined_row = "S-55" + str(kotorak) + "-" + str(bnak_hamar)


    print("combined_row = " + combined_row )
    cell_list = wks.find(combined_row)  # find cell with given code number
    values_list = wks.row_values(cell_list.row)  # get whole row with "given code" that found what row is this
    col_where_it_was_found = cell_list.col

    print(cell_list.row)
    print(values_list)
    print(values_list[col_where_it_was_found])

    # find ամսավճար cell and get column , so when required duty will be calculated we will do (column_where_amsvachar_column_is -1)
    find_cell = "ամսավճար"
    cell_amsavchar = wks.find(find_cell)
    # new_list = wks.row_values(cell_amsavchar.row)  # get whole row with "given code" that found what row is this
    column_where_amsvachar_column_is = cell_amsavchar.col

    print(f"{column_where_amsvachar_column_is} value of column_where_amsvachar_column_is ")

    final_duty_to_be_paid = values_list[column_where_amsvachar_column_is - 2]

    # settings.last_kotorak_value = kotorak
    # settings.last_bnak_hamar = bnak_hamar
    # settings.last_worksheet_sequence = worksheet_sequence

    print(final_duty_to_be_paid)

    temp21  = update_bill_code_for_given_user_to_db(message_chat_id, final_duty_to_be_paid) # 0 > rename to Depnow

    print ("value of fucntion  - > update_bill_code_for_given_user_to_db(message_chat_id, final_duty_to_be_paid)  = " +  temp21 )

    temp67 = update_selection_of_F_N_P_to_db(message_chat_id, "bill_code" , combined_row)

    print ("""update_selection_of_F_N_P_to_db(message_chat_id, 'bill_code' , combined_row)  = """ + temp67) #-> rename to  update_db_col_id_value



    return final_duty_to_be_paid


# Find_Code_By_address(20,10,0 )

# default values.

building_you_selected = "uknown"


@bot.message_handler(commands=['start'])
def start(message):
    # global current_user_id_start
    current_user_id_start = 99898
    # global Cell_To_Find
    current_user_id_start = message.chat.id
    message_chat_id = message.chat.id
    first_name_of_current_user = message.chat.first_name

    print(message.chat.first_name)
    print(message.chat.last_name)
    print(message.chat.id)

    # print("building_you_selected suring start  = " + str(building_you_selected))

    if if_user_is_new(current_user_id_start):
        add_new_user_to_db(current_user_id_start, message.chat.first_name, message.chat.last_name )

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("55/17")
        btn2 = types.KeyboardButton("55/20")
        btn_Avan6_1 = types.KeyboardButton("55/3")
        btn_Avan6_2 = types.KeyboardButton("55/33")
        btn_Avan6_3 = types.KeyboardButton("55/34")
        # btn_find_code_s_p = types.KeyboardButton("Find S or P by code")

        markup.add(btn1, btn2, btn_Avan6_1, btn_Avan6_2, btn_Avan6_3)


        bot.send_message(message.chat.id,
                         text="Ողջույն, " + first_name_of_current_user + " : Ես Նորավանի բոտն եմ և կօգնեմ Ձեզ տեղեկություն ստանալ Ձեր սեփականության ընթացիկ պարտքի կամ կանխավճարի մասին։ Հուսով եմ պարտք չէ, կանխավճար է :) \nԱյս պահին հասանելի է " + str(current_month_am) + " ամիսը:\n", reply_markup=markup)





    else:
        # print("aaaaa Cell to find ixxxx")
        # print(settings.Cell_To_Find)

        last_code_saved_in_db = get_selection_of_building_from_db_by_teleg_id(current_user_id_start, "bill_code")
        print ("get_selection_of_building_from_db_by_teleg_id(current_user_id_start) =   " + str(last_code_saved_in_db) )

        text_to_send_registered_user = "Ողջույն, {}!\n Դուք օգտվել եք այս համակարգից և ես ձեզ հիշում եմ, վերջին անգամ դուք հետաքրքված էիք հետևյալով {} :) \nԱյս պահին հասանելի է " + str(current_month_am) + " ամիսը: \n"

        # text_to_send_registered_user = text_to_send_registered_user.format(first_name_of_current_user,
        #                                                                   settings.Cell_To_Find)

        text_to_send_registered_user = text_to_send_registered_user.format(first_name_of_current_user,
                                                                           get_selection_of_building_from_db_by_teleg_id(current_user_id_start, "bill_code"))



        # bot.send_message(message.chat.id, text = text_to_send_registered_user, reply_markup=markup)

        text_to_print = str(
            text_to_send_registered_user) + " Խնդրում եմ ընտրեք ինչ եք ցանկանում անել, սեղմեք  «Այո, այդ ես եմ», եթե ցանկանում եք տեսնել " + str(
            last_code_saved_in_db) + " կոդով սեփականության պարտքը, կամ սեղմեք «Վերադարձ գլխավոր մենյու», եթե ցանկանում եք այլ որոնում իրականցել"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        correct_button = types.KeyboardButton("Այո, այդ ես եմ")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
        markup.add(correct_button, back)
        bot.send_message(message.chat.id, text=text_to_print, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    global building_you_selected
    message_chat_id = message.chat.id
    current_user_id_text = message.chat.id

    print("building_you_selected = " + str(building_you_selected))

    if if_user_is_new(message_chat_id):
        add_new_user_to_db(message_chat_id, message.chat.first_name, message.chat.last_name )



    # print("settings.selected_worksheet_is = " + str(settings.selected_worksheet_is))

    # print ("last_kotorak_value =  " + str(settings.last_kotorak_value) )
    # print ("last_bnak_hamar = " + str(settings.last_bnak_hamar))


    global dutytopay
    # selected_worksheet_is = 0  #by default it will be 0

    dutytopay = 99999999  # some default value
    x = message.text
    # sdsddddddddddddddddddd

    current_val_of_building_from_db_by_teleg_id  = get_selection_of_building_from_db_by_teleg_id (current_user_id_text,  "building")



    print(str(current_val_of_building_from_db_by_teleg_id) + "get_selection_of_building_from_db_by_teleg_id (current_user_id_text,  building) ")

    if (message.text == "55/17"):
        building_you_selected = "Avan4 55/17"
        # settings.selected_worksheet_is = 0
        # please select what do you want flat/nkukh/parking

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_flat = types.KeyboardButton("Բնակարան")
        btn2_nkugh = types.KeyboardButton("Նկուղ")
        btn3_parking = types.KeyboardButton("Կայանատեղի")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
        markup.add(btn1_flat, btn2_nkugh, btn3_parking, back)
        bot.send_message(message.chat.id, text="Դուք ընտրել եք " + str(
            message.text) + " շենքը։ Ընտրեք խնդրեմ, ինչ տեսակի սեփականության համար եք ցանկանում որոնել՝ սեղմելով համապատասխան կոճակը։",
                         reply_markup=markup)

        print(
            "user should slect  ->btn1_flat or btn2_nkugh btn3_parking , considering that building_you_selected  55/17   was chosen -> building_you_selected = [Avan4 55/17]") #-------------------------------------------------------
        print(building_you_selected)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        update_selection_of_building_to_db(current_user_id_text, building_you_selected ) #save this selection to DB in column 'building'


    elif (message.text == "55/20"):

        building_you_selected = "Avan4 55/20"
        # settings.selected_worksheet_is = 0

        # please select what do you want flat/nkukh/parking

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_flat = types.KeyboardButton("Բնակարան")
        btn2_nkugh = types.KeyboardButton("Նկուղ")
        btn3_parking = types.KeyboardButton("Կայանատեղի")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")

        markup.add(btn1_flat, btn2_nkugh, btn3_parking, back)

        bot.send_message(message.chat.id, text="Դուք ընտրել եք " + str(
            message.text) + " շենքը։ Ընտրեք խնդրեմ, ինչ տեսակի սեփականության համար եք ցանկանում որոնել՝ սեղմելով համապատասխան կոճակը։",
                         reply_markup=markup)

        print(
            "user should slect  ->btn1_flat or btn2_nkugh btn3_parking , considering that building_you_selected  55/20   was chosen - > -> building_you_selected = [Avan4 55/20]")
        print(building_you_selected)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        update_selection_of_building_to_db(current_user_id_text, building_you_selected ) #save  building_you_selected selection to DB  > it will save in  column "col1"


    # ====Avan6 worksheet 2 -------------------------------------------------
    elif (message.text == "55/33"):
        building_you_selected = "Avan6 55/33"
        # settings.selected_worksheet_is = 2

        # please select what do you want flat/nkukh/parking

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_flat = types.KeyboardButton("Բնակարան")
        btn2_nkugh = types.KeyboardButton("Նկուղ")
        btn3_parking = types.KeyboardButton("Կայանատեղի")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")

        markup.add(btn1_flat, btn2_nkugh, btn3_parking, back)

        bot.send_message(message.chat.id, text="Դուք ընտրել եք " + str(
            message.text) + " շենքը։ Ընտրեք խնդրեմ, ինչ տեսակի սեփականության համար եք ցանկանում որոնել՝ սեղմելով համապատասխան կոճակը։",
                         reply_markup=markup)

        print(
            "user should slect  ->btn1_flat or btn2_nkugh btn3_parking , considering that building_you_selected  Avan6 55/33   was chosen-> -> building_you_selected = [Avan4 55/33]")
        print(building_you_selected)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        update_selection_of_building_to_db(current_user_id_text, building_you_selected ) #save  building_you_selected selection to DB  > it will save in  column "col1"

    elif (message.text == "55/3"):
        building_you_selected = "Avan6 55/3"
        # settings.selected_worksheet_is = 2

        # please select what do you want flat/nkukh/parking

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_flat = types.KeyboardButton("Բնակարան")
        btn2_nkugh = types.KeyboardButton("Նկուղ")
        btn3_parking = types.KeyboardButton("Կայանատեղի")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")

        markup.add(btn1_flat, btn2_nkugh, btn3_parking, back)

        bot.send_message(message.chat.id, text="Դուք ընտրել եք " + str(
            message.text) + " շենքը։ Ընտրեք խնդրեմ, ինչ տեսակի սեփականության համար եք ցանկանում որոնել՝ սեղմելով համապատասխան կոճակը։",
                         reply_markup=markup)
        print(
            "user should slect  ->btn1_flat or btn2_nkugh btn3_parking , considering that building_you_selected  Avan6 55/3   was chosen - > -> building_you_selected = [Avan4 55/3]")
        print(building_you_selected)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        update_selection_of_building_to_db(current_user_id_text, building_you_selected ) #save  building_you_selected selection to DB  > it will save in  column "col1"

    elif (message.text == "55/34"):
        building_you_selected = "Avan4 55/34"
        # settings.selected_worksheet_is = 2

        # please select what do you want flat/nkukh/parking

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_flat = types.KeyboardButton("Բնակարան")
        btn2_nkugh = types.KeyboardButton("Նկուղ")
        btn3_parking = types.KeyboardButton("Կայանատեղի")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")

        markup.add(btn1_flat, btn2_nkugh, btn3_parking, back)

        bot.send_message(message.chat.id, text="Դուք ընտրել եք " + str(
            message.text) + " շենքը։ Ընտրեք խնդրեմ, ինչ տեսակի սեփականության համար եք ցանկանում որոնել՝ սեղմելով համապատասխան կոճակը։",
                         reply_markup=markup)

        print(
            "user should slect  ->btn1_flat or btn2_nkugh btn3_parking , considering that building_you_selected  Avan6 55/34   was chosen -> building_you_selected = [Avan4 55/34]")
        print(building_you_selected)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)


        update_selection_of_building_to_db(current_user_id_text, building_you_selected ) #save  building_you_selected selection to DB  > it will save in  column "col1"

    elif (message.text == "Find S or P by code"):

        building_you_selected = "Avan4 55/17"  # this to set some defsault value to initialize it -

        bot.send_message(message.chat.id,
                         text="ok, ->  i will need Code number it shoild match  ~ format S-5534-107 or P-5534-26")
        print("i will call fuction to Find S or P by code")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        # btn1 = types.KeyboardButton("no need")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
        markup.add(back)

        update_selection_of_building_to_db(current_user_id_text, building_you_selected ) #save  building_you_selected selection to DB  > it will save in  column "col1"


    elif (x.startswith("S") or x.startswith("P")):
        temp_val = Find_Dept_By_Code(x, current_user_id_text)
        if temp_val == "myundefined":

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
            markup.add(back)
            bot.send_message(message.chat.id, text=(
                    temp_val + " , there is no such 'Code'  , please try again with format: 'S-5534-107' or 'P-5534-26' ->>>----"),
                             reply_markup=markup)

            print("не нашли")
        else:
            text_to_print = " Dear Customer , for Code in P or S  {} you are looking for   "
            temp_text = text_to_print.format(x)
            if temp_val.startswith("-"):  # " means we with minus at the beginning,
                bot.send_message(message.chat.id, text=(temp_text + ", you should pay ->>>"))
                bot.send_message(message.chat.id, text=temp_val)
            else:
                bot.send_message(message.chat.id,
                                 text=(temp_text + "You don't have much to pay, your balance is positive"))
                bot.send_message(message.chat.id, text=temp_val)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
            markup.add(back)
            bot.send_message(message.chat.id,
                             text=" you may request another 'Code';  it shoild match  ~ format S-5534-107 or P-5534-26  or press button and go to home page ",
                             reply_markup=markup)


    # print(type(x))
    elif (x.isnumeric() == True) and get_selection_of_building_from_db_by_teleg_id(  current_user_id_text, "f_n_p") == "flat":
        print("numeric")


        building_you_selected_v2 = get_selection_of_building_from_db_by_teleg_id(message_chat_id, "building")
        print('get_selection_of_building_from_db_by_teleg_id(message_chat_id, "building") = ', building_you_selected_v2  )
        curr_wsheet = Realize_worksheet_by_building(building_you_selected_v2)
        print('curr_wsheet = Realize_worksheet_by_building(building_you_selected_v2)' + str(curr_wsheet)  )


        if int(x) < 281 and (
                int(x) >= 1):  # and building_you_selected : to be ADDDDDDDDDDDDDDDDDDEDDDDDDDDDDDDDDDDDDDDDDDDDDD
            # "Avan4 55/20" --- Avan6 55/3 ---Avan6 55/33 Avan6 55/34
            x = int(x)
            # get
            if curr_wsheet == 0:
                get_kototak_from_selection = building_you_selected_v2[9:11]
                if (int(get_kototak_from_selection) == 17 or int(get_kototak_from_selection) == 20):
                    dutytopay = Find_Code_By_address(message_chat_id, get_kototak_from_selection, x, curr_wsheet)
                    # ins_data_to_db(get_kototak_from_selection , flat_number, config.selected_worksheet_is ,     -- this supposed to be flat_number
                    #  e.g. Cell_To_Find  A-5517-34

                    print(current_user_id_text)
                    print(building_you_selected_v2)


                # elif int(get_kototak_from_selection) == 20:
                #     if x == 187 or x == 188:
                #         print("plz correct that row for 20 flat 187/188")
                #         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                #         # btn1 = types.KeyboardButton("no need")
                #         back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
                #         markup.add(back)
                #         bot.send_message(message.chat.id,
                #                          text=" Դուք կարող եք ճշտել այլ բնակարանի պարտք   " + building_you_selected_v2[6:] + "  շենքում կամ կարող եք վերադառնալ գլխավոր մենյու՝ սեղմելով համապատասխան կոճակը։ 55/20 շենքում այլ բնակարան ճշտելու համար մուտքագրեք բնակարանի համարը։ ",
                #                          reply_markup=markup)

                #     else:
                #         dutytopay = Find_Code_By_address(message_chat_id, get_kototak_from_selection, x, curr_wsheet)

                else:
                    print("get_kototak_from_selection suppose to be 17 or 20 for worksheet 0, error - > ")

            elif curr_wsheet == 2 and len(
                    building_you_selected_v2) == 11 and x < 71:  # "Avan4 55/20" --- Avan6 55/3 ---Avan6 55/33 Avan6 55/34
                get_kototak_from_selection = building_you_selected[9:11]
                if (int(get_kototak_from_selection) == 33):  # --------------> building selection was 33
                    dutytopay = Find_Code_By_address(message_chat_id, get_kototak_from_selection, x, curr_wsheet)
                    # update_new_user_to_db(current_user_id, building_you_selected_v2)

                elif int(get_kototak_from_selection) == 34:  # --------------> building selection was 34
                    dutytopay = Find_Code_By_address(message_chat_id, get_kototak_from_selection, x, curr_wsheet)
                    # update_new_user_to_db(current_user_id, building_you_selected_v2)

            elif curr_wsheet == 2 and len(
                    building_you_selected_v2) == 10 and x < 71:  # "Avan4 55/20" --- Avan6 55/3 ---Avan6 55/33 Avan6 55/34
                get_kototak_from_selection = building_you_selected_v2[9:10]
                if (int(get_kototak_from_selection) == 3):  # building selection was 3
                    dutytopay = Find_Code_By_address(message_chat_id, get_kototak_from_selection, x, curr_wsheet)
                    # update_new_user_to_db(current_user_id, building_you_selected_v2)


            else:
                # this means dutytopay = 99999999 means it was not yet intialiized , so we need to skip block below.
                print("flat is not in range , error - > need to debug maybe? ")
                print(building_you_selected_v2)
                text_to_print = " Ներեցեք, չեմ հասկանում ինչ հարցում եք կատարում։ Մուտքագրեք խնդրում եմ բնակարանի համարը 1-280 միջակայքում։ Խնդրում եմ կրկին փորձեք կամ կարող եք վերադարձ կատարել գլխավոր մենյու"

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
                markup.add(back)
                bot.send_message(message.chat.id, text=text_to_print, reply_markup=markup)

            print("type(dutytopay) ------------ ")
            print(type(dutytopay))

            dutytopay = str(dutytopay)

            if dutytopay != "99999999":
                print("flat is good")
                print(building_you_selected_v2)
                # bot.send_message(message.chat.id, text="for this flat you must pay .")
                text_to_print = " Հարգելի սեփականատեր,{} դրությամբ {} շենքի {} "
                temp_text = "uknownnnn"
                temp_text = text_to_print.format(get_day_date_from_google_doc, building_you_selected_v2[6:], int(x))

                print("type(dutytopay) ------------ ")
                print(type(dutytopay))
                if dutytopay.startswith("-"):  # " means we with minus at the beginning,

                    text_to_print = " Հարգելի սեփականատեր,{} դրությամբ Դուք ցավոք պարտք ունեք :(\n{} շենքի {} "
                    temp_text = "uknownnnn"
                    temp_text = text_to_print.format(get_day_date_from_google_doc, building_you_selected_v2[6:], int(x))

                    bot.send_message(message.chat.id, text=(temp_text + "բնակարանի պարտքը կազմում է` "))
                    bot.send_message(message.chat.id, text=dutytopay + " դրամ")

                    txt1 = """ Խնդրում եմ շուտափույթ մարել պարտքը հետևյալ ռեկվիզիտներով՝
Բանկային հաշվեհամար՝ 220563350051000 AMD ACBA Bank
Ստացող՝ «Նորավան» ՀՄՏ
Վճարում կատարելիս նպատակը դաշտում նշել տվյալ գույքի(բնակարան, կայանատեղի, նկուղ) կոդը: Օրինակ՝ «A-5520-6» կամ «P-5520-2» կամ «S-5520-212»։
Կամ EasyPay և FastShift տերմինալներով։
Ձեր վճարման կոդն է՝
"""

                    bot.send_message(message.chat.id, text=txt1)
                    # bot.send_message(message.chat.id, text=str(settings.Cell_To_Find))

                    current_billcode_in_db = get_selection_of_building_from_db_by_teleg_id(current_user_id_text, "bill_code")
                    print ("current_billcode_in_db = " + str(current_billcode_in_db))

                    bot.send_message(message.chat.id, text = current_billcode_in_db)
                    bot.send_message(message.chat.id, text="Շնորհակալություն։")




                else:
                    bot.send_message(message.chat.id,
                                     text=(
                                                 temp_text + " բնակարանի համար դուք ունեք կանխավճար, որի համար Նորավան համատիրությունը Ձեզ հոգաչափ շնորհակալ է և հպարտանում է Ձեզանով։ Ձեր կանխավճարը կազմում է՝"))
                    bot.send_message(message.chat.id, text=dutytopay + " դրամ")

                    # bot.send_message(message.chat.id, text = get_selection_of_building_from_db_by_teleg_id(current_user_id, "f_n_p"))

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
                markup.add(back)
                bot.send_message(message.chat.id,
                                 text=" Դուք կարող եք ճշտել այլ բնակարանի պարտք " + building_you_selected_v2[6:] + "  շենքում կամ կարող եք վերադառնալ գլխավոր մենյու՝ սեղմելով համապատասխան կոճակը: " + building_you_selected_v2[6:] + " շենքում այլ բնակարան ճշտելու համար մուտքագրեք բնակարանի համարը։ ",
                                 reply_markup=markup)



            else:
                print("dutytopay = 99999999 means it was not yet intialiized ")



        else:
            print("flat is not good ")
            print(building_you_selected_v2)
            text_to_print = "Ներեցեք, չեմ հասկանում ինչ հարցում եք կատարում։ Մուտքագրեք խնդրում եմ բնակարանի համարը 1-280 միջակայքում։ Խնդրում եմ կրկին փորձեք։"
            # temp_text = text_to_print.format(building_you_selected,int(x))
            # bot.send_message(message.chat.id, text = text_to_print)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
            markup.add(back)
            bot.send_message(message.chat.id, text=text_to_print, reply_markup=markup)

    # ------------------------------settings.nkugh_parking_flat == "nkugh":settings.nkugh_parking_flat == "parking"  - if nkugh_parking_flat ==flat it will cover on above IF else , not here, this peace only for nkuga and parking.

    # building_you_selected_v2 = get_selection_of_building_from_db_by_teleg_id(message_chat_id, "col1")


    elif (x.isnumeric() == True) and get_selection_of_building_from_db_by_teleg_id(current_user_id_text, "f_n_p") == "nkugh" and current_val_of_building_from_db_by_teleg_id != "uknown" or ( #  building_you_selected != "uknown"  - > this must be fixed to understand when this is happpeneing..
            x.isnumeric() == True) and get_selection_of_building_from_db_by_teleg_id(  current_user_id_text, "f_n_p")== "parking" and current_val_of_building_from_db_by_teleg_id != "uknown":




        print("we are in section of nkugh")
        # selected_worksheet_for_nkugh_parking = settings.selected_worksheet_is + 1
        # u should continue from here, 000000000000000000000000000000000000000000 find cell by entered Num - > find in selected worksheet - you have that .

        building_you_selected_v2 = get_selection_of_building_from_db_by_teleg_id(message_chat_id, "building")
        # print('elif (x.isnumeric() == True) and settings.nkugh_parking_flat == "nkugh"= ', building_you_selected_v2  )


        x = int(x)
        if len(building_you_selected_v2) == 10:  # and x>0 and x < 108:   # Avan6 55/3 and not ->  ---Avan6 55/33 Avan6 55/34

            get_kototak_from_selection = building_you_selected_v2[9:10]  # - this suppose to be "3" ALWAYS
            print("get_kototak_from_selection" + str(get_kototak_from_selection))

        elif len(building_you_selected_v2) == 11:  # and x>0 and x < 300:
            get_kototak_from_selection = building_you_selected_v2[9:11]  # - this suppose to be "33"  "20"  ,  "34"
            print("get_kototak_from_selection " + str(get_kototak_from_selection))

        print("building_you_selected_v2 " + str(building_you_selected_v2))

        get_current_f_n_p  = get_selection_of_building_from_db_by_teleg_id(current_user_id_text, "f_n_p")
        print ("get_current_f_n_p " + get_current_f_n_p)

        # if selected_worksheet_for_nkugh_parking == 1 or selected_worksheet_for_nkugh_parking == 3:  # we should remove this ----------------- validation !!!!!!!!!!!!!!!!!!!!!!
            # print("nkuhg or kayanateghi")



        if get_current_f_n_p == "nkugh":
            # settings.Cell_To_Find = "S-55" + str(get_kototak_from_selection) + "-" + str(x)
            combined_code = "S-55" + str(get_kototak_from_selection) + "-" + str(x)
        elif get_current_f_n_p == "parking":
            # settings.Cell_To_Find = "P-55" + str(get_kototak_from_selection) + "-" + str(x)
            combined_code = "P-55" + str(get_kototak_from_selection) + "-" + str(x)

        # example "S-553-71"  or "P-5520-43" max - S-5534-107 S-5520-224
        # parking max P-5520-48 , so 48   / P-5534-26 , so 26
        print ("combined_code = " + combined_code )

        dutytopay = Find_Dept_By_Code(combined_code, current_user_id_text)

        print ("combined_code = " + combined_code )


        print("dutytopay  = " + str(dutytopay)  )

        if dutytopay == "myundefined":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
            markup.add(back)
            bot.send_message(message.chat.id,
                             text=" Այդպիսի կոդով նկուղ/կայանատեղի չի գտնվել  " + building_you_selected_v2[6:] + " շենքում, ստուգեք մուտքագրված համարը և կրկին մուտքագրեք կամ կարող եք վերադառնալ գլխավոր մենյու՝ սեղմելով համապատասխան կոճակը ",
                             reply_markup=markup)

        else:

            update_bill_code_for_given_user_to_db(current_user_id_text, dutytopay)
            # update_new_user_to_db(current_user_id, building_you_selected_v2[6:])
            # print("settings.Cell_To_Find " + strupdate_selection_of_F_N_P_to_db(building_you_selected_v2[6:]))

            # ======================
            print(building_you_selected_v2)
            # bot.send_message(message.chat.id, text="for this flat you must pay .")

            text_to_print = " Հարգելի սեփականատեր,{} դրությամբ {} շենքի {} "
            temp_text = "uknownnnn"
            temp_text = text_to_print.format(get_day_date_from_google_doc, building_you_selected_v2[6:], int(x))

            print("type(dutytopay) ------------ ")
            print(type(dutytopay))

            tmp_text1 = " " # some empty value .
            if (get_selection_of_building_from_db_by_teleg_id(  current_user_id_text, "f_n_p") == "nkugh"):
                tmp_text1 = "նկուղի"
            elif get_selection_of_building_from_db_by_teleg_id(  current_user_id_text, "f_n_p") == "parking":
                tmp_text1 = "կայանատեղիի"


            get_selection_of_building_from_db_by_teleg_id(  current_user_id_text, "f_n_p")


            if dutytopay.startswith("-"):  # " means we with minus at the beginning,




                bot.send_message(message.chat.id, text=(temp_text + str(tmp_text1) + " համար Դուք ցավոք պարտք ունեք :( \n" + building_you_selected_v2[6:] + " շենքի " + str(x) + " " + str(tmp_text1) + " պարտքը կազմում է "  ))
                bot.send_message(message.chat.id, text=dutytopay + " դրամ")

                txt2_temp = """Խնդրում եմ շուտափույթ մարել պարտքը հետևյալ ռեկվիզիտներով՝
Բանկային հաշվեհամար՝ 220563350051000 AMD ACBA Bank
Ստացող՝ «Նորավան» ՀՄՏ
Վճարում կատարելիս նպատակը դաշտում նշել տվյալ գույքի(բնակարան, կայանատեղի, նկուղ) կոդը: Օրինակ՝ «A-5520-6» կամ «P-5520-2» կամ «S-5520-212»։
Կամ EasyPay և FastShift տերմինալներով։
Ձեր վճարման կոդն է՝
"""
                bot.send_message(message.chat.id, text = txt2_temp)

                current_billcode_in_db = get_selection_of_building_from_db_by_teleg_id(current_user_id_text, "bill_code")
                print ("current_billcode_in_db = " + str(current_billcode_in_db))
                bot.send_message(message.chat.id, text = current_billcode_in_db)
                # bot.send_message(message.chat.id, text = str(settings.Cell_To_Find))

                bot.send_message(message.chat.id, text= " Շնորհակալություն։")




            else:
                bot.send_message(message.chat.id,
                                 text=(temp_text + str(tmp_text1) + " համար Դուք ունեք կանխավճար, որի համար Նորավան համատիրությունը Ձեզ հոգաչափ շնորհակալ է և հպարտանում է Ձեզանով։ Ձեր կանխավճարը կազմում է՝"))
                bot.send_message(message.chat.id, text=dutytopay + " դրամ")


            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
            markup.add(back)
            bot.send_message(message.chat.id,
                             text="Դուք կարող եք ճշտել այլ " + str(tmp_text1) +  " " + building_you_selected_v2[6:] + " շենքում,  մուտքագրեք համարը կամ կարող եք վերադառնալ գլխավոր մենյու՝ սեղմելով համապատասխան կոճակը ",
                             reply_markup=markup)


    # =====================================---

    # else:
    #     print("block with     else -> x.isnumeric()==True) and settings.nkugh_parking_flat == "nkugh" or (x.isnumeric()==True) and settings.nkugh_parking_flat == "parking" ")

    # if (x.isnumeric()==True) and settings.nkugh_parking_flat == "parking":
    #     print("we are in section of parking - this block doesn't really required." )

    elif (message.text == "Այո, այդ ես եմ"):
        # bot.send_message(message.chat.id, "У меня нет имени..")
        # 'A-5517-10
        # settings.Cell_To_Find = "A-5517-10"



        last_bill_code_saved_in_db = get_selection_of_building_from_db_by_teleg_id(current_user_id_text, "bill_code")

        leng = len(last_bill_code_saved_in_db)

        if last_bill_code_saved_in_db[5:6] == "-":  # A-553-2
            print("this is 55/3 shenq")
            get_kotorak = last_bill_code_saved_in_db[4:5]  # get_kotorak = '3' ; ->>> print("this is 55/3 shenq")
            get_bnak_hamar = last_bill_code_saved_in_db[6:leng]  # for case with 'A-5517-10 - > 10

        else:
            get_kotorak = last_bill_code_saved_in_db[4:6]  # for case with 'A-5517-10 - > 17

            get_bnak_hamar = last_bill_code_saved_in_db[7:leng]  # for case with 'A-5517-10 - > 10

        get_bnak_hamar = int(get_bnak_hamar)

        print("str(get_kotorak) = " + str(get_kotorak))
        print("str(get_bnak_hamar =  " + str(get_bnak_hamar))

        get_kotorak = int(get_kotorak)

        if get_kotorak == 17 or get_kotorak == 20:
            worksheet_sequence = 0
        elif get_kotorak == 3 or get_kotorak == 33 or get_kotorak == 34:
            worksheet_sequence = 2

        else:
            print("other worksheets not yet coded.")

        print(" Find_Code_By_address(message_chat_id , get_kotorak, get_bnak_hamar, worksheet_sequence): ")

        print(worksheet_sequence)
        dept_for_this_user_in_google_doc = 0  # wwwwwhhhhhhhhhhhhhtFFFFFFFFFFFFFF?

        get_firstletter_of_code = last_bill_code_saved_in_db[0:1]
        print("get_firstletter_of_code = " + str(get_firstletter_of_code))

        if get_firstletter_of_code == "A":
            dept_for_this_user_in_google_doc = Find_Code_By_address(message_chat_id, get_kotorak, get_bnak_hamar, worksheet_sequence)
            dept_for_this_user_in_google_doc = str(dept_for_this_user_in_google_doc)

        elif get_firstletter_of_code == "S" or get_firstletter_of_code == "P":
            dept_for_this_user_in_google_doc = Find_Dept_By_Code(last_bill_code_saved_in_db, current_user_id_text)

        if dept_for_this_user_in_google_doc != "99999999":
            print("dept_for_this_user_in_google_doc  is good , iether Flat/Nkugh or P ")

            building_you_selected_v2 = str(get_kotorak)
            print(building_you_selected_v2)




            # bot.send_message(message.chat.id, text="for this flat you must pay .")
            # text_to_print = "Հարգելի սեփականատեր ,  ձեր բալանսը  հետևյալ " + str(settings.Cell_To_Find) +" կոդի համար  կազմում է: "
            text_to_print = "\nԱյս պահին հասանելի է " + str(current_month_am) + " ամիսը:\nՀարգելի սեփականատեր,{} դրությամբ ձեր բալանսը հետևյալ " + str(last_bill_code_saved_in_db) +" կոդի համար  կազմում է՝"
            temp_text = "uknownnnn"
            temp_text = text_to_print.format(get_day_date_from_google_doc)
            # temp_text = text_to_print.format(get_day_date_from_google_doc, building_you_selected[6:], int(get_bnak_hamar)

            bot.send_message(message.chat.id, text = temp_text)

            bot.send_message(message.chat.id, text=dept_for_this_user_in_google_doc + " դրամ")

            print("type(dept_for_this_user_in_google_doc) ------------ ")
            print(type(dept_for_this_user_in_google_doc))
            if dept_for_this_user_in_google_doc.startswith("-"):  # " means we with minus at the beginning,


                bot.send_message(message.chat.id, text=(" Դուք ցավոք պարտք ունեք "))

                txt2_temp = """Խնդրում եմ շուտափույթ մարել պարտքը հետևյալ ռեկվիզիտներով՝
Բանկային հաշվեհամար՝ 220563350051000 AMD ACBA Bank
Ստացող՝ «Նորավան» ՀՄՏ
Վճարում կատարելիս նպատակը դաշտում նշել տվյալ գույքի(բնակարան, կայանատեղի, նկուղ) կոդը: Օրինակ՝ «A-5520-6» կամ «P-5520-2» կամ «S-5520-212»։
Կամ EasyPay և FastShift տերմինալներով։
Ձեր վճարման կոդն է՝
"""
                bot.send_message(message.chat.id, text = txt2_temp)

                bot.send_message(message.chat.id, text = str(last_bill_code_saved_in_db))

                bot.send_message(message.chat.id, text= " Շնորհակալություն։")






            else:

                bot.send_message(message.chat.id,
                                 text=("դուք ունեք կանխավճար, որի համար Նորավան համատիրությունը Ձեզ հոգաչափ շնորհակալ է և հպարտանում է Ձեզանով։"))
                # bot.send_message(message.chat.id, text=dept_for_this_user_in_google_doc + " դրամ" )

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
            markup.add(back)

            bot.send_message(message.chat.id, text=" Սեղմեք վերադարձ գլխաոոր մենյու եթե ցանկանում եք կատարել այլ որոնումներ ", reply_markup=markup) #Փ№ՓՓ Փ ցօնտինւե ֆռօմ հեոեռեե


            # bot.send_message(message.chat.id,
            #                  text=" you may request another 'flat' within {" + building_you_selected + "}  or press button and go to home page ",
            #                  reply_markup=markup)



#             ================================================================


            # Հարգելի սեփականատեր, {55}/{20} շենքի   {4}  {բնակարան /նկուղ /  կայանատեղիի / } համար Դուք ունեք կանխավճար, որի համար Նորավան համատիրությունը Ձեզ հոգաչափ շնորհակալ է և հպարտանում է Ձեզանով։ Ձեր կանխավճարը կազմում է՝

            # GetCode  = = "S-5534-88"

            # Սեղմեք վերադարձ գլխաոոր մենյու եթե ցանկանում եք կատարել այլ որոնումներ



            # tmp_text1 = " " # some empty value .
            # if (settings.nkugh_parking_flat == "nkugh"):
            #     tmp_text1 = "նկուղի"
            # elif settings.nkugh_parking_flat == "parking":
            #     tmp_text1 = "կայանատեղիի"
            # elif settings.nkugh_parking_flat == "flat":
            #     tmp_text1 = "բնակարանի"













# ===============================================================




        else:
            print("dutytopay = 99999999 means it was not yet intialiized ")



    elif (message.text == "Как меня зовут?"):
        bot.send_message(message.chat.id, "У меня нет имени..")

    elif message.text == "Что я могу?":
        bot.send_message(message.chat.id, text="Поздороваться с читателями")

    elif (message.text == "Վերադարձ գլխավոր մենյու"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("55/17")
        btn2 = types.KeyboardButton("55/20")
        btn_Avan6_1 = types.KeyboardButton("55/3")
        btn_Avan6_2 = types.KeyboardButton("55/33")
        btn_Avan6_3 = types.KeyboardButton("55/34")
        # btn_find_code_s_p = types.KeyboardButton("Find S or P by code")
        # markup.add(btn1, btn2, btn3, btn4, btn5)
        markup.add(btn1, btn2, btn_Avan6_1, btn_Avan6_2, btn_Avan6_3)

        fname =  message.from_user.first_name

        bot.send_message(message.chat.id,
                         text="Ողջույն, "  + str(fname) + "!: Ես Նորավանի բոտն եմ և կօգնեմ Ձեզ տեղեկություն ստանալ Ձեր սեփականության ընթացիկ պարտքի կամ կանխավճարի մասին։ Հուսով եմ պարտք չէ, կանխավճար է :) \nԱյս պահին հասանելի է " + str(current_month_am) + " ամիսը:\n", reply_markup=markup)


        bot.send_message(message.chat.id, text="Դուք գլխավոր մենյուում եք։", reply_markup=markup)



    # select bnakaran part_---------------------------------------bnakaranbnakaranbnakaranbnakaranbnakaranbnakaranbnakaranbnakaranbnakaranbnakaran
    elif (message.text == "Բնակարան"):

        building_you_selected_v2 = get_selection_of_building_from_db_by_teleg_id(message_chat_id, "building")
        print('elif (message.text == "Բնակարան"    get_selection_of_building_from_db_by_teleg_id(message_chat_id, "building") = ', building_you_selected_v2  )
        # this is already slected before - > building_you_selected
        # this is already slected beforesettings.selected_worksheet_is = 0

        bot.send_message(message.chat.id,
                         text=str(building_you_selected_v2[5:]) + " շենքի ձեր բնակարանի համարը մուտքագրեք, խնդրում եմ։")
        print("i will call fuction to get how much you should pay")
        print(building_you_selected_v2)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # btn1 = types.KeyboardButton("no need")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
        markup.add(back)
        # bot.send_message(message.chat.id, text=" you may request another 'flat' within" + building_you_selected + "  or press button and go to home page ", reply_markup=markup)
        # settings.nkugh_parking_flat = "flat"

        update_selection_of_F_N_P_to_db(current_user_id_text, "f_n_p", "flat")

        print( " in message.text ==  Բնակարան i just called  update_selection_of_F_N_P_to_db(teleg_id, f_n_p,  flat ) ")

    # select Nkugh part_ՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղ
    elif (message.text == "Նկուղ"):

        building_you_selected_v2 = get_selection_of_building_from_db_by_teleg_id(message_chat_id, "building")
        print('elif (message.text == "Նկուղ"    get_selection_of_building_from_db_by_teleg_id(message_chat_id, "building") = ', building_you_selected_v2  )

        # this is already slected before - > building_you_selected
        # this is already slected before settings.selected_worksheet_is = 0

        # Text_to_send_to_bot = str(building_you_selected) + str(settings.selected_worksheet_is)

        # settings.nkugh_parking_flat = "nkugh"

        update_selection_of_F_N_P_to_db(current_user_id_text, "f_n_p", "nkugh")

        print( " in message.text ==  Բնակարան i just called  update_selection_of_F_N_P_to_db(teleg_id, f_n_p,  nkugh ) ")




        # bot.send_message(message.chat.id, text="ok, " + str(building_you_selected[5:]) + ' ' + str(
            # settings.selected_worksheet_is) + "  ->  i will need your nkugh Համար    please ")

        bot.send_message(message.chat.id, text= str(building_you_selected_v2[5:]) + " շենքի ձեր նկուղի համարը մուտքագրեք, խնդրում եմ: ")



        print("message.text == Նկուղ ")
        print(building_you_selected_v2)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # btn1 = types.KeyboardButton("no need")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
        markup.add(back)
        # bot.send_message(message.chat.id, text=" you may request another 'flat' within" + building_you_selected + "  or press button and go to home page ", reply_markup=markup)


    elif (message.text == "Կայանատեղի"):

        building_you_selected_v2 = get_selection_of_building_from_db_by_teleg_id(message_chat_id, "building")
        print('elif (message.text == "Կայանատեղի"    get_selection_of_building_from_db_by_teleg_id(message_chat_id, "building") = ', building_you_selected_v2  )

        # this is already slected before - > building_you_selected
        # this is already slected before settings.selected_worksheet_is = 0

        # Text_to_send_to_bot = str(building_you_selected) + str(settings.selected_worksheet_is)

        # settings.nkugh_parking_flat = "parking"

        update_selection_of_F_N_P_to_db(current_user_id_text, "f_n_p", "parking")


        print( " in message.text ==  Բնակարան i just called  update_selection_of_F_N_P_to_db(teleg_id, f_n_p,  parking ) ")

        tempppp  = get_selection_of_building_from_db_by_teleg_id(message_chat_id, "f_n_p")

        print ("get_selection_of_building_from_db_by_teleg_id(message_chat_id, 'f_n_p')" +  str(tempppp))

        bot.send_message(message.chat.id, text = str(building_you_selected_v2[6:]) + " շենքի ձեր կայանատեղիի  համարը մուտքագրեք, խնդրում եմ։ " )

        print(" this is elif section with message.text == Կայանատեղի   ")
        print(building_you_selected_v2)
        # print(settings.nkugh_parking_flat)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # btn1 = types.KeyboardButton("no need")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
        markup.add(back)
        # bot.send_message(message.chat.id, text=" you may request another 'flat' within" + building_you_selected + "  or press button and go to home page ", reply_markup=markup)



    elif (message.text == "number "):
        print("not yet defeinted")

    # building_you_selected = "Avan4 55/17"  # this to set some defsault value to initialize it -

    # bot.send_message(message.chat.id,
    #                  text="ok, ->  i will need Code number it shoild match  ~ format S-5534-107 or P-5534-26")
    # print("i will call fuction to Find S or P by code")
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # # btn1 = types.KeyboardButton("no need")
    # back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
    # markup.add(back)








    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
        markup.add(back)
        bot.send_message(message.chat.id,
                         text="Ներեցեք, չեմ հասկանում ինչ հարցում եք կատարում։ Մուտքագրեք խնդրում եմ բնակարանի/նկուղի/կայանտեղիի համարը 1-280 միջակայքում։ Խնդրում եմ կրկին փորձեք",
                         reply_markup=markup)


# if __name__ == '__main__':
#     bot.polling(none_stop=True)

try:

    bot.polling(none_stop=True)

# ConnectionError and ReadTimeout because of possible timout of the requests library

# TypeError for moviepy errors

# maybe there are others, therefore Exception

except Exception as e:
    logger.error(e)

    time.sleep(20)







# gs = gspread.service_account(filename='credentials.json')  # подключаем файл с ключами и пр.
# sh = gs.open_by_key('1w2wOpN5CCX5Xhlrqbm5e6eJWDXMchb-30j5EzvyxJBQ')  # подключаем таблицу по ID
# # worksheet = sh.sheet1  # получаем первый лист

# Avan_list_Adress = [17, 20, 3, 33, 34]
# exist_count = 99 #some initial value

# #we will ask to enter proper values till user realize that there is no other way
# def func_if_entered_data_is_correct(validate_adress):
#     global exist_count
#     x = True
#     if validate_adress in Avan_list_Adress:
#         exist_count = Avan_list_Adress.index(validate_adress)
#         print(exist_count)
#     else:
#         x = False
#         print("please enter proper values")
#     return x

# def func_if_entered_data_is_correct2(flat_number):
#     x = True
#     if flat_number < 281:
#       x = True
#     else:
#         x = False
#         print("please enter proper values")
#     return x


# # print(func_if_entered_data_is_correct(25))
# # print(func_if_entered_data_is_correct(122))
# # print(func_if_entered_data_is_correct2(400))
# # print(func_if_entered_data_is_correct2(0))

# col_where_it_was_found = 0

# ##this function will return array with row where code was found
# def Find_Code_By_address(kotorak, bnak_hamar):
#     global col_where_it_was_found
#     Cell_To_Find = "A-55" + str(kotorak) + "-" + str(bnak_hamar)
#     print(Cell_To_Find)
#     cell_list = wks.find(Cell_To_Find)  # find cell with given code number
#     values_list = wks.row_values(cell_list.row)  # get whole row with "given code" that found what row is this
#     col_where_it_was_found = cell_list.col
#     print(cell_list.row)
#     print(values_list)
#     return values_list

# # ----------

# # cell_list = wks.find("A-5520-27")
# # print("Found something at Row % s Column % s" % (cell_list.row, cell_list.col))

# # enter data ->
# print('what address are you interested in 55 /xx , it should be one of 17, 20, 3, 33, 34 ?')
# AddressToFind = int(input())
# func_if_entered_data_is_correct(AddressToFind) # validate inside fucntion if data is ok
# print('what flat  are you interested in 55 / ' + str(AddressToFind) + ' ? ')
# FlatToFind = int(input())
# func_if_entered_data_is_correct2(FlatToFind) # validate inside fucntion if data is ok
# #assuming data is good: exist_count = Avan_list_Adress.index(validate_adress) is showing proper worksheet

# print(exist_count)
# wks = sh.get_worksheet(exist_count)
# x = []
# x = Find_Code_By_address(AddressToFind, FlatToFind)


# print(col_where_it_was_found)
# print ("You have to pay my friend: ")
# print(x[col_where_it_was_found])


# if AddressToFind in Avan_list_Adress:
#     exist_count = Avan_list_Adress.index(AddressToFind)
#     print ("ok")
# else:
#     print("no such address, it should be one of -> 17, 20, 3, 33, 34 ")
#
# if FlatToFind < 281:
#     print ("ok - flat should be less than 280")
# else:
#     print("no such flat exist , it should be between 1 and 280 ")

# element exists in list
# exist_count = Avan_list_Adress.index(AddressToFind)
# print(str(exist_count)+"exist_count")

# # checking if it is more than 0
# if exist_count >= 0:
#     print("Yes,  exists in list")
# else:
#     print("No,  does not exists in list")


# get_code_of adress to validate


#
#
# # worksheet2 = sh.worksheet(self, "Avan 4 ParkingNkugh")
# # sh.worksheet()
#
# res = wks.get_all_records()  # считываем все записи (массив: ключ-значение)
# # res = worksheet.get_all_values()  # считываем все значения
# res2 = worksheet.row_values(1)  # получаем первую строчку таблицы
# res3 = worksheet.col_values(1)  # получаем первую колонку таблицы
# res4 = worksheet.get('A2')  # получаем заданную ячейку
# res5 = worksheet.get('A2:C2')  # получаем заданный диапазон
#
# print(res)  # выводим в консоль
#
# print(res2)  # выводим в консоль
#
# print(res3)  # выводим в консоль
#
# print(res4)  # выводим в консоль
#
# print(res5)  # выводим в консоль
#
#
#
