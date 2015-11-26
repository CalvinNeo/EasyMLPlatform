class ModelBase:
    def __init__(self, dataset):
        self.dataset = dataset

    def Test(self, inp):
        return inp

if __name__ == '__main__':
    class Base():
        def __init__(self, dataset):
            self.dataset = dataset
            print "Base:", self.dataset
        def Test(self):
            print "AHA"
    class Derived(Base):
        def __init__(self, dataset):
            Base.__init__(self, dataset)
            print "Derived:", self.dataset
            # self.Test = self.OHO
            self.Test()
        def OHO(self):
            print "OHO"
        # def Test(self):
        #     print "oHO"
    d = Derived([1,2,3])