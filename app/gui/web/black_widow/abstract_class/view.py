class AbstractView:
    class Session:
        def get(self, key:str):
            return 'SESSION OK ' + str(key)

    #@staticmethod
    #def get_session():
