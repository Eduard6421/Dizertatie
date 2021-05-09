import glob
import os
import sys
import time
import carla
import argparse
import logging
import random


from libs.WeatherBuilder import WeatherBuilder
from libs.Walker import Walker


def SpawnPedestriantsSocialLSTM(carla_client):

    num_agents = 35
    walkers = []

    try:

        world = carla_client.get_world()

        percentagePedestriansCrossing = 0.0

        spawn_points = []
        batch_commands = []

        walker_blueprints = carla_client.get_all_walker_blueprints()

        for i in range(num_agents):
            spawn_point = carla.Transform()
            loc = carla_client.get_random_location_from_navigation()
            if(loc!= None):
                spawn_point.location = loc
                walker_blueprint = random.choice(walker_blueprints)
                walker_create_command = carla_client.command_spawn_actor(walker_blueprint, spawn_point)
                batch_commands.append(walker_create_command)

        walker_result = carla_client.apply_commands_sync(batch_commands)

        walker_actor_ids = []

        for i in range(len(walker_result)):
            if walker_result[i].error:
                logging.error(walker_result[i].error)
            else:
                walker_actor_ids.append(walker_result[i].actor_id)

        batch_commands = []

        walker_controller_blueprint = carla_client.get_walker_controller_blueprint()

        for i in range(len(walker_actor_ids)):
            walker_controller_create_command = carla_client.command_spawn_actor(walker_controller_blueprint, carla.Transform(), walker_actor_ids[i])
            batch_commands.append(walker_controller_create_command)

        controller_result = carla_client.apply_commands_sync(batch_commands)

        for i in range(len(controller_result)):
            if(controller_result[i].error):
                logging.error(controller_result[i].error)
            else:
                full_walker = Walker(walker_actor_ids[i], controller_result[i].actor_id)
                walkers.append(full_walker)

        carla_client.wait_for_tick()

        world.set_pedestrians_cross_factor(percentagePedestriansCrossing)

        for i in range(0, len(walkers)):
            walker = walkers[i]

            actor = carla_client.get_actor(walker.actor_id)
            controller  = carla_client.get_actor(walker.controller_id)
            controller.start()

            #controller.go_to_location(carla_client.get_random_location_from_navigation())

            walker.set_actor(actor)
            walker.set_controller(controller)

    except:
        DespawnPedestrians(carla_client, walkers)

    return walkers


def SpawnPedestriantsWithTargets(carla_client):

    num_agents = 1
    walkers = []

    try:

        world = carla_client.get_world()

        percentagePedestriansCrossing = 0.0

        spawn_points = []
        batch_commands = []

        walker_blueprints = carla_client.get_all_walker_blueprints()

        for i in range(num_agents):
            spawn_point = carla.Transform()
            loc = carla_client.get_random_location_from_navigation()
            if(loc!= None):
                spawn_point.location = loc
                walker_blueprint = random.choice(walker_blueprints)
                walker_create_command = carla_client.command_spawn_actor(walker_blueprint, spawn_point)
                batch_commands.append(walker_create_command)

        walker_result = carla_client.apply_commands_sync(batch_commands)

        walker_actor_ids = []

        for i in range(len(walker_result)):
            if walker_result[i].error:
                logging.error(walker_result[i].error)
            else:
                walker_actor_ids.append(walker_result[i].actor_id)

        batch_commands = []

        walker_controller_blueprint = carla_client.get_walker_controller_blueprint()

        for i in range(len(walker_actor_ids)):
            walker_controller_create_command = carla_client.command_spawn_actor(walker_controller_blueprint, carla.Transform(), walker_actor_ids[i])
            batch_commands.append(walker_controller_create_command)

        controller_result = carla_client.apply_commands_sync(batch_commands)

        for i in range(len(controller_result)):
            if(controller_result[i].error):
                logging.error(controller_result[i].error)
            else:
                full_walker = Walker(walker_actor_ids[i], controller_result[i].actor_id)
                walkers.append(full_walker)

        carla_client.wait_for_tick()

        world.set_pedestrians_cross_factor(percentagePedestriansCrossing)

        for i in range(0, len(walkers)):
            walker = walkers[i]

            actor = carla_client.get_actor(walker.actor_id)
            controller  = carla_client.get_actor(walker.controller_id)
            controller.start()
            controller.go_to_location(carla_client.get_random_location_from_navigation())

            walker.set_actor(actor)
            walker.set_controller(controller)

        while True:
            world.wait_for_tick()
    finally:

        batch_commands = []

        for i in range(len(walkers)):
            walker_actor =  carla_client.get_actor(walkers[i].actor_id)
            controller_actor = carla_client.get_actor(walkers[i].controller_id)

            delete_walker_command = carla_client.command_delete_actor(walker_actor)
            delete_controller_command = carla_client.command_delete_actor(controller_actor)
            batch_commands.append(delete_walker_command)
            batch_commands.append(delete_controller_command)

        carla_client.apply_commands_sync(batch_commands)


def DespawnPedestrians(carla_client, walkers):

    batch_commands = []

    for i in range(len(walkers)):
        walker_actor =  carla_client.get_actor(walkers[i].actor_id)
        controller_actor = carla_client.get_actor(walkers[i].controller_id)
      
        delete_walker_command = carla_client.command_delete_actor(walker_actor)
        delete_controller_command = carla_client.command_delete_actor(controller_actor)
      
        batch_commands.append(delete_walker_command)
        batch_commands.append(delete_controller_command)
    
    carla_client.apply_commands_sync(batch_commands)

