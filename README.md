Game Overview:
You control a character in a maze, trying to reach the goal. The game runs in loops of N seconds or N moves (e.g., 10 moves per loop).
At the end of each loop, the maze resets, but your past actions are replayed by an “echo” (a ghost copy of your character).
Echoes can: Press switches,  Block enemies,  Hold doors open,  Distract patrolling guards 
(one must collaborate with your own past echoes to solve increasingly complex puzzles)


Puzzle Rules:
    1. Maze Reset Mechanic:
        Every 20 seconds, the maze resets to its initial state.
        The player returns to the start, and a ghost (echo) appears where they left off.

    2. Echo Mechanic:
        Echoes retrace your last loop's path (every movement: up/down/left/right).
        Echoes can:
            Press buttons, open gates, or block traps.
            Be interacted with buttons and doors, walls (e.g., pushed or avoided).
            Cause a failure if touched (optional for challenge mode).

    3. Movement: 
        Grid-based movement: 1 tile per arrow key input.
        No diagonal moves.

    4. Obstacles:
        Static walls (always present).
        Timed gates (open when a button is pressed).
        Traps (active unless an echo deactivates them).
        Checkpoints (optional).



Win Condition:
Reach the exit tile after at least one time loop (so that echoes help you).
Some puzzles require echoes to trigger buttons to allow access to the exit.


Lose Conditions:
Failing to reach the exit in limited number of loops (e.g., max 5 loops).
Being killed by traps (spikes, crushers, etc.).
Colliding with your own echo (in challenge mode).


Replayability Notes:
    Randomly generated mazes.
    Optional modes:
        Ghosts hurt you (hard mode).
        Multiple ghosts.
        Time countdown shortened.



Technologies Used:
    Python 3.11.0 – Core programming language for game logic and structure
    Pygame – 2D game development library for rendering graphics, handling input, and managing game loops
    Git & GitHub – Version control and collaboration
    VS Code – Preferred code editor for development

    Tiled Map Editor (optional) – For designing tile-based maze levels visually
    NumPy (optional) – For matrix/grid manipulation or complex puzzle logic
    Audacity or Bfxr (optional) – For creating sound effects and audio cues

