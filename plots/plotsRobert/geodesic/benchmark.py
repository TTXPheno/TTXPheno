## Make a 2nd oder dummy parametrization
##./make_reweight_card.py --overwrite --filename out.dat --couplings 2 x 1
#
## Load parametrization
#from TTXPheno.Tools.WeightInfo import WeightInfo
#w = WeightInfo("/afs/hephy.at/data/rschoefbeck01/TTXPheno/test_param/out.pkl")
#w.set_order(2)
#
#variables = ('x')
#
## Specify a parametrization 1+x**2
#coeffLists = [ [1,0,1] ]
#
## correct->
#w.get_total_weight_yield( coeffLists, x=1) # 1+1**2 = 2
#w.get_total_weight_yield( coeffLists, x=2)   # 1+2**2 = 5
#w.get_diff_weight_yield( 'x', coeffLists[0], x=3) # 2*3 = 6
#w.get_fisherInformation_matrix( coeffLists[0], x=2.) # -> 1/5.*(2*2)**2 
#w.get_christoffels( coeffLists )
#
## christoffel
#christoffels = w.get_christoffels( coeffLists )
#christoffels(0, (3.) ) # 0.5*1/(1/(10.)*(6.)**2)*(1/10.*(6)**3+2/10.**2*6*2) = 3.0333333333333337

# Make a 2nd oder dummy parametrization
#./make_reweight_card.py --overwrite --filename out_xy.dat --couplings 2 x 1 y 1

# Load parametrization
from TTXPheno.Tools.WeightInfo import WeightInfo
w = WeightInfo("/afs/hephy.at/data/rschoefbeck01/TTXPheno/test_param/out_xy.pkl")
w.set_order(2)

variables = ('x', 'y')

# Specify a parametrization 1/x/y/x^2/xy/y^2 
#1+x**2
coeffLists = [ [0,1,1,0,1,0] ]

# correct->
w.get_total_weight_yield( coeffLists, x=1, y=1) # 1+1**2 = 2
w.get_total_weight_yield( coeffLists, x=2)   # 1+2**2 = 5
w.get_diff_weight_yield( 'x', coeffLists[0], x=3) # 2*3 = 6
w.get_fisherInformation_matrix( coeffLists[0], x=2.) # -> 1/5.*(2*2)**2 
w.get_christoffels( coeffLists )

# christoffel
christoffels = w.get_christoffels( coeffLists )
christoffels(0, (3., 2.)) # 0.5*1/(1/(10.)*(6.)**2)*(1/10.*(6)**3+2/10.**2*6*2) = 3.0333333333333337
