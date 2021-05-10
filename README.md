# ChessAI

Repository containing Chess Engine and ML Model

## TODO
### **Wasif**
- Set up cnn/RNN/RNN,CNN/Greedy/Greedy+exploit
  - implement `_train` methods
  - `raw_data_to_datapoint` function in `data_extractor.py` and `generate_datapoint(moves)` in `ai.py`
- implement `predict_move`
- #### MILESTONE 1.5 base smart AI done
- Move w.r.t. various reward functions  
- Set up qlearning (links game to models>)
- Train/Test
- IReinfLearn to learn reward
#### MILESTONE 2: **Smart AI done**
- Write monitoring scripts
- Try other networks
- Tweak qlearning rewards

### **Ali**
- unit tests for board and game
- Write actual integration tests (one for why moves needs to be updated after each move)
  - i think it only needs tobe updated before a king moves
- Implement king movement
- enpassant/castle/promote
- check/checkmate
- Something wrong:
  - with the square 0,0
  - pawn capture pawn 2,5 -> 1,6
- write 2 system tests
- implement scoreboard + visualization
  - db contains `players`=(ID,name) and `scores`=(ID,ID, score)
- type documentation
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
