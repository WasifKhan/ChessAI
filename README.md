# ChessAI

Repository containing Chess Engine and ML Model

## TODO
### **Wasif**
- **solution to loss problem of passing in board:**
  - current prediction is 142 array of 0s with 1 non-zero entry. simply change all these values to *some notion* of board value, most simple is just `board.value`. complex finsih with using #attacks-#attacked?....MSE loss is OK, but then don't softmax last layer..use sigmoid
- clean backend/parser
- #### MILESTONE 1.5 base smart AI done
- Set up cnn/RNN/RNN,CNN/Greedy/Greedy+exploit
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
- write 2 system tests
- implement scoreboard + visualization
  - db contains `players`=(ID,name) and `scores`=(ID,ID, score)
- type documentation
- optimizations
  - change coordinate system to 2-digit int
  - remove `if x.is_white: ... else: ...` by inverting board at start/end of code
- write AI - X-d,All-b=2s thinking time
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
