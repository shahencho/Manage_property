import settings
import gspread  # импорти библиотеку

from workwithdb import *

gs = gspread.service_account(filename='credentials.json')  # подключаем файл с ключами и пр.
sh = gs.open_by_key('1w2wOpN5CCX5Xhlrqbm5e6eJWDXMchb-30j5EzvyxJBQ')  # подключаем таблицу по ID



def Find_Dept_By_Code(requested_str, telegram_id):
    # example "S-553-71"  or "P-5520-43" max - S-5534-107 S-5520-224
    # parking max P-5520-48 , so 48   / P-5534-26 , so 26

    final_duty_to_be_paid_for_P_S = "myundefined"

    requested_str = str(requested_str)
    print(requested_str)

    worksheet_based_on_requested_str = Realize_worksheet(requested_str)

    print ("Realize_worksheet(requested_str) " + str(worksheet_based_on_requested_str))


    # parking_str =
    len_requested_str = len(requested_str)
    print("Length is" + str(len_requested_str) )


    try:
        if len_requested_str >= 7 and len_requested_str <= 12:
            print("this is for len_requested_str >= 7 and len_requested_str <= 12 " )
            if requested_str[0]=="S" or requested_str[0]=="P" or requested_str[0]=="s" or requested_str[0]=="p":
                print("..we will find S in both sheets")
                # try to find in "Avan 4 ParkingNkugh" - it's 1
                # wks = sh.get_worksheet(1)
                wks = sh.get_worksheet(worksheet_based_on_requested_str)

                cell_list = wks.find(requested_str)  # find cell with given code number
                print(str(cell_list)+" Print cell list ")

                if cell_list is None:
                    print(str(cell_list)+"Print cell list was not found on worksheet 1 , looking on work 3  ")
                    #try the same with another worksheet Avan 6 ParkingNkugh it's 3
                    wks = sh.get_worksheet(3)

                    cell_list = wks.find(requested_str)  # find cell with given code number
                    print(str(type(cell_list)) + " str(type(cell_list)) ")
                    print (cell_list)
                    if cell_list is None:
                        print("we r not able to find it in both worksheer 1 and 3 - so - > format was correct, however there is no such code .")
                        print("there is no such 'Code'  , please try again with format : format S-5534-107 or P-5534-26")
                    else:
                        print("Print cell list was  found on  worksheet(3) uyuyyuuuuuuuuuuuy ")

                        #requested_str - save to db by teleg id
                        temp333 = update_selection_of_F_N_P_to_db(telegram_id, "bill_code", requested_str)
                        print (""" Print cell list was  found on  worksheet(3) uyuyyuuuuuuuuuuuy  - > update_selection_of_F_N_P_to_db(telegram_id, "bill_code", requested_str)   """ + str(temp333))

                        # since we for sure know that cell was found - we should get "Ստատուս" and count -1

                        values_list = wks.row_values(cell_list.row)  # get whole row with "given code" that found what row is this
                        col_where_it_was_found = cell_list.col

                        print(cell_list.row)
                        print(values_list)
                        print(values_list[col_where_it_was_found])

                        # find ամսավճար cell and get column , so when required duty will be calculated we will do (column_where_amsvachar_column_is -1)
                        find_cell_amsavchar="Ստատուս"
                        cell_amsavchar = wks.find(find_cell_amsavchar)
                        # new_list = wks.row_values(cell_amsavchar.row)  # get whole row with "given code" that found what row is this
                        column_where_amsvachar_column_is = cell_amsavchar.col
                        print(f"{column_where_amsvachar_column_is} value of column_where_amsvachar_column_is " )

                        final_duty_to_be_paid_for_P_S = values_list[column_where_amsvachar_column_is-2]

                        print("final_duty_to_be_paid_for_P_S = --------------------------0" + str(final_duty_to_be_paid_for_P_S))
                        print(type(final_duty_to_be_paid_for_P_S))




                         # res4 = worksheet.get('A2')  # получаем заданную ячейку
                        val11 = wks.cell(1, column_where_amsvachar_column_is-1).value

                        last_month_available_in_ggogle_doc = val11[6:]

                        print("val = wks.cell(1, column_where_amsvachar_column_is-1).value aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa               " + str(last_month_available_in_ggogle_doc ))

                else:
                    print("We  find it yuhuuuuuuuuuuuuuuuuuuuuuuuuuu  in  worksheet 1 .")

                    temp2211 = update_selection_of_F_N_P_to_db(telegram_id, "bill_code", requested_str)
                    print (""" We  find it yuhuuuuuuuuuuuuuuuuuuuuuuuuuu  in  worksheet 1 - > update_selection_of_F_N_P_to_db(telegram_id, "bill_code", requested_str)   """ + str(temp2211))


                    # settings.cell_for_parking = cell_list

                    # since we for sure know that cell was found - we should get "Ստատուս" and count -1

                    values_list = wks.row_values(cell_list.row)  # get whole row with "given code" that found what row is this
                    col_where_it_was_found = cell_list.col

                    print(cell_list.row)
                    print(values_list)
                    print(values_list[col_where_it_was_found])

                    # find Ստատուս cell and get column , so when required duty will be calculated we will do (column_where_amsvachar_column_is -1)
                    find_cell_amsavchar="Ստատուս"
                    cell_amsavchar = wks.find(find_cell_amsavchar)
                    # new_list = wks.row_values(cell_amsavchar.row)  # get whole row with "given code" that found what row is this
                    column_where_amsvachar_column_is = cell_amsavchar.col
                    print(f"{column_where_amsvachar_column_is} value of column_where_amsvachar_column_is " )

                    final_duty_to_be_paid_for_P_S = values_list[column_where_amsvachar_column_is-2]

                    print("final_duty_to_be_paid_for_P_S = " + str(final_duty_to_be_paid_for_P_S))




            elif requested_str[0]=="kkuuu": # remove this check i guess .. .
                print("this was block with if text starts with P or S , so -> we should ask to enter proper code , starting with S or P ")



        else:
            print("Length of your code is not matching , suppose to be 7 - 13 symbols, and  ~ format S-5534-107 or P-5534-26")


    except:

        print("some params inside try was not coreect????????????")

    finally:
        # if x==1:
        #     print("Something went wrong we will consider some params was wrong")
        #     print("let's ask user to unter proper values")
        # else:
        #     print("we are good")

        print("this is block for final ")



    return final_duty_to_be_paid_for_P_S



