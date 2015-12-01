class ModelBase:
    def __init__(self, dataset, prototype, *args, **kwargs):
        self.dataset = dataset
        '''
            prototype in ['boosting','bp','crf','decision_tree','em',...]
        '''
        self.prototype = prototype

        '''
            Classify
        '''
        if 'positive' in kwargs.keys() and kwargs['positive'] != None:
            self.Positive = kwargs['positive']
        else:
            self.Positive = 1        
        if 'negative' in kwargs.keys() and kwargs['negative'] != None:
            self.Negative = kwargs['negative']
        else:
            self.Negative = -1 
        '''
            Regress
        '''
        if 'classfeatureindex' in kwargs.keys() and kwargs['classfeatureindex'] != None:
            self.classfeatureindex = kwargs['classfeatureindex']
        else:
            self.classfeatureindex = self.dataset.classfeatureindex

    def Test(self, inp):
        return inp

    def T(self, inp):
        return inp[classfeatureindex]

    @staticmethod
    def AllModelInfo():
        # return eval(open('./models.json','r').read())
        return {
            'MATRIX_ADD':{
                'ndataset': 2
                ,'distributed': True
                ,'nontraining': True
                ,'modeltype': None
            },
            'MATRIX_DOT':{
                'ndataset': 2
                ,'distributed': True
                ,'nontraining': True
                ,'modeltype': None
            },
            'MATRIX_INV':{
                'ndataset': 1
                ,'distributed': True
                ,'nontraining': True
                ,'modeltype': None
            },
            'MATRIX_PCA':{
                'ndataset': 2
                ,'distributed': True
                ,'nontraining': False
                ,'modeltype': None
            },


            'EM':{
                'ndataset': 1
                ,'distributed': True
                ,'nontraining': False
                ,'modeltype': None
            },
            'SVM':{
                'ndataset': 1
                ,'distributed': True
                ,'nontraining': False
                ,'modeltype': 'CLASSIFY'
            },
            'NAIVE_BAYES':{
                'ndataset': 1
                ,'distributed': True
                ,'nontraining': False
                ,'modeltype': 'CLASSIFY'
            },
            'K_MEANS':{
                'ndataset': 1
                ,'distributed': True
                ,'nontraining': False
                ,'modeltype': 'CLUSTER'
            },
            'KNN':{
                'ndataset': 1
                ,'distributed': True
                ,'nontraining': False
                ,'modeltype': 'CLUSTER'
            },

            'DECISION_TREE':{
                'ndataset': 1
                ,'distributed': False
                ,'nontraining': False
                ,'modeltype': 'CLASSIFY'
            },
            'ADABOOST':{
                'ndataset': 1
                ,'distributed': False
                ,'nontraining': False
                ,'modeltype': 'CLASSIFY'
            },
            'LOGISTIC':{
                'ndataset': 1
                ,'distributed': False
                ,'nontraining': False
                ,'modeltype': 'CLASSIFY'
            },
            'CRF':{
                'ndataset': 1
                ,'distributed': False
                ,'nontraining': False
                ,'modeltype': 'CLASSIFY'
            },
            'FP_GROWTH':{
                'ndataset': 1
                ,'distributed': False
                ,'nontraining': False
                ,'modeltype': None
            },
        }

if __name__ == '__main__':
    class Base():
        def __init__(self, dataset, *args, **kwargs):
            self.dataset = dataset
            print "Base:", self.dataset
            if 'positive' in kwargs.keys() and kwargs['positive'] != None:
                print kwargs['positive']

        def Test(self):
            print "AHA"
    class Derived(Base):
        def __init__(self, dataset, *args, **kwargs):
            Base.__init__(self, dataset, *args, **kwargs)
            print "Derived:", self.dataset
            # self.Test = self.OHO
            self.Test()
        def OHO(self):
            print "OHO"
        # def Test(self):
        #     print "oHO"
    d = Derived([1,2,3], positive="FFFFFFFFFFFFFFFFFFFFFFFF")
    print ModelBase.AllModelInfo()