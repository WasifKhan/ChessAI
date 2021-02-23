from run_manual import run_manual
from test_suite.test_pawn import test_pawn


if __name__ == '__main__':
    while (user_input := input('\n1 for tests, 2 for manual: ')) not in {'1', '2'}:
        print('please enter a valid command')
    
    if user_input == '1':
        test_pawn()
    elif user_input == '2':
        run_manual()
