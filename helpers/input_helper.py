import getpass
import queue
import threading

inputQueue = queue.Queue()

def keyboard_input(inputQueueObj):
    """ Get keyboard input, uses getpass so input isn't echoed back

    """
    while (True):
        try:
            input_str = getpass.getpass("")
            inputQueueObj.put(input_str)
        except KeyboardInterrupt:
            inputQueueObj.put("\x03")

def input_init():
    """ Creates thread for keyboard_input()

    """
    global inputQueue

    inputThread = threading.Thread(target=keyboard_input, args=(inputQueue,), daemon=True)
    inputThread.start()

def check_input():
    """ Get the latest input

        :returns:
            Latest input from queue
    """
    global inputQueue
    if (inputQueue.qsize() > 0):
        input_str = inputQueue.get()
        return input_str
