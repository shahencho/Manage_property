# import asyncio

# async def check_new_offers_loop():
#     while True:
#         await check_new_offers()
#         await asyncio.sleep(10)
# async def check_new_offers():
#     user_selections_sheet = sh.worksheet("User_Selections_Sheet")
#     user_selections_list = user_selections_sheet.get_all_records()
#     for user in user_selections_list:
#         telegram_id = user['telegram_id']
#         country = user['country']
#         nights = user['nights']
#         date_range = user['date_range']
#         query = f"country='{country}' and nights={nights} and date_range='{date_range}'"
#         offers_sheet = sh.worksheet("Sheet1")
#         offers_list = offers_sheet.get_all_records()
#         new_offers = [offer for offer in offers_list if eval(query)]
#         if new_offers:
#             text = "New offers found:\n"
#             for offer in new_offers:
#                 text += f"{offer['Agency_Name']} - {offer['Hotel_Name']} - {offer['Total_Price']} - {offer['Available_Dates_To_Fly']}\n"
            
#             app = ApplicationBuilder().token(TOKEN).build()
#             await app.bot.send_message(chat_id=telegram_id, text=text)


# check_new_offers.start()

 