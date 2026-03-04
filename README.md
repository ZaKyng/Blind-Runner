# Readme here:

# Jumping 2D game

2D jumping game. When you are moving, the screen excluding player goes black and when stopped (not moving) you see.
You just have to memorise the level ahead. That's the main idea.
Contains a 2D game library for easier use in pygame (I have created special class nodes that depend on each other and work together in a lot of ways).


# How to start?

Requirements

- Python 3.13
- pip

1. Install latest .whl file in /dist/ folder. (Last update: 4. 3. 2026)
2. Put it in an empty folder anywhere on your device.
3. Open Terminal in that folder.
   
Run:

    pip install *name-of-the-file.whl
        or (if you already installed it) update
    pip install --force-reinstall *name-of-the-file.whl
    
        To run
    python -m ZaKnode
        (for ZaKnode library showcase)
    python -m blindrunner
        (for the game itself)

# Updated developer comment (4. 3. 2026)

ZaKnode library showcase is the same as the game, because I am in process of redoing the node logic. You can explore my progress in the archive folder, and mainly in failed folder inside. If you run "python -m archive.failed.test1_fail", you will see how far with the node system I came before starting over.