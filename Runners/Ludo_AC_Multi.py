import os

import numpy as np
from tqdm import tqdm

from Agents.A2CAgent import Agent
from Boards.Full_Board import FullBoard


def choose_rand(a):
    return np.random.choice(a)


def run_game(num_ep, model_output):
    env = FullBoard()
    agent0 = Agent(n_actions=env.action_size(), input_dim=env.state_size(), alpha=1e-8)

    agent0_reward = []
    agent1_reward = []
    agent2_reward = []
    agent3_reward = []
    episode_length = []

    output_dir_a = 'model_output/A2C/%s/actor/' % model_output
    output_dir_c = 'model_output/A2C/%s/critic/' % model_output

    if not os.path.exists(output_dir_a):
        os.makedirs(output_dir_a)
    if not os.path.exists(output_dir_c):
        os.makedirs(output_dir_c)

    for ep in tqdm(range(0, num_ep), ascii=True, unit="e"):
        step = 0
        s, _, game_over, player_turn = env.reset()
        episode_reward = [0.0, 0.0, 0.0, 0.0]
        while not game_over:
            env.roll_dice()
            action_list = env.get_next_states(player_turn)

            if action_list:
                # if player_turn > -1:
                if player_turn % 2 == 0:
                    s_t = env.convert_state(player_turn)
                    action, _ = agent0.act(s_t, action_list)
                else:
                    action = choose_rand(action_list)

                s_, reward, game_over, player_turn_temp = env.make_step(action)

                # if player_turn > -1:
                if player_turn % 2 == 0:
                    s_t_ = env.convert_state(player_turn)
                    agent0.learn(s_t, action, reward[player_turn], s_t_, game_over)

                episode_reward[player_turn] += reward[player_turn]

                player_turn = player_turn_temp
                step += 1
            else:
                player_turn = (player_turn + 1) % 4

            if game_over:
                agent0_reward.append(episode_reward[0])
                agent1_reward.append(episode_reward[1])
                agent2_reward.append(episode_reward[2])
                agent3_reward.append(episode_reward[3])
                episode_length.append(step / 4)

        if ep > 1000:
            agent0.reduce_alpha()

        if ep % 100 == 0:
            print(np.average(agent0_reward[-1000:]), np.average(agent1_reward[-1000:]))

    return [agent0_reward, agent1_reward, agent2_reward, agent3_reward, episode_length]
