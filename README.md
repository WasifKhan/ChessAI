# ChessAI

Repository containing Chess Engine and ML Model

## TODO
### **Wasif**
- only process games rank 1.8k and above
- weight each datapoint based on how many other datapoints we have in this state (if many, weight is less)
- ake board from 1x1->3x3
- loggers
- finish cnn
  - prediction=max(nn=softmax activation of final layer)
  - tweak rewards to see best one-prioritize defense
  - try 18 architectures {space,avg,dense}layer x {1,2,3}layers x {sigmoid, relu}activations
  - custom loss functions
- make data extracyor a subclass of ai
- clean up ai logic
- #### MILESTONE 1.5 base smart AI done
- Set up RNN/cnnRNN,CNN/Greedy/Greedy+exploit
- Move w.r.t. various reward functions  
- Set up qlearning (links game to models>)
- Train/Test
- IReinfLearn to learn reward
#### MILESTONE 2: **Smart AI done**

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
