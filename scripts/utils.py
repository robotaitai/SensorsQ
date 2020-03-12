
def check_user_input(exit_program):


    var = ""
    while not exit_program:
        var = input("")
        exit_program = (var == 'q' or var == 'Q')

