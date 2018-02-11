#!/bin/python

import requests
import json
from bots import vk, tg, processing
from pyauth import auth , dump_class

DUMP_INTERVAL = 60 #интервал дампа в секундах
'''
Пересылаем текстовые сообщения из тг в вк и обратно
'''

auth.load_auth_list()
dump = dump_class(auth.get_auth_list_object(),DUMP_INTERVAL)
dump.start()

offset = tg.get_last_updateID()

MSG_TG = tg.get_last_msg_json(offset)
MSG_VK = vk.get_last_msg_json()

print('Start working!')
while 1:
	# tg processing
	request_tg = tg.get_updates(offset)
	ACTUAL_MSG_TG = tg.get_msg_json(request_tg)
	if ACTUAL_MSG_TG != MSG_TG:
		request_tg = request_tg['result']
		i = request_tg.index(MSG_TG) + 1 if MSG_TG else MSG_TG
		while i < len(request_tg):
			processing.telegram(request_tg[i])
			i+=1
		MSG_TG = ACTUAL_MSG_TG
		# двигаем offset к последнему сообщению
		offset = tg.get_updateID(ACTUAL_MSG_TG) 


	# vk processing

	request_vk = vk.get_updates()
	ACTUAL_MSG_VK = vk.get_msg_json(request_vk)


	if ACTUAL_MSG_VK != MSG_VK:
		request_vk = request_vk['response']

		#i = request_vk.index(MSG_VK) - 1 
		# находим индекс сообщения с id MSG_VK
		i = 2
		for x in request_vk:
			if request_vk[i]['mid'] == MSG_VK:
				break
			i+=1
		i -= 1

		while i > 0:
			processing.vk_(request_vk[i])
			i-=1
		MSG_VK = ACTUAL_MSG_VK
