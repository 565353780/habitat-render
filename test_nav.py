#!/usr/bin/env python
# -*- coding: utf-8 -*-

agent = sim.initialize_agent(sim_settings["default_agent"])

agent_state = habitat_sim.AgentState()
agent_state.position = np.array([-0.6, 0.0, 0.0])
agent.set_state(agent_state)

agent_state = agent.get_state()
print("agent_state: position", agent_state.position, "rotation", agent_state.rotation)

action_names = list(cfg.agents[sim_settings["default_agent"]].action_space.keys())
print("Discrete action space: ", action_names)

display = True

def navigateAndSee(action=""):
    if action not in action_names:
        return False
    observations = sim.step(action)
    print("action: ", action)
    if display:
        display_sample(rgb_obs=observations["color_sensor"],
                       depth_obs=observations["depth_sensor"])

for _ in range(100):
    action = action_names[randint(0, len(action_names) - 1)]
    navigateAndSee(action)

