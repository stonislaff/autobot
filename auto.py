from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor 
from pymongo import MongoClient 
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import keyboards as kb
from random import randint
from aiogram.types import InputMediaPhoto

bot = Bot(token = '') #bot token
dp = Dispatcher(bot)


#подключение бд:
cluster = MongoClient("")
db = cluster["Autobot_db"]
collection = db["Autobot_coll"]
chat__id = 0;
Adv_coll = db['advrt_coll']
Adm_coll = db['adm_coll']


print("Запущено!")
CheckAdv = ' '
Greeting_message = 'Поздравляем! Вы подписались на КП - Volkswagen - Киев.'


@dp.message_handler()
async def Commands(msg: types.Message):
	admin_id = '204828347'
	chanel_id = '-1002203166433'
	if msg.text == "/start":
		if Adv_coll.count_documents({"_id": msg.from_user.id}) == 0:
			Adv_coll.insert_one({"_id": msg.from_user.id,"City": "0", "Marka": "0", "Model": "0", "Price" : "0", "BirthYear": "0", "EngineSize": "0", "Mileage": "0", "KbPeredach": "0", "Detail" : "0",'Number': ' ' ,"Picture_Name" : []})	

		await bot.send_message(msg.chat.id, Greeting_message ,reply_markup = kb.greet_kb)

		if collection.count_documents({"_id": msg.from_user.id}) == 0:
			collection.insert_one({"_id": msg.from_user.id,"Position": -1})	
		else:
			collection.update_one({"_id": msg.from_user.id}, {"$set" : {"Position": -1}})

	elif msg.text =='Розмістити оголошення 🚗':
		collection.update_one({'_id': msg.from_user.id}, {'$set' : {'Position': 0}})		
		if collection.find_one({'_id': msg.from_user.id})['Position'] == 0:
			await bot.send_message(msg.from_user.id , "Додайте декілька (1-8) фото вашого авто 🖼️",reply_markup = kb.addphoto_kb)

	
	elif msg.text == 'Додати фото ✅' and collection.find_one({'_id': msg.from_user.id})['Position'] != 1:
		await bot.send_message(msg.from_user.id," Додайте, будь ласка, мінімум одне фото, щоб перейти до наступного меню❗")

	elif collection.find_one({'_id': msg.from_user.id})['Position'] == 1:
		await bot.send_message(msg.from_user.id,'Місто 🌆',reply_markup = kb.city_kb)
		collection.update_one({"_id": msg.from_user.id}, {"$set" : {"Position": 666}})	

	elif collection.find_one({'_id': msg.from_user.id})['Position'] == 666:
		SplitedMsg = msg.text.split(' ')
		if SplitedMsg[1] == "і" and SplitedMsg[2] == "область" and len(SplitedMsg) == 3:
				collection.update_one({"_id": msg.from_user.id}, {"$set" : {"Position": 333}})	
				Adv_coll.update_one({'_id': msg.from_user.id}, {'$set' : {'City': msg.text}})
	
	if collection.find_one({'_id': msg.from_user.id})['Position'] == 333:
		await bot.send_message(msg.from_user.id,' Марка авто 🔠',reply_markup = kb.auto_kb)
		collection.update_one({"_id": msg.from_user.id}, {"$set" : {"Position": 2}})		

	elif collection.find_one({'_id': msg.from_user.id})['Position'] == 2:

		if msg.text == "Інші":
			 collection.update_one({"_id": msg.from_user.id}, {"$set" : {"Position": 700}})
			 await bot.send_message(msg.from_user.id, 'Напишіть свою марку авто 🛺',reply_markup = kb.ReplyKeyboardRemove())
		
		else:
			collection.update_one({"_id": msg.from_user.id}, {"$set" : {"Position": 311}})
			Adv_coll.update_one({'_id': msg.from_user.id}, {'$set' : {'Marka': msg.text}})

	elif collection.find_one({'_id': msg.from_user.id})['Position'] == 700:
		Adv_coll.update_one({'_id': msg.from_user.id}, {'$set' : {'Marka': msg.text}})
		collection.update_one({"_id": msg.from_user.id}, {"$set" : {"Position": 311}})


	if collection.find_one({'_id': msg.from_user.id})['Position'] == 311:
		await bot.send_message(msg.from_user.id, 'Напишіть свою модель авто 🛺',reply_markup = kb.ReplyKeyboardRemove())
		collection.update_one({"_id": msg.from_user.id}, {"$set" : {"Position": 312}})

	elif collection.find_one({'_id': msg.from_user.id})['Position'] == 312:
		Adv_coll.update_one({'_id': msg.from_user.id}, {'$set' : {'Model': msg.text}})
		await bot.send_message(msg.from_user.id,'💰Напишіть ціну авто $')
		collection.update_one({"_id": msg.from_user.id}, {"$set" : {"Position": 3}})

	elif collection.find_one({'_id': msg.from_user.id})['Position'] == 3:
		Adv_coll.update_one({'_id': msg.from_user.id}, {'$set' : {'Price': msg.text}})
		await bot.send_message(msg.from_user.id ,'📆Напишіть рік випуску авто')
		collection.update_one({"_id": msg.from_user.id}, {"$set" : {"Position": 5}})

	elif collection.find_one({'_id': msg.from_user.id})['Position'] == 5:
		Adv_coll.update_one({'_id': msg.from_user.id}, {'$set' : {'BirthYear': msg.text}})
		await bot.send_message(msg.from_user.id ,'🎚️ Напишіть об’єм двигуна авто')
		collection.update_one({"_id": msg.from_user.id}, {"$set" : {"Position": 6}})

	elif collection.find_one({'_id': msg.from_user.id})['Position'] == 6:
		Adv_coll.update_one({'_id': msg.from_user.id}, {'$set' : {'EngineSize': msg.text}})
		await bot.send_message(msg.from_user.id ,'🤖 Оберіть коробку передач', reply_markup = kb.per_kb)
		collection.update_one({"_id": msg.from_user.id}, {"$set" : {"Position": 7}})

	elif collection.find_one({'_id': msg.from_user.id})['Position'] == 7:
		Adv_coll.update_one({'_id': msg.from_user.id}, {'$set' : {'KbPeredach': msg.text}})
		await bot.send_message(msg.from_user.id ,'⏳ Напишіть пробіг авто',reply_markup = kb.ReplyKeyboardRemove())
		collection.update_one({"_id": msg.from_user.id}, {"$set" : {"Position": 8}})

	elif collection.find_one({'_id': msg.from_user.id})['Position'] == 8:
		Adv_coll.update_one({'_id': msg.from_user.id}, {'$set' : {'Mileage': msg.text}})
		await bot.send_message(msg.from_user.id ,'✍️ Напишіть деталі про ваше авто')
		collection.update_one({"_id": msg.from_user.id}, {"$set" : {"Position": 9}})

	elif collection.find_one({'_id': msg.from_user.id})['Position'] == 9:
		await bot.send_message(msg.from_user.id ,'☎️Напишіть свій номер телефону')
		Adv_coll.update_one({'_id': msg.from_user.id}, {'$set' : {'Detail': msg.text}})
		collection.update_one({"_id": msg.from_user.id}, {"$set" : {"Position": 10}})

	elif collection.find_one({'_id': msg.from_user.id})['Position'] == 10:
		Adv_coll.update_one({'_id': msg.from_user.id}, {'$set' : {'Number': msg.text}})
		await bot.send_message(msg.from_user.id ,'Готово ✅\nВаше оголошення заповнено\n🆗Згодом ми розмістимо його в нашій групі\n⏱️Дякуємо 🙏')
		Adm_coll.update_one({'_id': 1},{'$addToSet': {'AdvArray': msg.from_user.id}})
		collection.update_one({"_id": msg.from_user.id}, {"$set" : {"Position": -5}})
		await bot.send_message(admin_id,"Заповнена нова форма.✅\nПодивитись відповідь:  /addcar__answer \nВсі відповіді:  /forms")



	async def GetAdv(CheckID,Where):
		Adv_string = '🌆Місто - ' + str(Adv_coll.find_one({'_id': CheckID})['City']) + "\n🔠Марка авто - #"+ str(Adv_coll.find_one({'_id': CheckID})['Marka']) + "\n🛺Модель авто - #" + str(Adv_coll.find_one({'_id': CheckID})['Model']) + "\n💰Ціна $ - " +  str(Adv_coll.find_one({'_id': CheckID})['Price']) + "\n📆 Рік випуску - " + str(Adv_coll.find_one({'_id': CheckID})['BirthYear']) + "\n🎚️ Об'єм двигуна - " + str(Adv_coll.find_one({'_id': CheckID})['EngineSize']) + "\n🤖 Коробка передач - " +  str(Adv_coll.find_one({'_id': CheckID})['KbPeredach']) + "\n⏳ Пробіг - " + str(Adv_coll.find_one({'_id': CheckID})['Mileage']) + "\n✍️ Деталі про авто - " + str(Adv_coll.find_one({'_id': CheckID})['Detail']) + '\n☎️ Номер телефону - ' + str(Adv_coll.find_one({'_id': CheckID})['Number'])	
		if len(Adv_coll.find_one({'_id': CheckID})['Picture_Name']) == 1:
			p1 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][0]
			arr = [{'type': 'photo','media' : p1 , 'caption' : Adv_string}]

			if Where == 'me': 
				await bot.send_media_group(admin_id, arr)
			else :
				await bot.send_media_group(Where, arr)

		elif len(Adv_coll.find_one({'_id': CheckID})['Picture_Name']) == 2:
			p1 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][0]
			p2 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][1]
			arr = [{'type': 'photo','media' : p1 , 'caption' : Adv_string},{'type': 'photo','media' : p2}]
			if Where == 'me': 
				await bot.send_media_group(admin_id, arr)
			else :
				await bot.send_media_group(Where, arr)
		elif len(Adv_coll.find_one({'_id': CheckID})['Picture_Name']) == 3:
			p1 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][0]	
			p2 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][1]
			p3 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][2]
			arr = [{'type': 'photo','media' : p1 , 'caption' : Adv_string},{'type': 'photo','media' : p2},{'type': 'photo','media' : p3}]
			if Where == 'me': 
				await bot.send_media_group(admin_id, arr)
			else :
				await bot.send_media_group(Where, arr)
		elif len(Adv_coll.find_one({'_id': CheckID})['Picture_Name']) == 4:
			p1 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][0]
			p2 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][1]
			p3 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][2]
			p4 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][3]
			arr = [{'type': 'photo','media' : p1 , 'caption' : Adv_string},{'type': 'photo','media' : p2},{'type': 'photo','media' : p3},{'type': 'photo','media' : p4}]
			if Where == 'me': 
				await bot.send_media_group(admin_id, arr)
			else :
				await bot.send_media_group(Where, arr)
		elif len(Adv_coll.find_one({'_id': CheckID})['Picture_Name']) == 5:
			p1 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][0]
			p2 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][1]
			p3 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][2]
			p4 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][3]
			p5 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][4]
			arr = [{'type': 'photo','media' : p1 , 'caption' : Adv_string},{'type': 'photo','media' : p2},{'type': 'photo','media' : p3},{'type': 'photo','media' : p4},{'type': 'photo','media' : p5}]
			if Where == 'me': 
				await bot.send_media_group(admin_id, arr)
			else :
				await bot.send_media_group(Where, arr)

		elif len(Adv_coll.find_one({'_id': CheckID})['Picture_Name']) == 6:
			p1 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][0]
			p2 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][1]
			p3 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][2]
			p4 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][3]
			p5 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][4]
			p6 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][5]
			arr = [{'type': 'photo','media' : p1 , 'caption' : Adv_string},{'type': 'photo','media' : p2},{'type': 'photo','media' : p3},{'type': 'photo','media' : p4},{'type': 'photo','media' : p5},{'type': 'photo','media' : p6}]
			if Where == 'me': 
				await bot.send_media_group(admin_id, arr)
			else :
				await bot.send_media_group(Where, arr)
		elif len(Adv_coll.find_one({'_id': CheckID})['Picture_Name']) == 7:
			p1 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][0]
			p2 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][1]
			p3 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][2]
			p4 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][3]
			p5 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][4]
			p6 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][5]
			p7 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][6]
			arr = [{'type': 'photo','media' : p1 , 'caption' : Adv_string},{'type': 'photo','media' : p2},{'type': 'photo','media' : p3},{'type': 'photo','media' : p4},{'type': 'photo','media' : p5},{'type': 'photo','media' : p6},{'type': 'photo','media' : p7}]
			if Where == 'me': 
				await bot.send_media_group(admin_id, arr)
			else :
				await bot.send_media_group(Where, arr)
		elif len(Adv_coll.find_one({'_id': CheckID})['Picture_Name']) == 8:
			p1 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][0]
			p2 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][1]
			p3 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][2]
			p4 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][3]
			p5 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][4]
			p6 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][5]
			p7 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][6]
			p8 = Adv_coll.find_one({'_id': CheckID})['Picture_Name'][7]
			arr = [{'type': 'photo','media' : p1 , 'caption' : Adv_string},{'type': 'photo','media' : p2},{'type': 'photo','media' : p3},{'type': 'photo','media' : p4},{'type': 'photo','media' : p5},{'type': 'photo','media' : p6},{'type': 'photo','media' : p7},{'type': 'photo','media' : p8}]
			
			if Where == 'me': 
				await bot.send_media_group(admin_id, arr)
			else :
				await bot.send_media_group(Where, arr)

				#Adv_coll.find_one({'_id': msg.from_user.id})['Picture_Name'][0]

	if str(msg.from_user.id) == admin_id and msg.text == '/addcar__answer':
		CheckAdv = len(Adm_coll.find_one({'_id' : 1})['AdvArray']) - 1
		advert = Adm_coll.find_one({'_id': 1})['AdvArray'][CheckAdv]
		await GetAdv(advert,'me')
		Adm_coll.update_one({'_id': 1},{'$set' : {'CheckAdv': advert}})

	if str(msg.from_user.id) == admin_id:
		SplitedMsg = msg.text.split(' ')
		if len(SplitedMsg) == 2:
			if SplitedMsg[0] == '/addcar__answer':
				CheckAdv = SplitedMsg[1]
				advert = Adm_coll.find_one({'_id': 1})['AdvArray'][int(CheckAdv)]
				Adm_coll.update_one({'_id': 1},{'$set' : {'CheckAdv': advert}})
				await GetAdv(Adm_coll.find_one({'_id': 1})['AdvArray'][int(CheckAdv)],'me')

	if str(msg.from_user.id) == admin_id and msg.text == '/forms':
			i = 0
			FormStr = ' '
			while i < len(Adm_coll.find_one({'_id' : 1})['AdvArray']):
				FormNum = Adm_coll.find_one({'_id': 1})['AdvArray'][i]	
				FormStr += '\n' + str(i) + ' - ' + str(Adv_coll.find_one({'_id': FormNum})['Marka']) + ' ' + str(Adv_coll.find_one({'_id': FormNum})['Model']) 
				i += 1				
			await bot.send_message(int(admin_id),'Доступні оголошення: ' + FormStr)	
