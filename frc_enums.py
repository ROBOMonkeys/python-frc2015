from XboxButton import XboxButton as button


class XboxButton():
    '''
    A shell class for easy reference to the Xbox button values
    '''
    A = 1
    B = 2
    X = 3
    Y = 4
    L_bump = 5
    R_bump = 6
    start = 7
    select = 8


class XboxButtons(XboxButton):
    '''
    An empty class that just inherits XboxButton's variable names

    Contains button objects instead of just numbers
    '''
    def __init__(self):
        super().__init__()


class XboxAxis():
    '''
    A shell class for easy reference to the Xbox axes values
    '''
    R_X = 0
    R_Y = 1
    L_X = 4
    L_Y = 5
    Z_D = 2
    Z_U = 3


# when called with a controller object it iterates through
#  all of the variables in the XboxButton class and sets
#  the equivilant variable to a button type (with poll func)
#  in the empty XboxButtons class
def init_buttons(controller):
    # for every attribute in XboxButton
    for attr in dir(XboxButton):
        # if it isnt a function, and if it's name doesnt
        #  start with two underscores
        if not callable(attr) and not attr.startswith('__'):
            # set the equivilant attribute in XboxButtons with
            #  a button object
            setattr(XboxButtons,
                    attr,
                    button(controller,
                           getattr(XboxButton, attr)))
