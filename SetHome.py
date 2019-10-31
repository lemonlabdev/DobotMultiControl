# 다중 dobot 제어
import sys,threading,time
import DobotDllType as dType

api = dType.load()

errorString = [
    'Success',
    'NotFound',
    'Occupied']

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
            dType.SetHOMECmd(api, result[3],temp=0,isQueued=1)

    for t in threads:
        t.join()
    dType.DobotExec(api)