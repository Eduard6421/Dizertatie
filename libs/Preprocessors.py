import numpy as np

from libs.Walker import Walker


def SocialLSTMOutput(walker: Walker):

    frames = []
    ped_id = []
    x = []
    y = []

    for i in range(len(walker.trace)):
        trace = walker.trace[i]
        frames.append(trace[0])
        ped_id.append(trace[1])
        x.append(trace[2])
        y.append(trace[3])

    last_frame = frames[-1]
    last_ped_id = ped_id[-1]

    for i in range(12):
        last_frame +=10
        frames.append(last_frame)
        ped_id.append(last_ped_id)
        x.append(np.NaN)
        y.append(np.NaN)

    dict_result = {
        'frames': frames,
        'ped_id': ped_id,
        'x' : x,
        'y' : y
    }

    return dict_result

def MergeSocialLSTMOutput(o1,o2):

    dict_result = {
        'frames' : o1['frames'] + o2['frames'],
        'ped_id' : o1['ped_id'] + o2['ped_id'],
        'x' : o1['x'] + o2['x'],
        'y' : o1['y'] + o2['y']
    }

    return dict_result

'''


    result = np.array(walker.trace)
    frames = result[:,0]
    ped_id = result[:,1]
    x = result[:,2]
    y = result[:,3]

    last_frame = frames[-1]
    last_ped_id = ped_id[-1]

    for i in range(12):
        print('added'   )
        frames = np.insert(frames,0,last_frame)
        pred_id = np.insert(ped_id,0,last_ped_id)
        x = np.insert(x,0,np.NaN)
        y = np.insert(y,0,np.NaN)
        last_frame +=10


    dict_result = {
        'frames': frames,
        'ped_id': ped_id,
        'x' : x,
        'y' : y
    }



'''