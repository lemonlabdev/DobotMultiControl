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
    dType.SetHOMEParams(api, dobotId, 250, 0, 50, 0, isQueued=0) # 홈 파라미터 설정
    dType.SetPTPJointParams(api, dobotId, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1) # joint별 속도, 가속도 설정
    dType.SetPTPCommonParams(api, dobotId, 100, 100, isQueued = 1) # 속도비 및 가속도비 설정

    dType.SetEndEffectorSuctionCup(api, dobotId, 1, 1, isQueued=0)
    dType.dSleep(10000)
    dType.SetEndEffectorSuctionCup(api, dobotId, 1, 0, isQueued=0)
    
    
    dType.SetQueuedCmdClear(api, dobotId)
    dType.SetHOMECmd(api, dobotId, temp = 0, isQueued = 1)
    dType.SetQueuedCmdStopExec(api, dobotId)


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
        print("getresult ",i)
        if result[0] == 0:
            print("Connect success: dobotid =", result[3])
            t1 = threading.Thread(target=start_com,args=(result[3],)) # Method 쓰레드 생성 및 DobotId 인자로전달
            threads.append(t1) # 쓰레드 리스트에 할당
            t1.setDaemon(True) # 쓰레드를 데몬으로 해서 게속 작동시키기
            t1.start() # 쓰레드 시작

    for t in threads:
        t.join()
    dType.DobotExec(api)