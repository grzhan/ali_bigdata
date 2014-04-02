#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys

class Data(object):
	"""docstring for Data"""
	def __init__(self,filename="../data/out.txt",type_="raw"):
		super(Data, self).__init__()
		self.filename = filename
		self.type = type_
		self.count = 0
		
		self.user_set = set()
		self.item_set = set()
		self.score_dict = {}

		self.user_item_rel = {}
		self.item_user_rel = {}

		self.score_total = 0
		self.score_average = 0


	def createRawData(self):
		with open(self.filename,"r") as filehandle:
			self.raw = filehandle.readlines()
	
	def processRaw(self):
		"""Process raw data line by line """
		for line in self.raw:
			slices = line.split(' ')
			user = slices[0].strip("\n").strip("\r")
			item = slices[1].strip("\n").strip("\r")
			score = slices[2].strip("\n").strip("\r")
			self.user_set.add(user)
			self.item_set.add(item)
			self.addScore(user,item,score)
			self.addBelong(self.user_item_rel, user, item)
			self.addBelong(self.item_user_rel, item, user)
			self.score_total += float(score)
			self.count += 1
		self.score_average = self.score_total * 1.0 / self.count

	def addScore(self,user,item,score):
		""" Add a record(user->item->score) in score_dict """
		if not self.score_dict.has_key(user):
			self.score_dict[user] = {}
		self.score_dict[user][item] = score

	def addBelong(self, dict_, index,element):
		if not dict_.has_key(index):
			dict_[index] = set()
		dict_[index].add(element)

	def getScoreDict(self):
		return self.score_dict

	def getUserItem(self):
		return self.user_item_rel

	def getItemUser(self):
		return self.item_user_rel

	def getUser(self):
		return self.user_set

	def getItem(self):
		return self.item_set

	def getCount(self):
		return self.count

if __name__ == '__main__':
	data = Data()
	data.createRawData()
	data.processRaw()
