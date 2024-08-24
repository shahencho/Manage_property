token = '5559119243:AAH8F74c7N8qZ75R08QyrI7H8_DgcfCwSsU' #@duty55_bot



# AM version

import gspread  # импорти библиотеку
import telebot
import time

# import pyTelegramBotAPI

from telebot import types  # для указание типов
from workwithdb import *
from workwithdb import if_user_is_new
from Find_Dept_By_Code import Find_Dept_By_Code
from Find_Dept_By_Code  import get_month_in_am

import settings

import logging

logger = logging.getLogger('logger')

time.sleep(1)

print("time.sleep(1)")

# time.sleep(20)



# add_new_user_to_db(4544, "A-5")
# update_new_user_to_db(4544,"A-444-444" )

# print(Find_Dept_By_Code("P-5534-22"))

# print(Find_Dept_By_Code("P-5534-22091"))


token = '5559119243:AAH8F74c7N8qZ75R08QyrI7H8_DgcfCwSsU' #@duty55_bot
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
current_month_am = get_month_in_am(get_month_by_number)

#endof last_month_available_in_ggogle_doc



# worksheet = sh.sheet1  # получаем первый лист
Avan_list_Adress = [17, 20, 3, 33, 34]
exist_count = 99  # some initial value
someParam = True
col_where_it_was_found = 0


# Cell_To_Find = "undefined In Hlyoubot"

##this function will return array with row where code was found
def Find_Code_By_address(kotorak, bnak_hamar, worksheet_sequence):
    wks = sh.get_worksheet(worksheet_sequence)
    global col_where_it_was_found
    # global Cell_To_Find
    if worksheet_sequence == 0 or worksheet_sequence == 2:
        settings.Cell_To_Find = "A-55" + str(kotorak) + "-" + str(bnak_hamar)
    elif worksheet_sequence == 1 or worksheet_sequence == 3:
        print("nkuhg or kayanateghi")
        if settings.nkugh_parking_flat == "nkugh":
            settings.Cell_To_Find = "S-55" + str(kotorak) + "-" + str(bnak_hamar)
        elif settings.nkugh_parking_flat == "parking":
            settings.Cell_To_Find = "P-55" + str(kotorak) + "-" + str(bnak_hamar)

    print(settings.Cell_To_Find)
    cell_list = wks.find(settings.Cell_To_Find)  # find cell with given code number
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

    settings.last_kotorak_value = kotorak
    settings.last_bnak_hamar = bnak_hamar
    settings.last_worksheet_sequence = worksheet_sequence

    print(final_duty_to_be_paid)

    return final_duty_to_be_paid


# Find_Code_By_address(20,10,0 )

# default values.

building_you_selected = "uknown"


