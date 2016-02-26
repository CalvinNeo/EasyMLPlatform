#coding:utf8
import sys
sys.path.append('..')

import itertools
import model_list

class ModelBase:
    '''
        -- below should be implemented
        Test 
        Train 
        Save
        Read
        Graph
        T ()
    '''
    def __init__(self, dataset, prototype, *args, **kwargs):
        '''
            dataset
            prototype
            extra
            >positive negative
            <classfeatureindex loss
        '''
        self.dataset = dataset
        '''
            AUTO SET IF USE DERIVED CLASS
            prototype in ['boosting','bp','crf','decision_tree','em',...]
        '''
        self.prototype = prototype

        '''
            extra metadata of the model(JSON)
        '''
        if self.dataset.dstype == "JSON":
            if 'extra' in kwargs.keys() and kwargs['extra'] != None:
                self.extra = kwargs['extra']
            else:
                self.extra = self.dataset.extra

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
        if 'loss' in kwargs.keys() and kwargs['loss'] != None:
            self.Loss = kwargs['loss']
        else:
            self.Loss = ModelBase.QuadLoss

    def Train(self, dataset):
        pass

    def Save(self, name):
        pass

    def Load(self, name):
        pass

    def Test(self, inp):
        return inp

    def Apply(self, dataset, remove_item):
        return dataset

    def Graph(self, op):
        pass

    def T(self, inp):
        return inp[self.classfeatureindex]

    @staticmethod
    def QuadLoss(t, a):
        '''
            Quadratic Loss Function:
            L(Y, f(X)) = (Y - f(X))^2
        '''
        if type(t).__name__ in ['matrix','ndarray']:
            r = t-a
        else:
            r = np.matrix(t) - np.matrix(a)
        return np.dot(r,r.T)

    @staticmethod
    def BinLoss(t, a):
        '''
            0-1 Loss Function:
            L(Y, f(X)) = 1 if Y == f(X) else 0
        '''
        if type(t).__name__ in ['matrix','ndarray']:
            r = t-a
        else:
            r = np.matrix(t) - np.matrix(a)
        return 1 if np.sum(np.vectorize(lambda n:0 if n==0.0 else 1)(vec)) == 0.0 else 0

    @staticmethod
    def AbsLoss(t, a):
        '''
            Absolute Loss Function:
            L(Y, f(X)) = Abs( Y - f(X) )
        '''
        pass

    @staticmethod
    def LogLoss(t, a):
        '''
            Log-likelihood Loss Function:
        '''
        pass

    @staticmethod
    def L0(vec):
        '''
            count of non-zero elements of a vector
        '''
        if type(vec).__name__ in ['matrix','ndarray']:
            return np.sum(np.vectorize(lambda n:0 if n==0.0 else 1)(vec))
        else:
            return np.sum(np.vectorize(lambda n:0 if n==0.0 else 1)(np.matrix(vec)))

    @staticmethod
    def L1(vec):
        '''
            sum(abs(for each elements in a vector))
        '''
        if type(vec).__name__ in ['matrix','ndarray']:
            return np.sum(np.vectorize(lambda n:abs(n))(vec))
        else:
            return np.sum(np.vectorize(lambda n:abs(n))(np.matrix(vec)))

    @staticmethod
    def L2(vec):
        '''
            sqrt(sigma(square each elements))
        '''
        if type(vec).__name__ in ['matrix','ndarray']:
            return np.sum(np.vectorize(lambda n:n**2)(vec))**0.5
        else:
            return np.sum(np.vectorize(lambda n:n**2)(np.matrix(vec)))**0.5

    @staticmethod
    def EuclideanDist(vec1, vec2):
        '''
            Euclidean Distance:
                sqrt(sigma((vec1[i] - vec2[i]) ^ 2))
        '''
        if type(vec1).__name__ in ['matrix','ndarray']:
            r = vec1-vec2
            return np.trace(np.dot(r,r.T))**0.5
        else:
            r = np.matrix(vec1) - np.matrix(vec2)
            return np.trace(np.dot(r,r.T))**0.5

    @staticmethod
    def ManhattanDist(vec1, vec2):
        '''
            ManhattanDist Distance:
                sigma(abs(vec1[i] - vec2[i]))
        '''
        if type(vec1).__name__ in ['matrix','ndarray']:
            pass
        else:
            pass

    @staticmethod
    def AllModelInfo():
        # return eval(open('./models.json','r').read())
        import naive_bayes
        import decision_tree
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
                ,'cls': naive_bayes.NaiveBayes
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
                ,'cls': decision_tree.DecisionTree
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
    print ModelBase.AllModelInfo().keys()
