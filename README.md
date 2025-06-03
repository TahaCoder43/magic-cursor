# Introduction
This program is able to do actions in games using just the cursor, right now supported games are geometry dash lite on web and edge://surf (microsoft edge offline game). 

It can also control the mouse, clickinng works fine but moving the mouse is really sketchy (unusable) it jitters a lot, and when code is written to counter that then it regards movement as jitter

## What about low spec laptops

It runs on my laptop with 

- Nixos Linux (Windows is not supported but it should not be hard to implement)
- Intel i5 2520M (integrated GPU intel HD graphics 3000)
- 4GB RAM
- SSD (used for swap)

but even when running a low-end game with this program (like microsoft edge offline sufing game), the hand detection starts lagging behind so it starts detecting your gestures 2-3+ seconds after you make them


