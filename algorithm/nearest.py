import data
import pickle

class Nearest(object):
	""" =========================================================
	  It's a very important module that can determine performance 
	and correctness of this	algorithm. 
	  CURRENT STRATEGY : To find nearest user, we look at users 
	set's intersection, and we only calculate elements number of 
	this intersection to determine their similarity.
	============================================================="""
	def __init__(self,data):
		super(Nearest, self).__init__()
		self.users = data.getUser()
		self.items = data.getItem()
		self.user_item = data.getUserItem()
		self.nearest = {}
		self.outfilename = "/home/grzhan/Workspace/ali_bigdata/data/nearest_serialize"

		self.simi_total = 0
		self.simi_avg = 0
		self.simi_n = 0

		self.len_t = 0
		self.len_a = 0
		self.len_n = 0
		self.len_threshold = 0.0677358214499078

	def main(self):
		K = 4
		user_item = self.user_item
		nearest = self.nearest
		for active_user in self.users:
			self.nearest_set_init(active_user)
			for dest_user in self.users:
				self.nearest_set_init(dest_user)
				if active_user == dest_user:
					continue
				if active_user in nearest[dest_user]:
					continue
				
				intersection = user_item[active_user].intersection(user_item[dest_user])
				if not intersection  :
					continue
				# Important
				simi = self.strategyLen(intersection, user_item[active_user], user_item[dest_user])
				if simi :
					nearest[active_user].add(dest_user)
					nearest[dest_user].add(active_user)


	def strategyLen(self,inter,active_set,dest_set):
		# Important function !
		self.simi_n += 1
		self.len_n += 1

		len_inter = len(inter)
		len_activ = len(active_set)
		len_ = len_inter * 1.0 / len_activ
		self.len_t += len_

		if len_ >= 0.2:    # What threshold is better ?
			return True
		else:
			return False
		# if len_inter >= 4:
		# 	return True
		# else:
		# 	return False



	def nearest_set_init(self,index):
		nearest = self.nearest
		if not nearest.has_key(index):
			nearest[index] = set()

	def export(self):
		filename = self.outfilename
		serialize_s =  pickle.dumps(self.nearest)
		with open(self.outfilename, "w") as filehandle:
			filehandle.write(serialize_s)

	def getNearest(self):
		return self.nearest


if __name__ == '__main__':
	data_model = data.Data("/home/grzhan/Workspace/ali_bigdata/data/out.txt")
	data_model.createRawData()
	data_model.processRaw()
	nearest = Nearest(data_model)
	nearest.main()
	nearest.export()



# Threshold:
# In [3]: nearest.len_t /  nearest.len_n
# Out[3]: 0.0667062763561931
