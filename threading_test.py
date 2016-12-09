# -*- coding:utf-8 -*-

import threading
import time
import traceback

def say_1(hello):
    for i in range(2):
        print "At time %s ,111111111%s"%(time.ctime(),hello)
        time.sleep(2)

def sya_2(world):
    for i in range(2):
        print "At time %s ,222222222%s"%(time.ctime(),world)
        time.sleep(4)
"""
cookies=[{"SUB": "_2A251TXE7DeRxGeBO7VEW8C3OzzuIHXVWO-XzrDV_PUNbm9ANLRXMkW8VSFdPi3nLY0qbUzQzowkC9jvldA..", "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9WFYI.KksGPATbDsspcsTdYX5NHD95Qcehq0S050eoBNWs4Dqcj.i--ciKyWiK.Ni--Ri-z7i-zNi--RiK.7iKyhi--fi-iWiKys", "ALF": "1512715499", "SCF": "AkTYdawQH6Mr82fJUS_NDeKJfKUnvu1bym5EFGKE7z4dztaXnYzdX8AOZJ7HB1sUegM09hs3sQtMRu5iSlLtx1M.", "ALC": "ac%3D2%26bt%3D1481179499%26cv%3D5.0%26et%3D1512715499%26scf%3D%26uid%3D6063703247%26vf%3D0%26vs%3D0%26vt%3D0%26es%3D05a6ea0b129b3028f26e0a57b4697dad", "sso_info": "v02m6alo5qztKWRk5yljpOQpZCToKWRk5iljoOgpZCjnLaMg5izjbOAs4yjkLeJp5WpmYO0toyDmLONs4CzjKOQtw==", "tgc": "TGT-NjA2MzcwMzI0Nw==-1481179499-ja-58A9E37DB435E73A4D6E6B8B5D1A3C72", "LT": "1481179499"},
         {"SUB": "_2A251TXE7DeRxGeBO7lEV-S_FwjyIHXVWO-XzrDV_PUNbm9ANLVnzkW9OThw7-by82HHqP6GjOn9NLeTRRw..", "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9WFOyeiF.j5KFzH50IvFhSkQ5NHD95Qceh-0Sh.p1K.7Ws4Dqcj.i--Ni-2NiKyFi--ciKLsi-z0i--4iKLFiKnpi--RiKysi-zp", "ALF": "1512715499", "SCF": "AtBf2VvMxV9sz7vXAGZI6IJbDQgT7nLWN0mqkahd0xDG0YOBcT3Dix-vEAsv2jncNtvWLTX57wCNU1CiAcmFrYY.", "ALC": "ac%3D2%26bt%3D1481179499%26cv%3D5.0%26et%3D1512715499%26scf%3D%26uid%3D6053491990%26vf%3D0%26vs%3D0%26vt%3D0%26es%3D0a3b3baf863dcb2dc478e9057f9ff5eb", "sso_info": "v02m6alo5qztKWRk5ylkJOcpY6EiKWRk5iljpSYpZCjjKWRk6SljpSIpY6DhKWRk6CljoSYpZCjhKadlqWkj5OYsI2TjLSOk4S5jpOAwA==", "tgc": "TGT-NjA1MzQ5MTk5MA==-1481179499-ja-8E995B4768273B920DBCD374A79DD07D", "LT": "1481179499"}]
cookies.remove({"SUB": "_2A251TXE7DeRxGeBO7lEV-S_FwjyIHXVWO-XzrDV_PUNbm9ANLVnzkW9OThw7-by82HHqP6GjOn9NLeTRRw..", "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9WFOyeiF.j5KFzH50IvFhSkQ5NHD95Qceh-0Sh.p1K.7Ws4Dqcj.i--Ni-2NiKyFi--ciKLsi-z0i--4iKLFiKnpi--RiKysi-zp", "ALF": "1512715499", "SCF": "AtBf2VvMxV9sz7vXAGZI6IJbDQgT7nLWN0mqkahd0xDG0YOBcT3Dix-vEAsv2jncNtvWLTX57wCNU1CiAcmFrYY.", "ALC": "ac%3D2%26bt%3D1481179499%26cv%3D5.0%26et%3D1512715499%26scf%3D%26uid%3D6053491990%26vf%3D0%26vs%3D0%26vt%3D0%26es%3D0a3b3baf863dcb2dc478e9057f9ff5eb", "sso_info": "v02m6alo5qztKWRk5ylkJOcpY6EiKWRk5iljpSYpZCjjKWRk6SljpSIpY6DhKWRk6CljoSYpZCjhKadlqWkj5OYsI2TjLSOk4S5jpOAwA==", "tgc": "TGT-NjA1MzQ5MTk5MA==-1481179499-ja-8E995B4768273B920DBCD374A79DD07D", "LT": "1481179499"})
print len(cookies)
"""
threads = []
t1 = threading.Thread(target=say_1,args=("11111",))
threads.append(t1)
t2 = threading.Thread(target=sya_2,args=("22222",))
threads.append(t2)

if __name__=='__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    #print "all over %s" %time.ctime()

"""
try:
    a=3/0

第一种写法
except Exception,e:
    print Exception,":",e

第二种写法
except:
    f=open("./log.txt",'a')
    traceback.print_exc(file=f)
    f.flush()
    f.close()
"""
