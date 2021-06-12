# ChessAI

Repository containing Chess Engine and ML Model

## TODO
### **Wasif**
- compare separated vs non-separated network
- clean memory file
- get gpu acceleration
- tweak rewards (inputs) to see best one-prioritize defense
- custom loss function (outputs) to capture more chess strategy
- #### MILESTONE 1.5 base smart AI done
- Set up RNN/cnnRNN,CNN/Greedy/Greedy+exploit
- Move w.r.t. various reward functions  
- Set up qlearning (links game to models>)
- Train/Test
- IReinfLearn to learn reward
#### MILESTONE 2: **Smart AI done**
- Submit to Lichess

### **Ali**
- unit tests for board and game
- Write actual integration tests (one for why moves needs to be updated after each move)
  - i think it only needs tobe updated before a king moves
- write 2 system tests
- implement scoreboard + visualization
  - db contains `players`=(ID,name) and `scores`=(ID,ID, score)
- type documentation + doc strings
- optimizations
  - change coordinate system to 2-digit int
  - remove `if x.is_white: ... else: ...` by inverting board at start/end of code
- write AI - X-d,All-b=2s thinking time
#### MILESTONE 1: **Done backend**
- Start frontend
- Write Controller to interact Model and View
- Write Buttons for View
#### MILESTONE 2: **Frontend done**

### **Zuraze**
- Lose to AI

### Project Complete
