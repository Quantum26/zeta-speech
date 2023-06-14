from os import get_terminal_size

def clear_terminal_line(end='\r'):
    columns, _ = get_terminal_size()
    print('', end='\r')  # return cursor to beginning
    print(' ' * (columns - 1), end=end)  # Fill line with spaces
    
def print_sl(msg):
    clear_terminal_line()
    print(msg, end='\r')