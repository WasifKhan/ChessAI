# ChessAI

Repository containing Chess Engine and ML Model

## TODO
### **Wasif**
- ~~Split testing into unit and integration tests~~
- ~~Get unit testing frameworks together~~
- ~~get baseline interface going (link game with view through `interface.py`~~)
- ~~Write AI class (to play with humans/vs other AI=interat with game class)~~
- get unit test framework for board/game going
- #### MILESTONE 1: **Dumb AI done**
- Map datapoints to our coordinates
- Set up various models(fix datapoint mapping)
- Move w.r.t. various reward functions
- Set up qlearning (links game to models>)
- Train/Test
- Link intelligent weights to AI class
#### MILESTONE 2: **Smart AI done**
- Write monitoring scripts
- Try other networks
- Tweak qlearning rewards

### **Ali**
- ~~Finish all possible moves~~
- ~~Unit test pieces~~
- unit tests for board and game
- Write actual integration tests
- Implement king movement
- enpassant/castle/promote
- check/checkmate
- write 2 system tests
- optimizations
  - change coordinate system to 2-digit int
  - remove `if x.is_white: ... else: ...` by inverting board at start/end of code

#### MILESTONE 1: **Done backend**
- Start frontend
- Write Controller to interact Model and View
- Write Buttons for View
#### MILESTONE 2: **Frontend done**
- Optimize backend
- User-friendly Frontend

### **Zuraze**
- Lose to AI

### Project Complete
