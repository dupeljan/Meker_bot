#!/bin/python
import requests
import json
from pyauth import auth


class vk_bot:
	
	def __init__(self):
		self.URL = 'https://api.vk.com/method/'
		self.TOKEN = '5496ea96b321240adecde76e7f017f83d07d0945fae21829c1ff76422b31e3424bb3a687d4233a5a076d5'
		self.PARAMETRS = 'access_token=' + self.TOKEN 
		#self.tg = tg_bot()

	def get_last_msg_json(self):
		return self.get_updates()['response'][1]['mid']

	def get_msg_json(self,request):
		return request['response'][1]['mid']

	def get_updates(self):
		METHOD ='messages.get?'
		return requests.get(self.URL + METHOD + self.PARAMETRS).json()

	def send_msg(self , user_id , message):
		METHOD = 'messages.send?'
		parametrs = self.PARAMETRS + '&user_id=' + str(user_id) + '&message=' + str(message)
		return requests.get(self.URL + METHOD + parametrs).json()

	def get_last_msg(self):
		result = self.get_updates()['response'][1]	
		ans_str = result['body']
		if "attachment" in result:
			ans_str +=  result["attachment"]["type"] 	
		return ans_str +  str(self.fwd_msg_processing(result) )

	def get_msg(self,msg):
		ans_str = msg['body']
		if "attachment" in msg:
			ans_str +=  msg["attachment"]["type"] 	
		return ans_str +  str(self.fwd_msg_processing(msg) )

	def fwd_msg_processing(self,msg_branch,tab = 1):
		if "fwd_messages" in msg_branch:
			ans_str = ""
			msg_branch = msg_branch["fwd_messages"]
			i = 0
			for x in msg_branch:
				ans_str +="\n" + tab*'|' + str(self.get_username(msg_branch[i]['uid']))+ ':' +  msg_branch[i]['body'] 
				#проверяем на вложения
				if "attachment" in msg_branch[i]:
					ans_str += msg_branch[i]["attachment"]["type"]

				ans_str += self.fwd_msg_processing(msg_branch[i] , tab + 1 ) 
				i+=1
			return ans_str
		return ""

	def get_last_userID(self):
		return self.get_updates()['response'][1]['uid']

	def get_userID(self,msg):
		return msg['uid']

	def get_last_Messg_nubmer(self):
		return self.get_updates()['response'][1]['mid']

	def print_updates(self):
		with open('vk_json_update','w') as file:
			json.dump(self.get_updates() ,file,indent = 2)

	def get_username(self, user_id):
		METHOD = "users.get?"
		result = requests.get(self.URL + METHOD + self.PARAMETRS + "&user_ids=" + str(user_id)).json() 
		try:
			return result['response'][0]['first_name'] + ' ' + result['response'][0]['last_name']
		except IndexError:
			return "NO NAME"
			
	def get_uid(self,user_id):
		METHOD = "users.get?"
		result = requests.get(self.URL + METHOD + self.PARAMETRS + "&user_ids=" + str(user_id)).json() 
		try:
			return result["response"][0]["uid"]
		except KeyError:#IndexError:
			return -1


#=====================================================
	'''
	def processing_msg(self,msg):
		tg_chat_id = auth.user_vk(msg)
		if tg_chat_id:
			self.tg.send_msg(tg_chat_id, self.get_msg(msg))
		else:
			self.second_auth(msg)

	def second_auth(self,msg): # этап регистрации в vk
		if auth.confim(msg) and auth.is_candidate(msg):
			pair = auth.get_pair(msg)
			auth.auth_list_extend(pair)
			auth.candidate_list_remove(pair)
			self.send_msg(pair[1],"Congratulations! Success!")
		else:
			self.send_msg(vk.get_uid(msg),"Error, please firstly write tg bot")
	'''
#=====================================================		

