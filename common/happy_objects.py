class HappyObject():

    def is_happy(self):
        return False

    def clap_your_hands(self):
        print(self.__class__.__name__," : clap! clap!")

    def if_you_happy_and_you_know_it(self,clap_your_hands_function=None):
        if self.is_happy():
            if clap_your_hands_function :
                clap_your_hands_function()
            else :
                HappyObject.clap_your_hands()

        else :
            e=str(self.__name__)+"NotHappyException"
            assert False,e