def test_codes():
    fruits = ["S-5520-223", "P-553-1", "P-5534-26", "S-5534-107","S-5520-224", "S-5520-224","incoorect values-----------------------------------------------00000000000000000000", "s-9932-212","as-3332-212" , "4-3332-2asasa" ]
    for x in fruits:
        print(x + "      ---------")
        print(Find_Dept_By_Code(x))


# print("new fffffffffffffffffffffffffffffffffffffffffffffff======================================")
# test_codes()


def get_month_in_am(month_number):

    thisdict = {
      "01": " Հունվար ",
      "02": " Փերտրվար ",
      "03": "Մարտ",
      "04": "Ապրիլ",
      "05": "Մայիս",
      "06": "Հունիս",
      "07": "Հուլիս",
      "08": "Օգոստոս",
      "09": "Սեպտեմբեր",
      "10": "Հոկտեմբեր",
      "11": "Նոյեմբեր",
      "12": "Դեկտեմբեր"
      }

    # month_number = "Պարտք 31.01.2022"
    # val2  = month_number[9:11]

    last_month_available_in_ggogle_doc = thisdict[str(month_number)]

    print(" last_month_available_in_ggogle_doc = thisdict[str(month_number)]             " + str(last_month_available_in_ggogle_doc ))

    # so - we will have last_month_available_in_ggogle_doc during whole story


    return last_month_available_in_ggogle_doc

    # example "S-553-71"  or "P-5520-43" max - S-5534-107 S-5520-224
    # parking max P-5520-48 , so 48   / P-5534-26 , so 26

def Realize_worksheet (requested_string):
    temp = requested_string [2:6]
    print(temp)

    if temp == "5520" or temp == "5517":
        work_sh = 1
    elif temp == "5533" or temp == "5534" or temp == "553-":
        work_sh = 3
    else:
        work_sh = 99

    return work_sh


def Realize_worksheet_by_building (requested_string):
    temp1 = requested_string [6:]
    print(temp1)

    if temp1 == "55/20" or temp1 == "55/17":
        work_sh = 0
    elif temp1 == "55/33" or temp1 == "55/34" or temp1 == "55/3":
        work_sh = 2
    else:
        work_sh = 99

    return work_sh



    # example "S-553-71"  or "P-5520-43" max - S-5534-107 S-5520-224
    # parking max P-5520-48 , so 48   / P-5534-26 , so 26




    # Find_Dept_By_Code("S-5534-1079999999999")


    # wks = sh.get_worksheet(worksheet_sequence)
    # global col_where_it_was_found
    # # global Cell_To_Find
    # settings.Cell_To_Find = "A-55" + str(kotorak) + "-" + str(bnak_hamar)
    # print(settings.Cell_To_Find)
    # cell_list = wks.find(settings.Cell_To_Find)  # find cell with given code number
    # values_list = wks.row_values(cell_list.row)  # get whole row with "given code" that found what row is this
    # col_where_it_was_found = cell_list.col

    # print(cell_list.row)
    # print(values_list)
    # print(values_list[col_where_it_was_found])

    # # find ամսավճար cell and get column , so when required duty will be calculated we will do (column_where_amsvachar_column_is -1)
    # find_cell="ամսավճար"
    # cell_amsavchar = wks.find(find_cell)
    # # new_list = wks.row_values(cell_amsavchar.row)  # get whole row with "given code" that found what row is this
    # column_where_amsvachar_column_is = cell_amsavchar.col

    # print(f"{column_where_amsvachar_column_is} value of column_where_amsvachar_column_is " )

    # final_duty_to_be_paid = values_list[column_where_amsvachar_column_is-2]

    # settings.last_kotorak_value = kotorak
    # settings.last_bnak_hamar = bnak_hamar
    # settings.last_worksheet_sequence = worksheet_sequence


    # print(final_duty_to_be_paid)




    # return final_duty_to_be_paid








# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('kuku')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
