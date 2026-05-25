SUPPORTED_DEVICES = {
    # While technically any microcontroller be successfully used, these are the ones that the program specifically searches for when it starts. 
    # Most (if not all) microcontrollers that are capable of loading the firmware located in 'firmware/' should be capable of running this, provided they are added below
    # to the list of microcontrollers to search for.

    # Simply find the vid/pid online of the given microcontroller and add it below given the examples and it should be found when running main.py.

    # Arduino Uno (3/21/26)
    (
        0x2341, # vid
        0x0043 # pid
    ): 'Arduino Uno',
}