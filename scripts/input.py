with open('t_alibaba_data.csv','r') as f:
    raw = f.readlines()
    user_item = {}
    item_user = {}
    for entry in raw[1:]:
        user_id = entry.split(',')[0]
        item_id = entry.split(',')[1]
        action = entry.split(',')[2]
        if action == '1':
            if user_item.has_key(user_id):
                user_item[user_id].add(item_id)
            else:
                user_item[user_id] = set()
                user_item[user_id].add(item_id)
            if item_user.has_key(item_id):
                item_user[item_id].add(user_id)
            else:
                item_user[item_id] = set()
                item_user[item_id].add(user_id)
                
    user_rec = {}
    for entry in raw[1:] :
        user_id = entry.split(',')[0]
        item_id = entry.split(',')[1]
        action = entry.split(',')[2]
        if action == '2' or action == '3':
            if user_rec.has_key(user_id):
                user_rec[user_id].add(item_id)
            else:
                user_rec[user_id] = set()
                user_rec[user_id].add(item_id)

    for user in user_rec.keys():
        if user_item.has_key(user):
            user_rec[user] = user_rec[user] - user_item[user]

with open('answer','w') as f:
    for user in user_rec.keys():
        str_out = user + ' '
        if len(user_rec[user]) == 0 : continue
        for item in user_rec[user]:
            str_out += item + ','
        str_out = str_out.rstrip(',')
        print str_out
        f.write(str_out + '\r\n')









