import time
import carla

from libs.Carla import Carla
from libs.Spawner import SpawnPedestriantsWithTargets,SpawnPedestriantsSocialLSTM, DespawnPedestrians
from libs.Preprocessors import SocialLSTMOutput,MergeSocialLSTMOutput
from libs.Inference import runSocialLSTMInference

carla_client = Carla('localhost', 2000)


def __main__():
    pass

if __name__ == "__main__":
    __main__()