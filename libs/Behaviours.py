
import abc
from lib2to3.pytree import Base
from typing import List

from torch import lstm
from libs.Walker import Walker
from tracemalloc import start
import carla

from libs.Preprocessors import SocialLSTMOutput, MergeSocialLSTMOutput
from libs.Inference import runSocialLSTMInference


class BaseBehaviour():
    @abc.abstractmethod
    def act(self, walkers, frame_id):
        pass


class LSTMBehavior(BaseBehaviour):

    def __init__(self) -> None:
        self.last_run = 0
        self.started = False
        super().__init__()


    def act(self, walkers : List[Walker], frame_id):

        has_enough_trace = False

        lstm_output = None

        tick_diff = 100

        for i in range(len(walkers)):
            walker = walkers[i]
            controller = walker.controller

            actor_transform = controller.get_transform()
            actor_location = actor_transform.location
            actor_x = actor_location.x
            actor_y = actor_location.y

            walker.add_to_trace(frame_id, actor_x, actor_y)

            if(walker.get_trace_length() == 8):
                walker_lstm_output = SocialLSTMOutput(walker)
                if(lstm_output is None):
                    lstm_output = walker_lstm_output
                else:
                    lstm_output = MergeSocialLSTMOutput(lstm_output, walker_lstm_output)

                has_enough_trace = True


        if(has_enough_trace == True and (frame_id - self.last_run) > tick_diff):

            self.last_run = frame_id

            inference_result = runSocialLSTMInference(lstm_output,len(walkers))
            for i in range(len(walkers)):

                walker = walkers[i]


                walker_prediction = inference_result[0][i][1]
                future_positions = walker_prediction[-12:]

                actor_transform = walker.controller.get_transform()
                actor_location = actor_transform.location

                x_target = float(future_positions[11][0][1])
                y_target = float(future_positions[11][0][0])
                z_target = float(actor_location.z)

                new_target = carla.Location(x_target, y_target, z_target)

                if(i == 0):
                    print('========== Agent {} ========'.format(walker.instance_id))
                    print("Current Location")
                    print(walker.actor.get_location())
                    print("Target Location")
                    print(new_target)
                    print('============================'.format(walker.instance_id))

                walkers[i].set_destination(new_target)
