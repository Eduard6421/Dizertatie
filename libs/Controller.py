
from libs.Spawner import  SpawnPedestriansAtLocations, GetSpawnPointsNearLocation
from libs.Behaviours import LSTMBehavior

def spawnWalkers(carla_client, num_agents):
    spectator_transform = carla_client.get_spectator_transform()
    spectator_location = spectator_transform.location
    spawn_locations = GetSpawnPointsNearLocation(carla_client,spectator_location,num_agents)
    walkers = SpawnPedestriansAtLocations(carla_client,spawn_locations,num_agents)
    return walkers


def buildPipeline():


    lstmBehaviour = LSTMBehavior()

    action_pipeline = [
        lstmBehaviour
        #
        #
        #
    ]

    return action_pipeline


def simulateStep(carla_client, walkers, action_pipeline, step=10):
    tick = carla_client.tick()
    if(tick % step == 0):
        for action in action_pipeline:
            action.act(walkers, tick)

