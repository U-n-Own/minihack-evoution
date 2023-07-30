"""
main file where we generate the room environment and where we complete the task
using the information passed by the genetic algorithm 
"""

import gym
import minihack
import numpy as np
import random
from typing import List
from utility_func import print_room, search_environment_indexes, search_environment_agent_position, search_environment_goal_position
from utility_func import step_dictionary, movement_dictionary
from rules import Rule, generate_initial_population
from fitness_func import find_distance_grid, fitness_function
from genetic_algorithm import genetic_algorithm

def main():

    #Generate a new environment and save the describtions arrays in obs
    env=gym.make(
        "MiniHack-Room-Random-15x15-v0",
        observation_keys=("chars", "colors", "specials", "pixel"),
    )

    obs = env.reset() 
    env.render() #Print the room 

    i,j = search_environment_indexes(obs['chars'])

    #print the matrix in ASCII characters. 
    print("Tha matrix in ASCII that represent the random room is:")
    print_room(obs['chars'][i:i+15, j:j+15])

    #find the agent position and the goal position in the room    
    x_agent_position, y_agent_position = search_environment_agent_position(obs['chars'][i:i+15, j:j+15])
    x_goal_position, y_goal_position = search_environment_goal_position(obs['chars'][i:i+15, j:j+15])
    
    print("The agent position is: ", x_agent_position, " ",  y_agent_position)
    print("The goal position is: ", x_goal_position, " ", y_goal_position)

    #matrix that calculates the distance of each position from the goal
    distance_grid=find_distance_grid(x_goal_position, y_goal_position)

    
    #generate a size_of_population of rules that we insert into a list
    population = generate_initial_population(number_of_population=10)

    #associate each rule with a score given by the fitness function
    fitness_func=[]
    for x in range(len(population)):
        score=fitness_function(population[x], distance_grid)
        fitness_func.append(score)
    
    print("Regola 1:")
    population[0].print_rule()
    print("Regola 2:")
    population[1].print_rule()
    print("Fitness funciton:")
    print(fitness_func)

    population, fitness_func, average_fitness_func = genetic_algorithm(distance_grid,
                                                                       population,
                                                                       fitness_func,
                                                                       number_of_population=10,
                                                                       chance_for_mutation=0.05,
                                                                       number_of_generation=10)
    
    print("Nuova regola 1:")
    population[0].print_rule()
    print("Nuova regola 2:")
    population[1].print_rule()
    print("Nuova fitness funciton:")
    print(fitness_func)
    print("Average Fitness:")
    print(average_fitness_func)
    

    #index_list_of_score=sorted(range(len(fitness_func)), key=lambda k: fitness_func[k], reverse=True)
    #fitness_func.sort(reverse=True)
    #print(index_list_of_score)
    #print(fitness_func)
    #list_of_rules[index_list_of_score[0]].print_rule_movement()
    #list_of_rules[index_list_of_score[0]].print_rule_arrow()
    
    
    
    '''
    movements=list_of_rules[index_list_of_score[0]]
    step=0

    while x_agent_position!=x_goal_position and y_agent_position!=y_goal_position:
        
        env.step(movements.rules_grid[x_agent_position][y_agent_position])
        x_agent_position=x_agent_position+movement_dictionary[step_dictionary[movements.rules_grid[x_agent_position][y_agent_position]]][0]
        y_agent_position=y_agent_position+movement_dictionary[step_dictionary[movements.rules_grid[x_agent_position][y_agent_position]]][1]

        step=step+1
        print_room(obs['chars'][i:i+15, j:j+15])
    '''


if __name__ == "__main__":
    main()