@bot.message_handler(commands=['start'])
def start(message):
    global current_user_id
    # global Cell_To_Find
    current_user_id = message.chat.id
    first_name_of_current_user = message.chat.first_name

    print(message.chat.first_name)
    print(message.chat.last_name)
    print(message.chat.id)

    print("building_you_selected = " + str(building_you_selected))

    if if_user_is_new(current_user_id):
        add_new_user_to_db(current_user_id, "New user to db called during start  ")

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("55/17")
        btn2 = types.KeyboardButton("55/20")
        btn_Avan6_1 = types.KeyboardButton("55/3")
        btn_Avan6_2 = types.KeyboardButton("55/33")
        btn_Avan6_3 = types.KeyboardButton("55/34")
        # btn_find_code_s_p = types.KeyboardButton("Find S or P by code")

        markup.add(btn1, btn2, btn_Avan6_1, btn_Avan6_2, btn_Avan6_3)



        msg = bot.send_message(message.chat.id,
                         text="Ողջույն, {0.first_name}:  Ես Նորավանի բոտն եմ և կօգնեմ Ձեզ տեղեկություն ստանալ Ձեր սեփականության ընթացիկ պարտքի կամ կանխավճարի մասին։ Հուսով եմ պարտք չէ, կանխավճար է :) \n Այս պահին հասանելի է [" + str(current_month_am) + "] ամիսը:\n", reply_markup=markup)

        # bot.register_next_step_handler(msg, compile_text)


    else:
        print("aaaaa Cell to find ixxxx")
        print(settings.Cell_To_Find)
        # update_new_user_to_db(current_user_id, "A-5517-253 ") #we don't need this row

        # text_to_send_registered_user = "Ողջույն, {}!\n Դուք օգտվել եք այս համակարգից և ես ձեզ հիշում եմ, վերջին անգամ դուք հետաքրքված էիք հետևյալով {} :) \n"
        text_to_send_registered_user = "Ողջույն, {}!\n Դուք օգտվել եք այս համակարգից և ես ձեզ հիշում եմ, վերջին անգամ դուք հետաքրքված էիք հետևյալով {} :) \n Այս պահին հասանելի է [" + str(current_month_am) + "] ամիսը: \n"

        text_to_send_registered_user = text_to_send_registered_user.format(first_name_of_current_user,
                                                                           settings.Cell_To_Find)




        # bot.send_message(message.chat.id, text = text_to_send_registered_user, reply_markup=markup)

        text_to_print = str(
            text_to_send_registered_user) + " Խնդրում եմ ընտրեք ինչ եք ցանկանում անել, սեղմեք  ՛Այո, այդ ես եմ՛ եթե ցանկանում եք տեսնել   " + str(
            settings.Cell_To_Find) + " կամ սեղմեք ՚Վերադարձ գլխավոր մենյու՛ եթե ցանկանում եք այլ որոնում իրականցել"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        correct_button = types.KeyboardButton("Այո, այդ ես եմ")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
        markup.add(correct_button, back)
        bot.send_message(message.chat.id, text=text_to_print, reply_markup=markup)
        msg = bot.send_message(message.chat.id,
        text="Ողջույն, {0.first_name}:  Ես Նորավանի բոտն եմ և կօգնեմ Ձեզ տեղեկություն ստանալ Ձեր սեփականության ընթացիկ պարտքի կամ կանխավճարի մասին։ Հուսով եմ պարտք չէ, կանխավճար է :) \n Այս պահին հասանելի է [" + str(current_month_am) + "] ամիսը:\n", reply_markup=markup)

        # bot.register_next_step_handler(msg, compile_text)


def compile_text(message):
    e = message.text
    print(e)
    bot.send_message(message.chat.id, "fffffyyyuuck")
    print ( " we are now in def compile_text(message): fuunction" )




