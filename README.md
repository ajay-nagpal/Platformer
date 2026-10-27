# Platformer

A fully functional **Platformer** game built with **Python** and **Pygame**, featuring smooth player animation, gravity-based physics, jumping mechanics, grid-based level design, moving platforms, collision detection, enemies, collectible coins, scoring, sound effects, background music, and a level progression system.

---

## Features

- Smooth player movement with left and right directional controls.
- Animated player sprites with separate animations for both directions.
- Gravity-based physics with jumping mechanics.
- Grid-based level design using JSON files.
- Horizontally and vertically moving platforms.
- Collision detection with blocks, moving platforms, enemies, lava, coins, and exits.
- Coin collection with live score tracking.
- Enemy and lava collisions that trigger the game-over state.
- Background music with jump, coin collection, and game-over sound effects.
- Level progression by reaching the exit.
- Restart functionality to play again after game over.

---

## Controls

| Key | Action |
|------|--------|
| **← Left Arrow** | Move the player left |
| **→ Right Arrow** | Move the player right |
| **Spacebar** | Jump |

---

## Game Design

### Player

The player is animated using multiple sprite images to create smooth movement in both directions. Gravity continuously pulls the player downward, while pressing the **Spacebar** allows the player to jump. The player can move left and right to navigate the level, avoid obstacles, and reach platforms.

---

### World and Level Design

The game world is designed using a grid-based layout, where each cell represents a block or game object. Level layouts are stored in JSON files, allowing different levels to be created and modified by changing the grid data.

Different grid values represent solid blocks, grass, enemies, moving platforms, lava, coins, and exits.

---

### Moving Platforms

Moving platforms travel horizontally or vertically across the level. Each platform uses a movement direction and counter to control its motion. When a platform reaches its movement limit, its direction reverses.

The player must time jumps and landings carefully to navigate these platforms and progress through the level.

---

### Collision Detection

The game uses **rectangle-based collision detection** to determine when the player interacts with objects in the world. Collision checks prevent the player from passing through solid blocks and handle landing and head collisions during jumps.

Additional collision checks detect interactions with moving platforms, enemies, lava, coins, and exits.

---

### Scoring

The score increases by one each time the player collects a coin. Once collected, the coin disappears from the level, and a sound effect plays to provide feedback. The current score is displayed during gameplay.

---

### Level Progression

Each level contains an exit that the player must reach to complete the level. Level layouts are loaded from JSON files, allowing new levels to be designed without changing the core game logic.

---

### Game Over

Colliding with an enemy or lava triggers the game-over state. A game-over sound effect plays, and the player can use the restart functionality to try again.

---

### Sound Effects

The game includes background music and sound effects for jumping, collecting coins, and game over. Background music plays during gameplay, while individual sound effects provide audio feedback for important events.

---

### Restart

The restart functionality allows the player to start again after game over. The game resets the player and reloads the level, allowing another attempt at completing the platforming challenges.

---