class  tg_bot:

	def __init__(self):
		self.TOKEN = '525669681:AAGl4hQeZqjic2viTE8D_LvZDxKiVcOKDII'
		self.URL = 'https://api.telegram.org/bot' + self.TOKEN + '/'
		#self.vk = vk_bot()

	def get_updates(self, offset = 1):
		METHOD = 'getUpdates?offset=' + str(offset)
		return requests.get(self.URL + METHOD).json()

	def get_last_updateID(self):
		up_id = 1
		while 1:
			request = self.get_updates(up_id)
			up_id = request['result'][-1]['update_id']
			if len(self.get_updates(up_id)['result']) == 1:
				break
		return up_id

	def get_updateID(self,msg):
		return msg['update_id']

	def get_last_msg_json(self,offset = 1):
		try:
			return self.get_updates(offset)['result'][-1]
		except IndexError:
			return 0

	def get_msg_json(self,request):
		try:
			return request['result'][-1]
		except IndexError:
			return 0

	def get_last_msg(self):
		result = self.get_updates()['result'][-1]["message"]
		MSG = ""
		if "reply_to_message" in result:
			MSG = result['text'] + '\n'
			MSG += "reply from:" + result["reply_to_message"]["from"]["username"] + '\n'
			result = result['reply_to_message']
		
		if "forward_from" in result:
			MSG += "from: " + result["forward_from"]["username" ] + "\n"

		if "text" in result:
			MSG += result["text"] 
		else:
			self.send_Messege(self.get_last_chatID(),"I can't send this :(")

		return MSG

	def get_msg(self,result):
		result = result["message"]
		MSG = ""
		if "reply_to_message" in result:
			MSG = result['text'] + '\n'
			MSG += "reply from:" + result["reply_to_message"]["from"]["username"] + '\n'
			result = result['reply_to_message']
		
		if "forward_from" in result:
			try:
				MSG += "from: " + result["forward_from"]["username" ] + "\n"
			except KeyError:
				MSG += "from: " + result["forward_from"]["first_name" ] 
				try:
					MSG += ' ' + result["forward_from"]["last_name" ]
				except KeyError:
					pass
				MSG += '\n'

		if "text" in result:
			MSG += result["text"] 
		else:
			self.send_msg(self.get_last_chatID(),"I can't send this :(")

		return MSG
		
	def send_msg(self,chatID, text):
		return requests.get(self.URL + 'sendMessage?chat_id=' + str(chatID) + '&text='+ text ).content

	def send_Photo(self,chatID,file):
		METHOD = 'sendPhoto?chat_id='
		return requests.post(self.URL + METHOD + str(chatID), files = file )		

	def get_last_chatID(self):
		return self.get_updates()['result'][-1]['message']['chat']['id']

	def get_last_mesId(self):
		return self.get_updates()['result'][-1]['message']['message_id']

	def print_updates(self,offset = 1):
		with open('tg_json_update','w') as file:
			json.dump(self.get_updates(offset) ,file,indent = 2)

	def get_chatID(self,msg):
		return msg['message']['chat']['id']

	def get_username(self,msg):
		try:
			return msg['message']['from']['username']
		except KeyError:
			try:
				return msg['message']['from']["first_name"] + ' ' + msg['message']['from']['last_name']
			except KeyError:
				return msg['message']['from']["first_name"]
#===================================================== 
	'''
	def processing_msg(self,msg):
		vk_id = auth.user_tg(msg)
		if vk_id:
			self.vk.send_msg(vk_id,self.get_msg(msg))
		else:
			self.first_auth(msg)

	def first_auth(self,msg): # этап регистации в tg
		vk_id = self.vk.get_uid(msg["messege"]["text"])
		if vk_id != -1:
			#добавляем в candidate_list пару
			auth.candidate_list_extend([ tg.get_chatID(msg) , vk_id ])
			#Отправляем инструкции
			MSG = "Check your vk messege"
			self.send_msg(tg.get_chatID(msg),MSG)

			MSG = "Your tg username is " + tg.get_username(msg) + ',\n'
			MSG += 'if it\'s true please answer "yes"'
			self.vk.send_msg(vk_id, MSG)
		else:
			self.send_msg(tg.get_chatID(msg),"NOT FOUND \n try again") 
	'''
#=====================================================

class msg_processing:

	def __init__(self):
		self.vk = vk_bot()
		self.tg = tg_bot()

	def telegram(self,msg):
		pair = auth.user_tg(msg) #пытаемся получить vk_id из tg_id
		if pair:
			self.vk.send_msg(pair[1],self.tg.get_msg(msg))
			print("tg->vk")
		else:
			self.first_auth(msg)

	def vk_(self,msg):
		pair = auth.user_vk(msg) #пытаемся получить tg_id из vk_id
		if pair:
			self.tg.send_msg(pair[0], self.vk.get_msg(msg))
			print("vk->tg")
		else:
			self.second_auth(msg)

	def first_auth(self,msg):
		vk_id = self.vk.get_uid(msg["message"]["text"]) # Пытаемя найти vk_uid
		if vk_id != -1:
			#добавляем в candidate_list пару
			auth.candidate_list_extend([ tg.get_chatID(msg) , vk_id ])
			#Отправляем инструкции
			MSG = "Check your vk messege"
			self.tg.send_msg(tg.get_chatID(msg),MSG)

			MSG = "Your tg username is " + self.tg.get_username(msg) + ',\n'
			MSG += 'if it\'s true please answer "yes"'
			self.vk.send_msg(vk_id, MSG)
		else:
			self.tg.send_msg(self.tg.get_chatID(msg),"NOT FOUND \n try again") 
	
	def second_auth(self,msg):
		if auth.confim(msg) and auth.is_candidate(msg):
			pair = auth.get_pair(msg)
			auth.auth_list_extend(pair)
			auth.candidate_list_remove(pair)
			self.vk.send_msg(pair[1],"Congratulations! Success!")
			print("New user!")
		else:
			self.vk.send_msg(self.vk.get_userID(msg),"Error, please firstly write tg bot")

vk = vk_bot()
tg = tg_bot()
processing = msg_processing()