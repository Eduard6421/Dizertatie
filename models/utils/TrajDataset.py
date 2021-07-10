import tensorflow as tf
import numpy as np

from typing import Text


class TrajectoryDataset(tf.data.Dataset):


    def get_total_frames(self,):
        return self.total_frames

    def set_total_frames(self,arg):
        self.total_frames = arg


    def _generator(filePath):
        
        read_mode = "r"
        file = open(filePath,read_mode)

        num_prediction_frames = 20

        frame_map = {
        }
        frame_list = []

        for idx,line in enumerate(file):
            items = line.split()
            items = map(lambda x : float(x),items)
            (frame_id,agent_id,x_coord,y_coord) = items

            frame_list.append(frame_id)

            if frame_id in frame_map:
                frame_map[frame_id]['agents'].append(agent_id)
                frame_map[frame_id][agent_id] = (x_coord,y_coord)
            else:
                frame_map[frame_id] = {}
                frame_map[frame_id]['frame_num'] = frame_id
                frame_map[frame_id]['agents'] = [agent_id]
                frame_map[frame_id][agent_id] = (x_coord,y_coord)


        frame_list = list(dict.fromkeys(frame_list))
        frame_list.sort()
        frame_num = len(frame_list)

        max_agents = 0

        for i in range(0,frame_num - num_prediction_frames, num_prediction_frames):
        

            pedestrian_tensor = np.array([])

            for j in range(i,i+num_prediction_frames):
                current_frame = frame_list[j]
                current_frame_data = frame_map[current_frame]
                if(len(current_frame_data['agents']) > max_agents):
                    max_agents = len(current_frame_data['agents'])
                
                
                coordinate_tensor = []


                for element in frame_map[current_frame]['agents']:
                    print(element)
                    coordinate_tensor.append(frame_map[element])

                print(coordinate_tensor)


                print(frame_map[current_frame])
            #current_data = frame_map.slice(i,i+num_prediction_frames)
            #print(current_data)

    def __new__(cls,filePath):


        return tf.data.Dataset.from_generator(
            cls._generator,
            output_signature = tf.TensorSpec(shape = (4,), dtype = tf.int64),
            args=(filePath,)
        )
