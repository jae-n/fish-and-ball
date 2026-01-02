# Fish and Ball

A compact Python playground demonstrating a simple multi-agent/learning scenario:

- A controllable Ball (RL agent) that learns via a DQN-style loop to chase and eat Fish.
- A population of Fish that evolve across episodes using small genomes (per-fish parameters) and simple evolutionary operators.

This repository is intended for experimentation: tune `config.py`, run headless experiments, and observe whether fish genomes adapt to avoid the Ball.

---

## How it works (high level)

- Ball (agent): a discrete-action agent (up/down/left/right) that receives a state vector and is trained with DQN-style updates. Environment rewards include small survival/distance components and a larger `REWARD_EATEN` when the Ball collides with a Fish.
- Fish (population): each `Fish` carries a small genome with behavioral parameters:
	- `perception_radius` — how far it detects the Ball
	- `panic_multiplier` — scales extra speed when Ball is approaching
	- `flee_speed` — baseline flee speed
	- `max_speed` — top movement speed for the fish
	- `steering_smoothness` — how smoothly the fish steers toward the flee direction

- During an episode each Fish accumulates `fitness` (combining survival and distance from the Ball) and `age` (steps survived). When the episode ends the environment uses elitism + tournament selection + Gaussian mutation to produce the next generation. If all fish die, the longest-lived dead fish's genome is used to seed the next population.

Key implementation files:
- `main.py` — training loop, ties together `GameEnvironment`, `Agent`, `Renderer`, and `StatisticsTracker`.
- `GameEnvironment.py` — environment step/reset logic, fish behavior, collision handling, evolution.
- `entity.py` — `Ball` and `Fish` classes (Fish now own their genome, fitness, and age).
- `agent.py` — DQN agent implementation used to control the Ball.
- `utills.py` — model saving/loading and `StatisticsTracker` utilities.
- `collision_detector.py` — collision helper functions.

---

## Requirements

- Python 3.8+
- Recommended packages: `pygame`, `numpy`, `torch` (PyTorch). You can add these to a `requirements.txt`.

Install (recommended in virtualenv):

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install pygame numpy torch
```

---

## Run

- Interactive (with rendering):

```powershell
python main.py
```

- Headless / batch experiments (faster):
	- Edit `config.py` and set `RENDER_GAME = False`.
	- Optionally disable `BALL_AUTO_CHASE` for a harder RL task.

---

## Configuration

All tunable parameters live in `config.py`. Important groups:

- Ball: `BALL_SPEED`, `BALL_MAX_SPEED`, `BALL_AUTO_CHASE`, `BALL_CHASE_STRENGTH`.
- Fish/evolution: `FISH_MUTATION_RATE`, `FISH_MUTATION_SCALE`, `FISH_GENOME_ELITISM`, `FISH_TOURNAMENT_SIZE`, `FISH_MUTATION_DECAY`, `FISH_PERCEPTION_MIN/MAX`, etc.
- Rewards: `REWARD_SURVIVAL`, `REWARD_EATEN`, `REWARD_DISTANCE_MULTIPLIER`.
- Rendering / training: `RENDER_GAME`, `SAVE_MODEL_EVERY_N_EPISODES`, `VERBOSE`.

Tune these to adjust selection pressure, mutation noise, and task difficulty.

---

## Logging and statistics

- `utills.StatisticsTracker` collects episode-level statistics. There is support for recording per-generation genome summaries; to persist generation stats, call `stats_tracker.record_generation(env.generation, env.genomes)` in `main.py` after `env.reset(...)`.
- Models (agent checkpoints) are saved via `utills.ModelManager.save_model()` when configured in the main loop.

---

## Troubleshooting

- If nothing appears to learn:
	- Run headless experiments (`RENDER_GAME = False`) to speed up training.
	- Ensure `REWARD_EATEN` is large enough to provide learning signal to the Ball.
	- Verify the agent's training loop is running (replay and optimizer calls).

- If `pygame` is missing, install it with `pip install pygame`.

---

## Next steps (suggestions)

- Add `requirements.txt` to make setup reproducible.
- Hook `stats_tracker.record_generation(...)` into `main.py` for automatic per-generation logging to disk.
- Add small unit tests for collision logic, mutation/clamping, and `reset()` selection behavior.
- Run headless experiments (e.g., 100 episodes) and plot genome means over generations to verify adaptation.

If you want, I can add `requirements.txt`, update `main.py` to persist generation stats automatically, or run a short headless experiment and return a summary of genome trends.