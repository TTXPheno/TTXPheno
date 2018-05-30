''' Class to interpret weight info pkl file
'''

# General
import pickle
import scipy.special
import itertools

from operator import mul

# Logger
import logging
logger = logging.getLogger(__name__)

class WeightInfo:
    def __init__( self, filename ):
        data = pickle.load(file(filename))

        if 'rw_dict' in data.keys(): self.data = data['rw_dict']
        else: self.data = data

        if 'order' in data.keys(): self.pkl_order = data['order']['order']
        else: self.pkl_order = None

        if 'ref_point' in data.keys(): self.ref_point = data['ref_point']
        else: self.ref_point = None

        # store all variables (Wilson coefficients)
        self.variables = self.data.keys()[0].split('_')[::2]
        self.nvar      = len(self.variables)

        # compute reference point coordinates
        self.ref_point_coordinates = [ float( self.ref_point[var] ) if (self.ref_point is not None and var in self.ref_point.keys()) else 0 for var in self.variables ]

        # Sort wrt to position in ntuple
        self.id = self.data.keys()
        self.id.sort(key=lambda w: self.data[w])
        self.nid = len(self.id)

        logger.debug( "Found %i variables: %s. Found %i weights." %(self.nvar, ",".join( self.variables ), self.nid) )

    def set_order( self, order):
        if self.pkl_order == None:
            print( "WARNING: Could not find the polynomial order of the gridpack!")
        elif order > self.pkl_order:
            raise ValueError( "Polynomial order is greater than in the gridpack (order %i)" % self.pkl_order )
        self.order = order

    @staticmethod
    def get_ndof( nvar, order ):
        return sum( [ int(scipy.special.binom(nvar + o - 1, o)) for o in xrange(order+1) ] )

    # compute combinations on demand
    @property
    def combinations( self ):
        if hasattr( self, "_combinations"):
            return self._combinations
        else:
            self._combinations = []
            for o in xrange(self.order+1):
                self._combinations.extend( list(itertools.combinations_with_replacement( self.variables, o )) )
            return self._combinations

    def weight_string(self):
        ''' get the full reweight string
        '''
        substrings = []
        for i_comb, comb in enumerate(self.combinations):
            substrings.append(  "*".join( ["p_C[%i]"%i_comb] + [ "(rw_%s-%s)"%(v,self.ref_point[v].rstrip('0')) if self.ref_point is not None and v in self.ref_point.keys() else "rw_%s"%(v) for v in  comb] )  )

        return "+".join( substrings )

    def complement_args(self, args ):
        ''' prepare the args; add the ref_point ones and check that there is no inconsistency''' 
        args = {x:y for x,y in args.items() if y!=0} # remove entries which are 0

        # add WC that are in the ref point but not in args
        if self.ref_point is not None:
            for item in self.ref_point.keys():
                if item not in args.keys(): args[item] = 0

        # check if WC in args that are not in the gridpack
        unused_args = set(args.keys()) - set(self.variables)
        if len(unused_args) > 0:
            raise ValueError( "Variable %s not in the gridpack! Please use only the following variables: %s" % (' && '.join(unused_args), ', '.join(self.variables)) )
        
    def get_weight_string(self, **kwargs):
        '''make a root draw string that evaluates the weight in terms of the p_C coefficient vector using the kwargs as WC'''

        # add the arguments from the ref-point 
        self.complement_args( kwargs )

        substrings = []

        # run all combinations of WC
        for i_comb, comb in enumerate(self.combinations):
            if False in [v in kwargs for v in comb]: continue
            substrings.append( "p_C[%i]*%s" %(i_comb, str(float(reduce(mul,[ ( kwargs.get(v) - float(self.ref_point[v]) ) if self.ref_point is not None and v in self.ref_point.keys() else kwargs.get(v) for v in comb],1))).rstrip('0') ) )
        return "+".join( substrings )

    def get_weight_func(self, **kwargs):
        '''construct a lambda function that evaluates the weight in terms of the event.p_C coefficient vector using the kwargs as WC'''

        # add the arguments from the ref-point 
        self.complement_args( kwargs )

        terms = []
        for i_comb, comb in enumerate(self.combinations):
            if False in [v in kwargs for v in comb]: continue
            # store [ ncoeff, factor ]
            terms.append( [ i_comb, float(reduce(mul,[ ( kwargs.get(v) - float(self.ref_point[v]) ) if self.ref_point is not None and v in self.ref_point.keys() else kwargs.get(v) for v in comb],1)) ] )

        return lambda event, sample: sum( event.p_C[term[0]]*term[1] for term in terms )

    def get_weight_yield(self, coeffList, **kwargs):
        '''compute yield from a list of coefficients (in the usual order of p_C) using the kwargs as WC'''

        # add the arguments from the ref-point 
        self.complement_args( kwargs )

        result = 0 
        for i_comb, comb in enumerate(self.combinations):
            if False in [v in kwargs for v in comb]: continue
            result += coeffList[i_comb]*float(reduce(mul,[ ( kwargs.get(v) - float(self.ref_point[v]) ) if self.ref_point is not None and v in self.ref_point.keys() else kwargs.get(v) for v in comb],1))

        return result

    @staticmethod
    def differentiate( comb, var ):
        ''' Differentiate a product
        '''
        prefac = comb.count( var ) 
        if prefac==0:
            diff_comb = tuple()
        else:
            diff_comb = list(comb)
            diff_comb.remove( var )
        return prefac, tuple(diff_comb)

    def diff_weight_string(self, var):
        if var not in self.variables:
            raise ValueError( "Variable %s not in list of variables %r" % (var, self.variables) )
        substrings = []
        for i_comb, comb in enumerate(self.combinations):
            prefac, diff_comb = WeightInfo.differentiate( comb, var)
            if prefac!=0:
                substrings.append(  "*".join( ["%i*p_C[%i]"%(prefac, i_comb) if prefac!=1 else "p_C[%i]"% i_comb] + [ "rw_%s"%v for v in diff_comb] )  )

        return "+".join( substrings )

    def fisherParametrization( self, var1, var2):
        if var1==var2:
            return "(%s)**2/(%s)"%( self.diff_weight_string( var1 ), self.weight_string() )
        else:
            return "(%s)*(%s)/(%s)"%( self.diff_weight_string( var1 ), self.diff_weight_string( var2 ), self.weight_string( ) )

    # Make a list from the bin contents from a histogram that resulted from a 'Draw' of p_C 
    @staticmethod
    def BinContentToList(histo):
        return [histo.GetBinContent(i) for i in range(1,histo.GetNbinsX()+1)]

