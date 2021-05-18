# ChessAI

Repository containing Chess Engine and ML Model

## TODO
### **Wasif**
- clean backend/random AI no errors
  - Something wrong w/ pawn movement!
  - only-need-`piece.is_white is not self.is_white:`-in-pawn-apture-sine-board-returns-none-on-negatiev-indicies.-also-dont-need-to-divide into 3 separatecases
- board input is wrong...need to distinguish bishop and knight... simply numbers are no good
- clean `parser`
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
