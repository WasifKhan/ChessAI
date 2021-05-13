# ChessAI

Repository containing Chess Engine and ML Model

## TODO
### **Wasif**
- each piece stores a dict `move_IDs` containing `move_ID:lambda destination`
- everyitmeca piece moves, `piece.move()` :(updates location) + seaches the moves dict for `destination` and outputs the appropriate `move_ID` - **FINISH GENERATE DATAPOINT**
- `piece.get_move(prediction,board,piece)->(source,destination)` : simply search `move_ID`(declared in fn) in `piece.moveIDs` and output `(piece.location-int, piece.moveIDs[moveID]` **FINISH PREDICTION TO MOVE**
- fill `MOVES` dictionary
- test without the data concertion bug to see if learning is working properly
- Help Ali
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
- implement promote/check/checkmate
- unit tests for board and game
- Write actual integration tests (one for why moves needs to be updated after each move)
  - i think it only needs tobe updated before a king moves
- Something wrong:
  - with the square 0,0(UI)
  - pawn capture pawn 2,5 -> 1,6(backend)
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
