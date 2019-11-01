import threading
import DobotDllType as dType

#Load Dll
api = dType.load()      

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

def MoveBox(dobotId, targetx, targety):
  targetz = -120
  dType.SetDeviceWithL(api, dobotId, 1)
  main.process.emit("CheckLinearRail", "")
  dType.SetPTPLParamsEx(api,dobotId,100,50,1)
  dType.SetEndEffectorParamsEx(api, dobotId,59.7, 0, 0, 1)
  if True:
    current_pose = dType.GetPose(api)
    dType.SetPTPWithLCmdEx(api, 1, dobotId,current_pose[0], current_pose[1], current_pose[2], current_pose[3], 0, 1)
    dType.SetPTPCmdEx(api, dobotId, 0, 250,  0,  targetz, 0, 1)
    dType.SetEndEffectorSuctionCupEx(api, dobotId, 1, 1)
    dType.SetPTPCmdEx(api, dobotId, 0, 250,  0,  0, 0, 1)
    current_pose = dType.GetPose(api)
    dType.SetPTPWithLCmdEx(api, 1, current_pose[0], current_pose[1], current_pose[2], current_pose[3], 1000, 1)
    current_pose = dType.GetPose(api)
    dType.SetPTPCmdEx(api, 4, (-90),  80,  (dType.GetPoseEx(api, 7)), current_pose[7], 1)
    dType.SetEndEffectorSuctionCupEx(api, 0, 1)
    dType.SetPTPCmdEx(api, 0, 250,  0,  50, 0, 1)
  else:
    pass

if __name__ == '__main__':
    result = dType.ConnectDobot(api, "COM6", 115200)
    dobotId = result[3]
    state = result[0]
    print("Connect status:",CON_STR[state])

    # target = [[250,0],[275,0],[250.-22],[275,-22]]

    if (state == dType.DobotConnect.DobotConnect_NoError):

        #Clean Command Queued
        dType.SetQueuedCmdClear(api, dobotId)

        #Async Motion Params Setting
        dType.SetHOMEParams(api, dobotId,250, 0, 50, 0, isQueued = 0)
        dType.SetPTPJointParams(api,dobotId, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 0)
        dType.SetPTPCommonParams(api,dobotId, 100, 100, isQueued = 0)

        #dType.SetHOMECmd(api, dobotId, temp=0, isQueued=0)

        print("start moving")
        MoveBox(dobotId, 250, 0)

        #Start to Execute Command Queued
        #dType.SetQueuedCmdStartExec(api, dobotId)

        
        #Wait for Executing Last Command
        #while lastIndex > dType.GetQueuedCmdCurrentIndex(api, dobotId)[0]:
        #    dType.dSleep(100)

        #Stop to Execute Command Queued
        dType.SetQueuedCmdStopExec(api,dobotId)

    #Disconnect Dobot
    dType.DisconnectDobot(api, dobotId)