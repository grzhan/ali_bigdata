import pickle
import data

class SlopeOne(object):
    """Implementation of slope one algorithm"""
    def __init__(self,data):
        super(SlopeOne, self).__init__()
        self.data = data
        self.user_item_set = data.getUserItem()
        self.item_user_set = data.getItemUser()
        self.users = data.getUser()
        self.items = data.getItem()

        self.score_dict  = data.getScoreDict()

        self.nearest = {}
        self.predict_score = {}


    def test_case(self):
        self.user_item_set = {"John": {"item1","item2","item3"} , "Mark": {"item1","item2"}, "Lucy": {"item2","item3"}}
        self.item_user_set = {"item1": {"John","Mark"}, "item2" : {"John","Mark","Lucy"}, "item3" : {"John","Lucy"}}
        self.users = {"John","Mark","Lucy"}
        self.items = {"item1","item2","item3"}
        self.score_dict = {"John": {"item1":5,"item2":3,"item3":2}, "Mark": {"item1":3,"item2":4}, "Lucy":{"item2":2,"item3":5}}
        self.nearest = {"John":{"Mark","Lucy"}, "Mark":{"John","Lucy"}, "Lucy": {"John","Mark"}}


    def main(self):
        # self.importNearest()
        score_dict = self.score_dict

        user_item = self.user_item_set
        item_user = self.item_user_set
        for user in self.users:
            diff_t = set()
            inter_d = dict()
            diff_d = dict()
            for near in self.nearest[user]:
                # Get difference set between active user's <item set> and nearest user's <item set>
                diff = user_item[near].difference(user_item[user])
                # Get total diff <item> set
                diff_t = diff_t.union(diff)

                intersec = user_item[user].intersection(user_item[near])
                # For each <item> that nearest user and active user both have.
                for inter in intersec:
                    # Record <intersection item> : <nearest user>
                    self.dict_init_set(inter_d,inter)
                    inter_d[inter].add(near)

                # For each <item> that nearest user has but active user not
                for dif in diff:
                    # Record <difference item> : <nearest user>
                    self.dict_init_set(diff_d, dif)
                    diff_d[dif].add(near)

            # For each <item> that active user not has
            for diff in diff_t:
                # For each <item> that active user has
                predict = 0
                num_t = 0
                for self_ in user_item[user]:
                    total = 0; num = 0
                    if inter_d.has_key(self_):
                        intersection = inter_d[self_].intersection(diff_d[diff])
                    else:
                        continue

                    # For each <nearest user> that match conditions
                    for inter in intersection:
                        total = total +  float(score_dict[inter][diff]) - float(score_dict[inter][self_])
                        num += 1
                    if num > 0:
                        average = total * 1.0 / num
                        slope = average + float(score_dict[user][self_])
                        num_t += num
                        predict += slope * num

                self.addPredict(user,diff, predict * 1.0 / num_t)

    def addPredict(self,user,item,value):
        if value < 10:
            return 
        predict_score = self.predict_score
        if not predict_score.has_key(user):
            predict_score[user] = dict()
        predict_score[user][item] = value

    def outputPredict(self,K=10,filename='predict_score'):
        predict_score = self.predict_score
        self.strings = str()
        filename += '_' + str(K)
        filepath = '/home/grzhan/Workspace/ali_bigdata/data/' + filename

        for i in predict_score.keys():
            sort = sorted(predict_score[i].items(),key=lambda e:e[1], reverse=True)
            l = [x[0] for x in sort]
            if len(l) > K:
                l = l[:K]
            s = reduce(lambda x,y: x+','+str(y), l[1:],str(l[0]))
            self.strings += i + ':' + s + '\r\n'
        with open(filepath,'w') as filehandle:
            filehandle.write(self.strings)

    def dict_init_set(self,d,i):
        if not d.has_key(i):
            d[i] = set()


    def importNearest(self):
        self.nearest_file_name = "/home/grzhan/Workspace/ali_bigdata/data/nearest_serialize"
        filename = self.nearest_file_name
        with open(filename,"r") as filehandle:
            s = filehandle.read()
            self.nearest = pickle.loads(s)



if __name__ == '__main__':
    model = data.Data("/home/grzhan/Workspace/ali_bigdata/data/out.txt")
    model.createRawData()
    model.processRaw()

    slope = SlopeOne(model)
    # slope.test_case()
    slope.importNearest()
    slope.main()
