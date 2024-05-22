import eel
import os
from queue import Queue

class ChatBot:  # Corrected class name to 'ChatBot'

    started = False
    userinputQueue = Queue()

    @staticmethod  # Added staticmethod decorator
    def isUserInput():  # Added 'self' parameter
        return not ChatBot.userinputQueue.empty()

    @staticmethod  # Added staticmethod decorator
    def popUserInput():  # Added 'self' parameter
        return ChatBot.userinputQueue.get()

    @staticmethod  # Added staticmethod decorator
    def close_callback(route, websockets):
        # if not websockets:
        #     print('Bye!')
        exit()

    @staticmethod  # Added staticmethod decorator
    @eel.expose
    def getUserInput(msg):  # Added 'self' parameter
        ChatBot.userinputQueue.put(msg)
        print(msg)
    
    @staticmethod  # Added staticmethod decorator
    def close():
        ChatBot.started = False
    
    @staticmethod  # Added staticmethod decorator
    def addUserMsg(msg):
        eel.addUserMsg(msg)
    
    @staticmethod  # Added staticmethod decorator
    def addAppMsg(msg):
        eel.addAppMsg(msg)

    @staticmethod  # Added staticmethod decorator
    def start():
        path = os.path.dirname(os.path.abspath(__file__))
        eel.init(path + r'\web', allowed_extensions=['.js', '.html'])
        try:
            eel.start('index.html', mode='chrome',
                                    host='localhost',
                                    port=27005,
                                    block=False,
                                    size=(350, 480),
                                    position=(10,100),
                                    disable_cache=True,
                                    close_callback=ChatBot.close_callback)
            ChatBot.started = True
            while ChatBot.started:
                try:
                    eel.sleep(10.0)
                except:
                    # main thread exited
                    break
        
        except:
            pass
