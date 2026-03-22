SUPPORTED_DEVICES = {
    # While there is no reason that any microcontroller can be successfully used, these are the ones that the program specifically searches for when it starts. 
    # Most (if not all) microcontrollers that are capable of loading the firmware located in 'firmware/' should be capable of running this, provided they are added below.

    # Arduino Uno (3/21/26)
    (
        0x2341, # vid
        0x0043 # pid
    ): 'Arduino Uno',
}