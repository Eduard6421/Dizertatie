
import abc
import carla

from libs.Preprocessors import SocialLSTMOutput,MergeSocialLSTMOutput
from libs.Inference import runSocialLSTMInference


class BaseBehaviour():
    @abc.abstractmethod
    def act(self, frame_id, walkers):
        pass


class RandomBehaviour(BaseBehaviour):
    def act(self, frame_id, walker):
        raise 'Method not implemented'


class LSTMBehavior(BaseBehaviour):

    def act(self,walkers, frame_id):

        lstm_output = None

        for i in range(len(walkers)):
            walker = walkers[i]
            controller = walker.controller

            actor_transform = controller.get_transform()
            actor_location = actor_transform.location
            actor_x = actor_location.x
            actor_y = actor_location.y
            walker.add_to_trace(frame_id, actor_x, actor_y)

            if(frame_id > 80):
                walker_lstm_output = SocialLSTMOutput(walker)
                if(lstm_output is None):
                    lstm_output = walker_lstm_output
                else:
                    lstm_output = MergeSocialLSTMOutput(lstm_output, walker_lstm_output)

        if(frame_id % 90 == 0):
            inference_result = runSocialLSTMInference(lstm_output)
            for i in range(len(walkers)):

                walker = walkers[i]

                walker_prediction = inference_result[0][i][1]
                future_positions = walker_prediction[-12:]

                actor_transform = walker.controller.get_transform()
                actor_location = actor_transform.location

                x_target = float(future_positions[11][1][1])
                y_target = float(future_positions[11][1][0])
                z_target = float(actor_location.z)

                new_target = carla.Location(x_target, y_target, z_target)

                #print('========== Agent {} ========'.format(walker.instance_id))
                # print(new_target)
                # print('============================'.format(walker.instance_id))

                walkers[i].set_destination(new_target)
