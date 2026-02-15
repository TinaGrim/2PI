# 2PI Game

A pygame-based 2D game with tile-based maps and player movement system.

## Description

2PI is a 2D game built with Python and Pygame that features:
- Player-controlled character with physics-based movement
- Camera system that follows the player
- Tile-based map rendering using Tiled TMX format
- NPC system with automatic spawning
- Boost mechanic for faster movement

## Features

- **Player Movement**: Arrow keys to move, Left Shift to boost
- **Physics System**: Realistic acceleration, velocity, and friction
- **Camera System**: Smooth camera following with boundary constraints
- **Tile Maps**: Uses pytmx for loading and rendering Tiled maps
- **NPC System**: NPCs spawn automatically every second
- **Collision Detection**: Wall collision boundaries

## Requirements

```
pygame
pytmx
```

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```bash
   pip install pygame pytmx
   ```
3. Make sure you have the following directory structure:
   - `Font/` - Contains LuckiestGuy.ttf font file
   - `img/` - Contains player.png sprite
   - `tmx/` - Contains map.tmx tilemap file
   - `tsx/` - Tileset files
   - `export/` - Export directory

## Usage

Run the game:
```bash
python 2PI.py
```

## Controls

- **Arrow Keys**: Move player (Up, Down, Left, Right)
- **Left Shift**: Boost (increases movement speed by 1.5x)

## Game Classes

- **Base_Player**: Base class for all player entities with movement and rendering
- **Player**: Playable character with boost ability and physics-based movement
- **NPC**: Non-playable characters that move automatically
- **Camera**: Camera system that follows the player
- **TileMap**: Handles tile-based map rendering
- **TwoPI**: Main game class managing game loop and initialization

## Technical Details

- Screen Resolution: 2500x1400
- Target FPS: 60
- Tile Size: 256x256 pixels
- Player Sprite: 400x200 pixels

## License

This project is open source and available for use.