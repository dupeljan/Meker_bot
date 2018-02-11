#!/bin/python
import json
import time
from threading import Thread

class dump_class(Thread): 
	'''с некоторым промежутком сохраняет auth_list'''
	def __init__(self,param_list,interval):
		Thread.__init__(self)
		self.auth_list = param_list
		self.interval = interval


	def run(self):
		while 1:
			time.sleep(self.interval)
			with open('dump_file','w') as file:
				json.dump(self.auth_list,file)
			print("Dump!")

class auth_class:
	'''
	Хранит пары [tg_id , vk_id]
	Сохраняет и загружает эти пары
	в файл
	'''
	def __init__ (self):
		self.auth_list = list()
		self.candidate_list = list()

	def get_auth_list_object(self):
		return self.auth_list

	def load_auth_list(self):
		try:
			with open('dump_file','r') as file:
				self.auth_list = json.loads(file.read())
		except FileNotFoundError:
			print("dump file not found")

	def candidate_list_extend(self,msg):
		self.candidate_list.append(msg)

	def candidate_list_remove(self,msg):
		self.candidate_list.remove(msg)

	def auth_list_extend(self,msg):
		self.auth_list.append(msg)
	'''
	def first_auth(self,msg): # этап регистации в tg

		vk_id = vk.get_uid(msg["messege"]["text"])
		if vk_id != -1:
			#добавляем в candidate_list пару
			self.candidate_list.extend([ tg.get_chatID(msg) , vk_id ])
			#Отправляем инструкции
			MSG = "Check your vk messege"
			tg.send_msg(tg.get_chatID(msg),MSG)

			MSG = "Your tg username is " + tg.get_username(msg) + ',\n'
			MSG += 'if it\'s true please answer "yes"'
			vk.send_msg(vk_id, MSG)
		else:
			tg.send_msg(tg.get_chatID(msg),"NOT FOUND \n try again") 

	def second_auth(self,msg): # этап регистрации в vk
		if self.confim(msg) and self.is_candidate(msg):
			pair = self.get_pair(msg)
			self.auth_list.extend(pair)
			self.candidate_list.remove(pair)
			vk.send_msg(pair[1],"Congratulations! Success!")
		else:
			vk.send_msg(vk.get_uid(msg),"Error, please firstly write tg bot")
	'''

	def confim(self,msg):
		result = msg['body']
		return result in ['y' , 'Y' , 'Yes', 'yes']

	def is_candidate(self,msg):
		result = msg['uid']
		i = 0
		print(self.candidate_list)
		for x in self.candidate_list:
			if self.candidate_list[i][1] == result:
				return True
			i += 1
		return False

	def get_pair(self,msg): # msg из vk , вернуть пару из candidate_list
		result = msg['uid']
		i = 0
		for x in self.candidate_list:
			if self.candidate_list[i][1] == result:
				return x
			i +=1
		return "Error" # Ошибки быть не должно

	# возвращает пару если нашел в списке tg chatID
	# иначе False
	def user_tg(self,msg): # msg из телеграма
		result = msg['message']['chat']['id']
		i = 0
		for x in self.auth_list:
			if self.auth_list[i][0] == result:
				return x
			i += 1
		return False
		

	def user_vk(self,msg):  # msg из vk
		result = msg['uid']
		i = 0
		for x in self.auth_list:
			if self.auth_list[i][1] == result:
				return x
			i += 1
		return False

auth = auth_class()