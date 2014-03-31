#!/usr/bin/env python
# -*- coding:utf-8 -*-

month = ["31","28","31","30","31","30","31","31","30","31","30","31"]
month_t = [31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
max_day = 0
min_day = 10000

def cal_month(mon):
    s = 0
    m = int(mon)
    for i in range(m-1):
        s += int(month[i])
    return s

with open('t_alibaba_data.csv','r') as f:
    with open('new_ali_data.csv',"w") as g:
        raw = f.readlines()
        user_item = {}
        item_user = {}
        date_list = []
        for entry in raw[1:]:
            user_id = entry.split(',')[0]
            item_id = entry.split(',')[1]
            action = entry.split(',')[2]
            d = entry.split(',')[3].strip("\xc8\xd5\r\n").split("\xd4\xc2")
            # date_list.append(entry.split(',')[3].strip("\xc8\xd5\r\n").split("\xd4\xc2"))
            day =  month_t[int(d[0])] + int(d[1])
            if day > max_day :
                max_day = day
            if day < min_day:
                min_day = day 
        for entry in raw[1:]:
            user_id = entry.split(',')[0]
            item_id = entry.split(',')[1]
            action = entry.split(',')[2]
            d = entry.split(',')[3].strip("\xc8\xd5\r\n").split("\xd4\xc2")
            # date_list.append(entry.split(',')[3].strip("\xc8\xd5\r\n").split("\xd4\xc2"))
            day =  month_t[int(d[0])] + int(d[1])
            out_s = "%s,%s,%s,%d\r\n" % (user_id,item_id,action,max_day - day)
            g.write(out_s)
        print max_day
        print min_day