@bot.message_handler(content_types=['text'])
def func(message):
    global building_you_selected

    print("building_you_selected = " + str(building_you_selected))

    print("settings.selected_worksheet_is = " + str(settings.selected_worksheet_is))

    print ("last_kotorak_value =  " + str(settings.last_kotorak_value) )
    print ("last_bnak_hamar = " + str(settings.last_bnak_hamar))


    global dutytopay
    # selected_worksheet_is = 0  #by default it will be 0

    dutytopay = 99999999  # some default value
    x = message.text
    # sdsddddddddddddddddddd

    if (message.text == "55/17"):
        building_you_selected = "Avan4 55/17"
        settings.selected_worksheet_is = 0
        # please select what do you want flat/nkukh/parking

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_flat = types.KeyboardButton("Բնակարան")
        btn2_nkugh = types.KeyboardButton("Նկուղ")
        btn3_parking = types.KeyboardButton("Կայանատեղի")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
        markup.add(btn1_flat, btn2_nkugh, btn3_parking, back)

        msg = bot.send_message(message.chat.id, text="Ողջույն, դուք ընտրել եք հետևյալ շենքը  " + str(
            message.text) + ": Ընտրեք խնդրեմ , ինչ եք ցանկանում որոնել սեղմելով համապատասխան կոճակը ",
                         reply_markup=markup)

        print(
            "user should slect  ->btn1_flat or btn2_nkugh btn3_parking , considering that building_you_selected  55/17   was chosen -> building_you_selected = [Avan4 55/17]") #-------------------------------------------------------
        print(building_you_selected)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)


        bot.register_next_step_handler(msg, compile_text)

    elif (message.text == "55/20"):

        building_you_selected = "Avan4 55/20"
        settings.selected_worksheet_is = 0

        # please select what do you want flat/nkukh/parking

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_flat = types.KeyboardButton("Բնակարան")
        btn2_nkugh = types.KeyboardButton("Նկուղ")
        btn3_parking = types.KeyboardButton("Կայանատեղի")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")

        markup.add(btn1_flat, btn2_nkugh, btn3_parking, back)

        bot.send_message(message.chat.id, text=" Ողջույն, դուք ընտրել եք հետևյալ շենքը  " + str(
            message.text) + " Ընտրեք խնդրեմ , ինչ եք ցանկանում որոնել սեղմելով համապատասխան կոճակը ",
                         reply_markup=markup)

        print(
            "user should slect  ->btn1_flat or btn2_nkugh btn3_parking , considering that building_you_selected  55/20   was chosen - > -> building_you_selected = [Avan4 55/20]")
        print(building_you_selected)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # ====Avan6 worksheet 2 -------------------------------------------------
    elif (message.text == "55/33"):
        building_you_selected = "Avan6 55/33"
        settings.selected_worksheet_is = 2

        # please select what do you want flat/nkukh/parking

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_flat = types.KeyboardButton("Բնակարան")
        btn2_nkugh = types.KeyboardButton("Նկուղ")
        btn3_parking = types.KeyboardButton("Կայանատեղի")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")

        markup.add(btn1_flat, btn2_nkugh, btn3_parking, back)

        bot.send_message(message.chat.id, text="Ողջույն, դուք ընտրել եք հետևյալ շենքը  " + str(
            message.text) + " Ընտրեք խնդրեմ , ինչ եք ցանկանում որոնել սեղմելով համապատասխան կոճակը ",
                         reply_markup=markup)

        print(
            "user should slect  ->btn1_flat or btn2_nkugh btn3_parking , considering that building_you_selected  Avan6 55/33   was chosen-> -> building_you_selected = [Avan4 55/33]")
        print(building_you_selected)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)



    elif (message.text == "55/3"):
        building_you_selected = "Avan6 55/3"
        settings.selected_worksheet_is = 2

        # please select what do you want flat/nkukh/parking

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_flat = types.KeyboardButton("Բնակարան")
        btn2_nkugh = types.KeyboardButton("Նկուղ")
        btn3_parking = types.KeyboardButton("Կայանատեղի")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")

        markup.add(btn1_flat, btn2_nkugh, btn3_parking, back)

        bot.send_message(message.chat.id, text="Ողջույն, դուք ընտրել եք հետևյալ շենքը  " + str(
            message.text) + " Ընտրեք խնդրեմ , ինչ եք ցանկանում որոնել սեղմելով համապատասխան կոճակը ",
                         reply_markup=markup)

        print(
            "user should slect  ->btn1_flat or btn2_nkugh btn3_parking , considering that building_you_selected  Avan6 55/3   was chosen - > -> building_you_selected = [Avan4 55/3]")
        print(building_you_selected)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)


    elif (message.text == "55/34"):
        building_you_selected = "Avan4 55/34"
        settings.selected_worksheet_is = 2

        # please select what do you want flat/nkukh/parking

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_flat = types.KeyboardButton("Բնակարան")
        btn2_nkugh = types.KeyboardButton("Նկուղ")
        btn3_parking = types.KeyboardButton("Կայանատեղի")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")

        markup.add(btn1_flat, btn2_nkugh, btn3_parking, back)

        bot.send_message(message.chat.id, text="Ողջույն, դուք ընտրել եք հետևյալ շենքը  " + str(
            message.text) + " Ընտրեք խնդրեմ , ինչ եք ցանկանում որոնել սեղմելով համապատասխան կոճակը ",
                         reply_markup=markup)

        print(
            "user should slect  ->btn1_flat or btn2_nkugh btn3_parking , considering that building_you_selected  Avan6 55/34   was chosen -> building_you_selected = [Avan4 55/34]")
        print(building_you_selected)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)




    elif (message.text == "Find S or P by code"):

        building_you_selected = "Avan4 55/17"  # this to set some defsault value to initialize it -

        bot.send_message(message.chat.id,
                         text="ok, ->  i will need Code number it shoild match  ~ format S-5534-107 or P-5534-26")
        print("i will call fuction to Find S or P by code")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        # btn1 = types.KeyboardButton("no need")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
        markup.add(back)

    elif (x.startswith("S") or x.startswith("P")):
        temp_val = Find_Dept_By_Code(x)
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
    elif (x.isnumeric() == True) and settings.nkugh_parking_flat == "flat":
        print("numeric")

        if int(x) < 281 and (
                int(x) >= 1):  # and building_you_selected : to be ADDDDDDDDDDDDDDDDDDEDDDDDDDDDDDDDDDDDDDDDDDDDDD
            # "Avan4 55/20" --- Avan6 55/3 ---Avan6 55/33 Avan6 55/34
            x = int(x)

            if settings.selected_worksheet_is == 0:
                get_kototak_from_selection = building_you_selected[9:11]
                if (int(get_kototak_from_selection) == 17 or int(get_kototak_from_selection) == 20):
                    dutytopay = Find_Code_By_address(get_kototak_from_selection, x, settings.selected_worksheet_is)
                    # ins_data_to_db(get_kototak_from_selection , flat_number, config.selected_worksheet_is ,     -- this supposed to be flat_number
                    #  e.g. Cell_To_Find  A-5517-34
                    update_new_user_to_db(current_user_id, settings.Cell_To_Find)
                    print(" update db row with update_new_user_to_db(current_user_id, Cell_To_Find) ")
                    print(current_user_id)
                    print(settings.Cell_To_Find)


                elif int(get_kototak_from_selection) == 20:
                    if x == 187 or x == 188:
                        print("plz correct that row for 20 flat 187/188")
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        # btn1 = types.KeyboardButton("no need")
                        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
                        markup.add(back)
                        bot.send_message(message.chat.id,
                                         text=" Դուք կարող եք ճշտել այլ բնակարանի պարտք   {" + building_you_selected[6:] + "}  շենքում կամ կարող եք վերադառնալ գլխավոր մենյու՝ սեղմելով համապատասխան կոճակը։ 55/20 շենքում այլ բնակարան ճշտելու համար մուտքագրեք բնակարանի համարը։ ",
                                         reply_markup=markup)

                    else:
                        dutytopay = Find_Code_By_address(get_kototak_from_selection, x, settings.selected_worksheet_is)

                else:
                    print("get_kototak_from_selection suppose to be 17 or 20 for worksheet 0, error - > ")

            elif settings.selected_worksheet_is == 2 and len(
                    building_you_selected) == 11 and x < 71:  # "Avan4 55/20" --- Avan6 55/3 ---Avan6 55/33 Avan6 55/34
                get_kototak_from_selection = building_you_selected[9:11]
                if (int(get_kototak_from_selection) == 33):  # --------------> building selection was 33
                    dutytopay = Find_Code_By_address(get_kototak_from_selection, x, settings.selected_worksheet_is)
                    update_new_user_to_db(current_user_id, settings.Cell_To_Find)

                elif int(get_kototak_from_selection) == 34:  # --------------> building selection was 34
                    dutytopay = Find_Code_By_address(get_kototak_from_selection, x, settings.selected_worksheet_is)
                    update_new_user_to_db(current_user_id, settings.Cell_To_Find)

            elif settings.selected_worksheet_is == 2 and len(
                    building_you_selected) == 10 and x < 71:  # "Avan4 55/20" --- Avan6 55/3 ---Avan6 55/33 Avan6 55/34
                get_kototak_from_selection = building_you_selected[9:10]
                if (int(get_kototak_from_selection) == 3):  # building selection was 3
                    dutytopay = Find_Code_By_address(get_kototak_from_selection, x, settings.selected_worksheet_is)
                    update_new_user_to_db(current_user_id, settings.Cell_To_Find)


            else:
                # this means dutytopay = 99999999 means it was not yet intialiized , so we need to skip block below.
                print("flat is not in range , error - > need to debug maybe? ")
                print(building_you_selected)
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
                print(building_you_selected)
                # bot.send_message(message.chat.id, text="for this flat you must pay .")
                text_to_print = " Հարգելի սեփականատեր,  {} շենքի  {}  "
                temp_text = "uknownnnn"
                temp_text = text_to_print.format(building_you_selected, int(x))

                print("type(dutytopay) ------------ ")
                print(type(dutytopay))
                if dutytopay.startswith("-"):  # " means we with minus at the beginning,

                    text_to_print = " Հարգելի սեփականատեր, Դուք ցավոք պարտք ունեք :(\n   {} շենքի  {}  "
                    temp_text = "uknownnnn"
                    temp_text = text_to_print.format(building_you_selected[6:], int(x))

                    bot.send_message(message.chat.id, text=(temp_text + "բնակարանի պարտքը կազմում է` "))
                    bot.send_message(message.chat.id, text=dutytopay)

                    txt1 = """ Խնդրում եմ շուտափույտ մարել պարտքը հետևյալ ռեկվիզիտներով՝
Բանկային հաշվեհամար՝ 220563350051000 AMD ACBA Bank
Ստացող՝ «Նորավան» ՀՄՏ
Վճարում կատարելիս նպատակը դաշտում նշել տվյալ գույքի(բնակարան, կայանատեղի, նկուղ) կոդը: Օրինակ՝ «A-5520-6» կամ «P-5520-2» կամ «S-5520-212»։
Կամ EasyPay և FastShift տերմինալներով։
Ձեր վճարման կոդն է՝
"""

                    bot.send_message(message.chat.id, text=txt1)
                    bot.send_message(message.chat.id, text=str(settings.Cell_To_Find))
                    bot.send_message(message.chat.id, text="Շնորհակալություն։")



                else:
                    bot.send_message(message.chat.id,
                                     text=(
                                                 temp_text + " բնակարանի համար դուք ունեք կանխավճար, որի համար Նորավան համատիրությունը Ձեզ հոգաչափ շնորհակալ է և հպարտանում է Ձեզանով։ Ձեր կանխավճարը կազմում է՝"))
                    bot.send_message(message.chat.id, text=dutytopay)

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
                markup.add(back)
                bot.send_message(message.chat.id,
                                 text=" Դուք կարող եք ճշտել այլ բնակարանի պարտք {" + building_you_selected[6:] + "}  շենքում կամ կարող եք վերադառնալ գլխավոր մենյու՝ սեղմելով համապատասխան կոճակը: " + building_you_selected[6:] + " շենքում այլ բնակարան ճշտելու համար մուտքագրեք բնակարանի համարը։ ",
                                 reply_markup=markup)



            else:
                print("dutytopay = 99999999 means it was not yet intialiized ")



        else:
            print("flat is not good ")
            print(building_you_selected)
            text_to_print = "Ներեցեք, չեմ հասկանում ինչ հարցում եք կատարում։ Մուտքագրեք խնդրում եմ բնակարանի համարը 1-280 միջակայքում։ Խնդրում եմ կրկին փորձեք։"
            # temp_text = text_to_print.format(building_you_selected,int(x))
            # bot.send_message(message.chat.id, text = text_to_print)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
            markup.add(back)
            bot.send_message(message.chat.id, text=text_to_print, reply_markup=markup)

    # ------------------------------settings.nkugh_parking_flat == "nkugh":settings.nkugh_parking_flat == "parking"  - if nkugh_parking_flat ==flat it will cover on above IF else , not here, this peace only for nkuga and parking.

    elif (x.isnumeric() == True) and settings.nkugh_parking_flat == "nkugh" and building_you_selected != "uknown" or (
            x.isnumeric() == True) and settings.nkugh_parking_flat == "parking" and building_you_selected != "uknown":
        print("we are in section of nkugh")
        selected_worksheet_for_nkugh_parking = settings.selected_worksheet_is + 1
        # u should continue from here, 000000000000000000000000000000000000000000 find cell by entered Num - > find in selected worksheet - you have that .

        x = int(x)
        if len(building_you_selected) == 10:  # and x>0 and x < 108:   # Avan6 55/3 and not ->  ---Avan6 55/33 Avan6 55/34

            get_kototak_from_selection = building_you_selected[9:10]  # - this suppose to be "3" ALWAYS
            print("get_kototak_from_selection" + str(get_kototak_from_selection))

        elif len(building_you_selected) == 11:  # and x>0 and x < 300:
            get_kototak_from_selection = building_you_selected[9:11]  # - this suppose to be "33"  "20"  ,  "34"
            print("get_kototak_from_selection " + str(get_kototak_from_selection))

        print("building_you_selected " + str(building_you_selected))

        if selected_worksheet_for_nkugh_parking == 1 or selected_worksheet_for_nkugh_parking == 3:
            print("nkuhg or kayanateghi")
            if settings.nkugh_parking_flat == "nkugh":
                settings.Cell_To_Find = "S-55" + str(get_kototak_from_selection) + "-" + str(x)
            elif settings.nkugh_parking_flat == "parking":
                settings.Cell_To_Find = "P-55" + str(get_kototak_from_selection) + "-" + str(x)

        # example "S-553-71"  or "P-5520-43" max - S-5534-107 S-5520-224
        # parking max P-5520-48 , so 48   / P-5534-26 , so 26

        dutytopay = Find_Dept_By_Code(settings.Cell_To_Find)
        print(dutytopay)

        if dutytopay == "myundefined":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
            markup.add(back)
            bot.send_message(message.chat.id,
                             text=" Այդպիսի կոդով նկուղ/կայանատեղի չի գտնվել  {" + building_you_selected[6:] + "} շենքում, , ստուգեք մուտքագրված համարը և կրկին մուտքագրեք կամ կարող եք վերադառնալ գլխավոր մենյու՝ սեղմելով համապատասխան կոճակը ",
                             reply_markup=markup)

        else:
            update_new_user_to_db(current_user_id, settings.Cell_To_Find)
            print("settings.Cell_To_Find " + str(settings.Cell_To_Find))

            # ======================
            print(building_you_selected)
            # bot.send_message(message.chat.id, text="for this flat you must pay .")
            text_to_print = " Հարգելի սեփականատեր, {} շենքի   {} "
            temp_text = "uknownnnn"
            temp_text = text_to_print.format(building_you_selected[6:], int(x))

            print("type(dutytopay) ------------ ")
            print(type(dutytopay))

            tmp_text1 = " " # some empty value .
            if (settings.nkugh_parking_flat == "nkugh"):
                tmp_text1 = "նկուղի"
            elif settings.nkugh_parking_flat == "parking":
                tmp_text1 = "կայանատեղիի"


            if dutytopay.startswith("-"):  # " means we with minus at the beginning,




                bot.send_message(message.chat.id, text=(temp_text + str(tmp_text1) + " համար Դուք ցավոք պարտք ունեք :( \n" + building_you_selected[6:] + " շենքի " + str(x) + " " + str(tmp_text1) + " պարտքը կազմում է "  ))
                bot.send_message(message.chat.id, text=dutytopay)

                txt2_temp = """Խնդրում եմ շուտափույտ մարել պարտքը հետևյալ ռեկվիզիտներով՝
Բանկային հաշվեհամար՝ 220563350051000 AMD ACBA Bank
Ստացող՝ «Նորավան» ՀՄՏ
Վճարում կատարելիս նպատակը դաշտում նշել տվյալ գույքի(բնակարան, կայանատեղի, նկուղ) կոդը: Օրինակ՝ «A-5520-6» կամ «P-5520-2» կամ «S-5520-212»։
Կամ EasyPay և FastShift տերմինալներով։
Ձեր վճարման կոդն է՝
"""
                bot.send_message(message.chat.id, text = txt2_temp)

                bot.send_message(message.chat.id, text = str(settings.Cell_To_Find))

                bot.send_message(message.chat.id, text= " Շնորհակալություն։")

            else:
                bot.send_message(message.chat.id,
                                 text=(temp_text + str(tmp_text1) + " համար Դուք ունեք կանխավճար, որի համար Նորավան համատիրությունը Ձեզ հոգաչափ շնորհակալ է և հպարտանում է Ձեզանով։ Ձեր կանխավճարը կազմում է՝"))
                bot.send_message(message.chat.id, text=dutytopay)


            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
            markup.add(back)
            bot.send_message(message.chat.id,
                             text=" Դուք կարող եք ճշտել այլ " + str(tmp_text1) +  " { " + building_you_selected[6:] + " } շենքում,  մուտքագրեք համարը կամ կարող եք վերադառնալ գլխավոր մենյու՝ սեղմելով համապատասխան կոճակը ",
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
        leng = len(settings.Cell_To_Find)
        if settings.Cell_To_Find[5:6] == "-":  # A-553-2
            print("this is 55/3 shenq")
            get_kotorak = settings.Cell_To_Find[4:5]  # get_kotorak = '3' ; ->>> print("this is 55/3 shenq")
            get_bnak_hamar = settings.Cell_To_Find[6:leng]  # for case with 'A-5517-10 - > 10

        else:
            get_kotorak = settings.Cell_To_Find[4:6]  # for case with 'A-5517-10 - > 17

            get_bnak_hamar = settings.Cell_To_Find[7:leng]  # for case with 'A-5517-10 - > 10

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

        print(" Find_Code_By_address(get_kotorak, get_bnak_hamar, worksheet_sequence): ")

        print(worksheet_sequence)
        dept_for_this_user_in_google_doc = 0  # wwwwwhhhhhhhhhhhhhtFFFFFFFFFFFFFF?

        get_firstletter_of_code = settings.Cell_To_Find[0:1]
        print("get_firstletter_of_code = " + str(get_firstletter_of_code))

        if get_firstletter_of_code == "A":
            dept_for_this_user_in_google_doc = Find_Code_By_address(get_kotorak, get_bnak_hamar, worksheet_sequence)
            dept_for_this_user_in_google_doc = str(dept_for_this_user_in_google_doc)

        elif get_firstletter_of_code == "S" or get_firstletter_of_code == "P":
            dept_for_this_user_in_google_doc = Find_Dept_By_Code(settings.Cell_To_Find)

        if dept_for_this_user_in_google_doc != "99999999":
            print("flat is good")

            building_you_selected = str(get_kotorak)
            print(building_you_selected)




            # bot.send_message(message.chat.id, text="for this flat you must pay .")
            # text_to_print = "Հարգելի սեփականատեր ,  ձեր բալանսը  հետևյալ " + str(settings.Cell_To_Find) +" կոդի համար  կազմում է: "
            text_to_print = "\n Այս պահին հասանելի է [" + str(current_month_am) + "] ամիսը:\n Հարգելի սեփականատեր ,  ձեր բալանսը  հետևյալ " + str(settings.Cell_To_Find) +" կոդի համար  կազմում է: "
            temp_text = "uknownnnn"
            temp_text = text_to_print.format(building_you_selected[6:], int(get_bnak_hamar))

            print("type(dept_for_this_user_in_google_doc) ------------ ")
            print(type(dept_for_this_user_in_google_doc))
            if dept_for_this_user_in_google_doc.startswith("-"):  # " means we with minus at the beginning,
                bot.send_message(message.chat.id, text=(text_to_print + " Դուք ցավոք պարտք ունեք "))
                bot.send_message(message.chat.id, text=dept_for_this_user_in_google_doc)
            else:
                bot.send_message(message.chat.id,
                                 text=(temp_text + "դուք ունեք կանխավճար, որի համար Նորավան համատիրությունը Ձեզ հոգաչափ շնորհակալ է և հպարտանում է Ձեզանով։ Ձեր կանխավճարը կազմում է՝"))
                bot.send_message(message.chat.id, text=dept_for_this_user_in_google_doc)

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
                         text="Ողջույն, "  + str(fname) + "!: Ես Նորավանի բոտն եմ և կօգնեմ Ձեզ տեղեկություն ստանալ Ձեր սեփականության ընթացիկ պարտքի կամ կանխավճարի մասին։ Հուսով եմ պարտք չէ, կանխավճար է :) \n Այս պահին հասանելի է [" + str(current_month_am) + "] ամիսը:\n", reply_markup=markup)


        bot.send_message(message.chat.id, text="Դուք գլխավոր մենյուում եք։", reply_markup=markup)



    # select bnakaran part_---------------------------------------bnakaranbnakaranbnakaranbnakaranbnakaranbnakaranbnakaranbnakaranbnakaranbnakaran
    elif (message.text == "Բնակարան"):
        # this is already slected before - > building_you_selected
        # this is already slected beforesettings.selected_worksheet_is = 0

        bot.send_message(message.chat.id,
                         text=str(building_you_selected[5:]) + " շենքի ձեր բնակարանի համարը մուտքագրեք, խնդրում եմ։")
        print("i will call fuction to get how much you should pay")
        print(building_you_selected)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # btn1 = types.KeyboardButton("no need")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
        markup.add(back)
        # bot.send_message(message.chat.id, text=" you may request another 'flat' within" + building_you_selected + "  or press button and go to home page ", reply_markup=markup)
        settings.nkugh_parking_flat = "flat"

    # select Nkugh part_ՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղՆկուղ
    elif (message.text == "Նկուղ"):
        # this is already slected before - > building_you_selected
        # this is already slected before settings.selected_worksheet_is = 0

        # Text_to_send_to_bot = str(building_you_selected) + str(settings.selected_worksheet_is)

        settings.nkugh_parking_flat = "nkugh"

        # bot.send_message(message.chat.id, text="ok, " + str(building_you_selected[5:]) + ' ' + str(
            # settings.selected_worksheet_is) + "  ->  i will need your nkugh Համար    please ")

        bot.send_message(message.chat.id, text= str(building_you_selected[5:]) + " շենքի ձեր նկուղի  համարը մուտքագրեք, խնդրում եմ: ")



        print("message.text == Նկուղ ")
        print(building_you_selected)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # btn1 = types.KeyboardButton("no need")
        back = types.KeyboardButton("Վերադարձ գլխավոր մենյու")
        markup.add(back)
        # bot.send_message(message.chat.id, text=" you may request another 'flat' within" + building_you_selected + "  or press button and go to home page ", reply_markup=markup)


    elif (message.text == "Կայանատեղի"):
        # this is already slected before - > building_you_selected
        # this is already slected before settings.selected_worksheet_is = 0

        # Text_to_send_to_bot = str(building_you_selected) + str(settings.selected_worksheet_is)

        settings.nkugh_parking_flat = "parking"

        bot.send_message(message.chat.id, text = str(building_you_selected[6:]) + " շենքի ձեր կայանատեղիի  համարը մուտքագրեք, խնդրում եմ։ " )

        print(" this is elif section with message.text == Կայանատեղի   ")
        print(building_you_selected)
        print(settings.nkugh_parking_flat)
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
