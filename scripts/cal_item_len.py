# Num of user : 884
# Num of item : 9531
with open('t_alibaba_data.csv','r') as f:
    raw = f.readlines()
    user_item = {}
    item_user = {}
    item_set = set()

    for entry in raw[1:]:
        user_id = entry.split(',')[0]
        item_id = entry.split(',')[1]
        action = entry.split(',')[2]