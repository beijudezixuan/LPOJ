# coding=utf-8

import MySQLdb
import socket
import json
import time
from time import sleep
from Codeforces import get_CF_data
from HDU import get_HDU_data
from Vjudge import get_VJ_data
from LPOJ import get_LPOJ_data


myjsonfile = open("./setting.json", 'r')
judgerjson = json.loads(myjsonfile.read())

db = MySQLdb.connect(judgerjson["db_ip"], judgerjson["db_user"], judgerjson["db_pass"],
                     judgerjson["db_database"], int(judgerjson["db_port"]), charset='utf8')

while True:
    cursor = db.cursor()
    cursor.execute( "SELECT * from board_board")
    datas = cursor.fetchall()
    for data in datas:
        username = str(data[0])
        accounts = str(data[5]).split("|")
        print(username)
        CF = get_CF_data(accounts[0])
        print(accounts[0],"CF:",CF)
        if CF[0] == -1:
            continue
        HDU = get_HDU_data(accounts[1])
        print(accounts[1],"HDU:",HDU)
        if HDU[0] == -1:
            continue
        VJ = get_VJ_data(accounts[2])
        print(accounts[2],"VJ:",VJ)
        if VJ[0] == -1:
            continue
        LPOJ = get_LPOJ_data(accounts[3])
        print(accounts[3],"LPOJ:",LPOJ)
        if LPOJ[0] == -1:
            continue

        Others = [int(str(data[6]).split("|")[-1]),int(str(data[7]).split("|")[-1])] #其他OJ

        today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        totleac = CF[0] + HDU[0] +VJ[0] + LPOJ[0] + Others[0]
        cursor.execute("INSERT INTO board_dailyboard(username,account,collecttime) SELECT '%s', %d,'%s' FROM DUAL WHERE NOT EXISTS(SELECT * FROM board_dailyboard WHERE username = '%s' and collecttime= '%s')" % (username,totleac,today,username,today))

        ac = str(CF[0]) + "|" + str(HDU[0]) + "|" + str(VJ[0]) + "|"+ str(LPOJ[0]) + "|" + str(Others[0])
        submit = str(CF[1]) + "|" + str(HDU[1]) + "|" + str(VJ[1]) + "|"+ str(LPOJ[1]) + "|" + str(Others[1])
        cursor.execute("UPDATE board_board SET acnum = '%s' ,submitnum = '%s'  WHERE username = '%s'" % (ac,submit,username))
        db.commit()
        print(username,ac,submit)



    sleep(7200)



