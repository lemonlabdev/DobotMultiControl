# 다중 dobot 제어
import sys,threading,time
import DobotDllType as dType

api = dType.load()

errorString = [
    'Success',
    'NotFound',
    'Occupied']

def start_com(dobotId):
    print("Start dobot motion:dobotId =", dobotId)
    dType.SetQueuedCmdClear(api, dobotId)
    dType.SetHOMECmd(api, dobotId, temp = 0, isQueued = 0)
    print("This is Dobotid:", dobotId)

#start_com("COM5")
#start_com("COM3")

maxDobotConnectCount = 20
comlist = ["COM6"] # 연결할 dobot 포트
# 여러개 할때는 ["COM6", "COM4"] 이런식으로 지정

if __name__ == '__main__':
    threads = []
    print("Start search dobot, count:", maxDobotConnectCount)
    #for i in range(0, maxDobotConnectCount):
    #    result = dType.ConnectDobot(api, "",115200)
    for i in comlist:
        result = dType.ConnectDobot(api, i,115200)
        if result[0] == 0:
            print("Connect success: dobotid =", result[3])
            t1 = threading.Thread(target=start_com,args=(result[3],)) # Method 쓰레드 생성 및 DobotId 인자로전달
            threads.append(t1) # 쓰레드 리스트에 할당
            t1.setDaemon(True) # 쓰레드를 데몬으로 해서 게속 작동시키기
            t1.start() # 쓰레드 시작

    for t in threads:
        print("for t")
        t.join()

    dType.DobotExec(api)