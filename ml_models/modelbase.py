class ModelBase:
    def __init__(self, dataset):
        self.dataset = dataset

    def Test(self, inp):
        return inp

    @staticmethod
    def AllModelInfo():
        # return eval(open('./models.json','r').read())
        return {
            'MATRIX_ADD':{
                'ndataset': 2
                ,'distributed': True
                ,'nontraining': True
            },
            'MATRIX_DOT':{
                'ndataset': 2
                ,'distributed': True
                ,'nontraining': True
            },
            'MATRIX_INV':{
                'ndataset': 1
                ,'distributed': True
                ,'nontraining': True
            },
            'MATRIX_PCA':{
                'ndataset': 2
                ,'distributed': True
                ,'nontraining': False
            },


            'EM':{
                'ndataset': 1
                ,'distributed': True
                ,'nontraining': False
            },
            'SVM':{
                'ndataset': 1
                ,'distributed': True
                ,'nontraining': False
            },
            'NAIVE_BAYES':{
                'ndataset': 1
                ,'distributed': True
                ,'nontraining': False
            },
            'K_MEANS':{
                'ndataset': 1
                ,'distributed': True
                ,'nontraining': False
            },
            'KNN':{
                'ndataset': 1
                ,'distributed': True
                ,'nontraining': False
            },

            'DECISION_TREE':{
                'ndataset': 1
                ,'distributed': False
                ,'nontraining': False
            },
            'ADABOOST':{
                'ndataset': 1
                ,'distributed': False
                ,'nontraining': False
            },
            'LOGISTIC':{
                'ndataset': 1
                ,'distributed': False
                ,'nontraining': False
            },
            'CRF':{
                'ndataset': 1
                ,'distributed': False
                ,'nontraining': False
            },
            'FP_GROWTH':{
                'ndataset': 1
                ,'distributed': False
                ,'nontraining': False
            },
        }

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
    print ModelBase.AllModelInfo()