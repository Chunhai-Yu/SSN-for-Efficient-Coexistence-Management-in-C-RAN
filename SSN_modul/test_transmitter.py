import sys

a_on='11010101'
b_on='10111111'
NUM_ATTEMPTS=100

def transmit_code(code):
    print(code)
    print(NUM_ATTEMPTS)












if __name__ == '__main__':
    exec('NUM_ATTEMPTS=25*int(sys.argv[1])') # sys.argv[1]: /seconds
    exec('print(NUM_ATTEMPTS)')
    for argument in sys.argv[2:]:
        exec('transmit_code(' + str(argument) + ')')