if __name__ == "__main__":

    #w = WeightInfo("/afs/hephy.at/data/rschoefbeck02/TopEFT/results/gridpacks/ttZ0j_rwgt_patch_currentplane_highStat_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl")
    #w.fisherParametrization(2, 'cpt', 'cpt')
    #c = ROOT.TChain( "Events" )
    #c.Add("/afs/hephy.at/data/rschoefbeck02/TopEFT/skims/gen/v2/fwlite_ttZ_ll_LO_currentplane_highStat_scan/fwlite_ttZ_ll_LO_currentplane_highStat_scan_0.root" )
    #fisher_string = ":".join( [ w.fisherParametrization(2, 'cpt', 'cpt'),  w.fisherParametrization(2, 'cpt', 'cpQM'),  w.fisherParametrization(2, 'cpQM', 'cpQM') ] )
    #c.Scan(fisher_string)
    import ROOT
    c = ROOT.TChain("Events")
    c.Add("/afs/hephy.at/data/rschoefbeck02/TopEFT/skims/gen/v2_small/fwlite_ttZ_ll_LO_highStat_scan/fwlite_ttZ_ll_LO_highStat_scan.root")
#    w = WeightInfo("/afs/cern.ch/user/l/llechner/public/CMSSW_9_4_6_patch1/src/Refpoint_test/gridpacks/addons/cards/ttZ0j_rwgt/ttZ0j_rwgt_reweight_card.pkl")
#    w = WeightInfo("/afs/hephy.at/data/rschoefbeck02/TopEFT/results/gridpacks/ttZ0j_rwgt_patch_625_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl")
    w = WeightInfo("/afs/hephy.at/data/llechner01/TTXPheno/gridpacks/18052018_ref/ttZ/order2/ttZ0j_rwgt_slc6_amd64_gcc630_CMSSW_9_3_0_tarball.pkl")
    w.set_order( 2 )

#    para = {'cpt':3, 'cpQM':5}
#    w.arg_weight_func(**para)
#    fisher_string = ":".join( [ w.fisherParametrization( 'cpt', 'cpt'),  w.fisherParametrization( 'cpt', 'cpQM'),  w.fisherParametrization('cpQM', 'cpQM') ] )

    print(w.ref_point)
    print(w.weight_string())
    w.weight_string()
    print(w.get_weight_string(ctW=4, ctZ=5, ctGI=2))
#    print(w.weight_string())
#    print(w.arg_weight_string(ctZI=2, cpt=5))
#     print(w.arg_weight_string())