#@ai21jid

	if str(msg.from_user.id) == admin_id:
		SplitedMsg = msg.text.split(' ')
		if len(SplitedMsg) == 2:
			if SplitedMsg[0] == '/add_chanell':
				Adm_coll.update_one({'_id': 1},{'$addToSet': {'ConfArray': SplitedMsg[1]}})
				await bot.send_message(int(admin_id),'Канал успішно доданo!')


	if str(msg.from_user.id) == admin_id:
		SplitedMsg = msg.text.split(' ')
		if SplitedMsg[0] == '/publish' and len(SplitedMsg) == 2:

			i = 0
			while i < len(Adm_coll.find_one({'_id' : 1})['ConfArray']) :
				CheckConf = Adm_coll.find_one({'_id': 1})['ConfArray'][i]
				CheckAdv = '0'
				CheckAdv = SplitedMsg[1]
				await GetAdv(Adm_coll.find_one({'_id': 1})['AdvArray'][int(CheckAdv)], str(CheckConf))	
				i += 1
			await bot.send_message(int(admin_id),'Пост опубліковано!')
			Published = Adm_coll.find_one({'_id': 1})['AdvArray'][int(CheckAdv)]
			Adv_coll.delete_one({'_id' : int(Published)})
			Adm_coll.update_one({'_id': 1},{'$pull': {'AdvArray': Published}})
			Adm_coll.update_one({'_id': 1},{'$set' : {'CheckAdv	': '0'}})
		#elif msg.text == 'Запланувати пост':




	
@dp.message_handler(content_types=["photo"])
async def Commandssdsd(msg: types.Message):

	if  len(Adv_coll.find_one({'_id': msg.from_user.id})['Picture_Name']) < 9:
		Adv_coll.update_one({'_id': msg.from_user.id}, {'$addToSet' : {'Picture_Name' : msg.photo[0].file_id} })

		
	collection.update_one({'_id': msg.from_user.id},{'$set' : {'Position': 1}})	



if __name__ == '__main__':
	executor.start_polling(dp)
