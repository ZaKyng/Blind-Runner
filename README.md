# Blind Runner

## Overview

**Blind Runner** is a 2D side-scrolling platformer built around memory, spatial awareness, and risk.  
The core mechanic removes visual information while the player is moving, forcing them to **memorize the level layout** and navigate blindly.

The game is developed in **Python using Pygame** and includes a custom-built internal node-based library (**ZaKnode**) designed to simplify and structure 2D game development.

---

## Core Idea

You control a character running and jumping through levels toward a predefined goal.

- The player **spawns at a fixed location** in each level.
- **When the player moves**, the entire level (except the player and background) **disappears**.
- **When the player stops**, the level becomes visible again.
- Movement is therefore blind — you never see where you are going.
- The camera is **static** to make spatial orientation easier.
- Every few levels, a **new mechanic, element, or enemy** is introduced.
- Enemies **cannot be killed** and must be avoided.
- Upon death (enemy collision or other causes):
  - The player briefly sees the reason for death.
  - The player respawns at the spawn point.
- User data (statistics, progress, collectibles) is stored in `.txt` files.

---

## Objective

Each level has a **visible target location**.

The **only goal** is to reach it.

---

## Visual Design

- **Pixel art**, 2D side view (similar to *Hollow Knight*)
- Levels are built from **square tiles on a grid**
- Player, enemies, and moving elements:
  - Spawn on the grid
  - Move freely outside the grid
- Every few levels:
  - Color palette or visual style changes to indicate progression
- Minimal focus on story

---

## Art & Assets

- Custom-made **UI sprites**
- Custom **side-view sprite sheets**
- Static custom background art
- Original sprite sheets for:
  - Player
  - Enemies
  - Animated level elements

---

## Level Editor

Players can create and edit their own levels.

Features:
- Full access to all level elements
- Editable spawn and goal positions
- Levels are saved as `.txt` files
- Custom levels appear in a UI tab (e.g. **Custom Levels**)
- Levels are loaded from a folder such as `user_levels`
- Levels can be shared simply by copying files
- Default game levels:
  - Also stored as `.txt`
  - Located in a protected folder (e.g. `default`)
  - Not editable through the UI
- Custom levels can be:
  - Edited later
  - Overwritten
  - Saved as entirely new levels

---

## Planned / Optional Features (If Time Allows)

### Weapon System
- Optional weapon per level
- Allows limited defense
- Not part of the core gameplay (default gameplay requires avoiding enemies)

### Surface Types
Special terrain with gameplay effects:
- **Sand** – slows movement
- **Ice** – slippery movement
- Visual effects appear while moving:
  - Sand dust
  - Ice particles
- Effects remain visible even during movement so the player knows what surface they are on

### Collectibles
Two possible approaches:
- Rare collectible figurines:
  - Appear once every few levels
  - Can only be collected once
  - Stored permanently in player `.txt` data
  - Accessible via a **Gallery** menu
- OR:
  - Each level contains **3 visible stars**
  - Goal is to collect all stars and finish as fast as possible

### Larger & More Interactive Levels
- Doors that teleport the player to another area within the same level
- Buttons and switches affecting distant parts of the level
- More complex, interconnected level design

---

## How to Start

### Requirements
- Python **3.13**
- `pip`

### Installation

1. Locate the latest `.whl` file in the `/dist` folder  
2. Copy it into an empty directory anywhere on your system  
3. Open a terminal in that directory  

Install:
```bash
pip install name-of-the-file.whl
```

Update/reinstall:
```bash
pip install --force-reinstall name-of-the-file.whl
```

### Running

Library showcase:
```bash
python -m ZaKnode
```

Game:
```bash
python -m blindrunner
```

---

## DEVELOPER NOTE (Updated 3. 3. 2026)
The ZaKnode showcase is now the same as the game. While the library is being reworked, game won't me updated much. 
If you clone this repository, you will find my previous progress.

Previous development stages can be explored in:
- `archive/`
- `archive/failed`
  
To see the last version of the old node system before restarting:
```bash
python -m archive.failed.test1_fail
```
