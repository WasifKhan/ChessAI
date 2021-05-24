# ChessAI

Repository containing Chess Engine and ML Model

## TODO
### **Wasif**
- change input to be:
  - 5 neurons per piece(5 8x8 layers)
  - 1= under attack (sum of enemy atks
  - 2= possible defends(sum of defends)
  - 3= possible threats(sum of attacking enemy)
  - 4= possible moves
  - 5=value of piece
- try 9 architectures:
  - {sparse, avg, dense} neurons per layer
  - 1,2,3} hidden layers
- graph various architecture performances
- smart CNN= 3 networks:
  - 1- piece should move -binary
  - 2- piece best move - categorical
  - 3- pieces vote best move - categorical
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
