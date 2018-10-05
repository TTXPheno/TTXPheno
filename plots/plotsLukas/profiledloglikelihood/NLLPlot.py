''' Plot script WC parameter LogLikelihood
'''

# Standard imports 
import sys
import ROOT
import imp
import pickle

from math import sqrt
# turn off graphics
ROOT.gROOT.SetBatch( True )

# RootTools
from RootTools.core.standard import *

import numpy as np
import ctypes

from multiprocessing import Pool

# Logger
import TTXPheno.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   'DEBUG', logFile = None)
logger_rt = logger_rt.get_logger('INFO', logFile = None)

# TTXPheno
from TTXPheno.samples.benchmarks import * 
from TTXPheno.Tools.user import plot_directory

# get the reweighting function
from TTXPheno.Tools.WeightInfo import WeightInfo

ROOT.gStyle.SetNumberContours(255)

# Arguments
import argparse

argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--version',         action='store',     default='test', help='Appendix to plot directory')
argParser.add_argument('--process',         action='store',     default='ttZ_3l', nargs='?', choices=['ttZ_3l', 'ttZ_4l', 'ttgamma_1l', 'ttgamma_2l'], help="which process to calculate?")
argParser.add_argument('--fit',             action='store',     default='SM', nargs='?', choices=['SM', 'BestFit'], help="compare to SM or BestFit?")
argParser.add_argument('--sample',          action='store',     default='fwlite_ttZ_ll_LO_order2_15weights_ref', help='Sample name specified in sample/python/benchmarks.py, e.g. fwlite_ttZ_ll_LO_order2_15weights_ref')
argParser.add_argument('--order',           action='store',     default=2, help='Polynomial order of weight string (e.g. 2)')
argParser.add_argument('--selection',       action='store',     default='lepSel3-onZ-njet3p-nbjet1p-Zpt0', help="Specify cut.")
argParser.add_argument('--small',           action='store_true', help='Run only on a small subset of the data?')
argParser.add_argument('--contours',        action='store_true', help='draw 1sigma and 2sigma contour line?')
argParser.add_argument('--smooth',          action='store_true', help='smooth histogram?')
argParser.add_argument('--level',           action='store',     default='reco', nargs='?', choices=['reco', 'gen'], help='Which level of reconstruction? reco, gen')
argParser.add_argument('--variables' ,      action='store',     default = ['ctZ', 'ctZI'], type=str, nargs=2, help = "argument plotting variables")
argParser.add_argument('--binning',         action='store',     default = [1, -2, 2, 1, -2, 2], type=float, nargs=6, help = "argument parameters")
argParser.add_argument('--zRange',          action='store',     default = [None, None], type=float, nargs=2, help = "argument parameters")
argParser.add_argument('--luminosity',      action='store',     default=150, help='Luminosity for weighting the plots')
argParser.add_argument('--scale',           action='store',     default=None, help='Luminosity for weighting the plots')
argParser.add_argument('--cores',           action='store',     default=8, type=int, help='number of cpu cores for multicore processing')
argParser.add_argument('--overwrite',       action='store_true', help='overwrite datafile?')
argParser.add_argument('--binMultiplier',   action='store',     default=3, type=int, help='bin multiplication factor')
argParser.add_argument('--detector',        action='store',     default='CMS', nargs='?', choices=['CMS', 'ATLAS', 'phase2_CMS'], help='Which Delphes detector simulation?')
argParser.add_argument('--scale14TeV',      action='store_true', help='scale 13 TeV cross-sections to 14 Tev?')

args = argParser.parse_args()

if args.level == 'gen':
    if 'ttZ' in args.process.split('_'):
        if args.small: from TTXPheno.Analysis.regions import genttZRegionsSmall as regions
        else:          from TTXPheno.Analysis.regions import genttZRegions as regions
    elif 'ttgamma' in args.process.split('_'):
        if args.small: from TTXPheno.Analysis.regions import genttgammaRegionsSmall as regions
        else:          from TTXPheno.Analysis.regions import genttgammaRegions as regions

    # Import additional functions/classes specified for the level of reconstruction
    from TTXPheno.Tools.cutInterpreterGen import cutInterpreter

elif args.level == 'reco':
    if 'ttZ' in args.process.split('_'):
        if args.small: from TTXPheno.Analysis.regions import recottZRegionsSmall as regions
        else:          from TTXPheno.Analysis.regions import recottZRegions as regions
    elif 'ttgamma' in args.process.split('_'):
        if args.small: from TTXPheno.Analysis.regions import recottgammaRegionsSmall as regions
        else:          from TTXPheno.Analysis.regions import recottgammaRegions as regions

    # Import additional functions/classes specified for the level of reconstruction
    from TTXPheno.Tools.cutInterpreterReco import cutInterpreter


if args.fit == 'SM':
    rmin=0.99
    rmax=1.01
elif args.fit == 'BestFit':
    rmin=0.01
    rmax=2

#binning range
binningX = args.binning[:3]
binningY = args.binning[3:]

if binningX[0] > 1:
    xRange = np.linspace( binningX[1], binningX[2], int(binningX[0]), endpoint=False)
    xRange = [ el + 0.5 * ( xRange[1] - xRange[0] ) for el in xRange ]
else:
    xRange = [ 0.5 * ( binningX[1] + binningX[2] ) ]

if binningY[0] > 1:
    yRange = np.linspace( binningY[1], binningY[2], int(binningY[0]), endpoint=False)
    yRange = [ el + 0.5 * ( yRange[1] - yRange[0] ) for el in yRange ]
else:
    yRange = [ 0.5 * ( binningY[1] + binningY[2] ) ]

#save data file
filename = '_'.join( ['nll', args.detector ] + args.sample.split('_')[1:3] + args.variables + map( str, args.binning ) + [ args.selection, str(args.luminosity), "14TeV" if args.scale14TeV else "13TeV" ] ) + '.data'
#do the calculation
print filename
print not os.path.isfile('data/' + filename)
if not os.path.isfile('data/' + filename) or args.overwrite:
    # Import samples
    sample_file     = "$CMSSW_BASE/python/TTXPheno/samples/benchmarks.py"
    loadedSamples   = imp.load_source( "samples", os.path.expandvars( sample_file ) )

    ttXSample       = getattr( loadedSamples, args.sample + '_%s' %args.detector )
    WZSample        = getattr( loadedSamples, 'fwlite_WZ_lep_LO_order2_15weights_%s' %args.detector )
#    ttSample        = getattr( loadedSamples, 'fwlite_tt_full_LO_order2_15weights_%s' %args.detector )
#    tWSample        = getattr( loadedSamples, 'fwlite_tW_LO_order2_15weights_%s' %args.detector )
    tWZSample       = getattr( loadedSamples, 'fwlite_tWZ_LO_order2_15weights_%s' %args.detector )
    tZqSample       = getattr( loadedSamples, 'fwlite_tZq_LO_order2_15weights_%s' %args.detector )
#    ZgammaSample    = getattr( loadedSamples, 'fwlite_Zgamma_LO_order2_15weights_%s' %args.detector )
#    ttgammaSample   = getattr( loadedSamples, 'fwlite_ttgamma_bg_LO_order2_15weights_%s' %args.detector )

    #if args.process.split('_')[0] == 'ttgamma':
    #    ttgammaIsrSample  = copy.deepcopy( ttXSample ) #select ttgamma events with isolated gamma from ISR (cat a2)
    #    ttgammaIsrSample.name = 'fwlite_ttgamma_ISR_LO_order2_15weights_ref'

#    if args.process == 'ttZ_3l': bg = [ WZSample, tWZSample, tZqSample, ttgammaSample ]
    if args.process == 'ttZ_3l': bg = [ WZSample, tWZSample, tZqSample ]
    elif args.process == 'ttZ_4l': bg = [ WZSample, tWZSample, tZqSample, ttgammaSample ]
    elif args.process == 'ttgamma_1l': bg = [ ttSample, tWSample, tWZSample, tZqSample, ZgammaSample ]
    elif args.process == 'ttgamma_2l': bg = [ ttSample, tWSample, tWZSample, tZqSample, ZgammaSample ]

    def checkReferencePoint( sample ):
        ''' check if sample is simulated with a reference point
        '''
        return pickle.load(file(sample.reweight_pkl))['ref_point'] != {}

    # set selection string
    selectionString = cutInterpreter.cutString(args.selection)

    # somehow has to be separate from the next loop
    if args.small:
        for s in [ttXSample] + bg:
            s.reduceFiles( to = 5 )

    # configure samples
    for s in [ttXSample] + bg:

        s.event_factor = s.nEvents / float( s.chain.GetEntries() )
        s.xsecScaleFactor = s.xsec14 / s.xsec if args.scale14TeV else 1.
        s.weightInfo = WeightInfo( s.reweight_pkl )
        s.weightInfo.set_order( args.order )
        s.setSelectionString( selectionString )

        if checkReferencePoint( s ):
            s.setWeightString( 'ref_lumiweight1fb*(%s)*(%s)*(%s)'%( str(args.luminosity), str(s.event_factor), str(s.xsecScaleFactor) ) )
        else:
            s.setWeightString( 'lumiweight1fb*(%s)*(%s)*(%s)'%( str(args.luminosity), str(s.event_factor), str(s.xsecScaleFactor) ) )

    # overlap removal
    if args.process.split('_')[0] == 'ttgamma':
        ttXSample.addSelectionString( "(nonIsoPhoton!=1)" ) 
        ttSample.addSelectionString(  "(nonIsoPhoton==1)" ) 

    for var in args.variables:
        if var not in ttXSample.weightInfo.variables and not (args.variables[0] == 'cuB' and args.variables[1] == 'cuW'):
            raise ValueError('Input variable not in gridpack: %s' %var)

    observation                  = {}

    signal_jec_uncertainty       = {}
    signal_fakerate_uncertainty  = {}

    ttX_SM_rate                  = {}
    ttX_coeffList                = {}

    background_rate                 = {}
    background_jec_uncertainty      = {}
    background_fakerate_uncertainty = {}

    for i_region, region in enumerate(regions):
        # compute signal yield for this region (this is the final code)

        logger.info( "At region %s", region )

        # ttX SM
        ttX_coeffList[region] = ttXSample.weightInfo.getCoeffListFromDraw( ttXSample, selectionString = region.cutString() )
        ttX_SM_rate[region]   = ttXSample.weightInfo.get_weight_yield( ttX_coeffList[region] )

        # signal uncertainties
        signal_jec_uncertainty      [region] = 1.05
    #    signal_jec_uncertainty      [region] = 1.09
        signal_fakerate_uncertainty [region] = 1.0  # signal has no FR uncertainty

        background_rate[region]                 = {}
        background_fakerate_uncertainty[region] = {}
        background_jec_uncertainty[region]      = {}

        for i_background, background in enumerate(bg):
            # compute bg yield for this region (this is the final code)

            background_rate                 [region][background.name] = background.getYieldFromDraw( selectionString=region.cutString() )['val']
            background_fakerate_uncertainty [region][background.name] = min( [ 1 + 0.03*(i_region+1), 1.12 ] ) #*(i_background+1) #change that
            background_jec_uncertainty  [region][background.name] = max( [ 1.05, min( [ 1.12 - 0.01*(i_region+1), 1.12 ] ) ] ) #1.2 - 0.02*(i_region+1) #*(i_background+1) #change that

        # Our expected observation :-)
        observation[region] = int( sum( background_rate[region].values() ) + ttX_SM_rate[region] )


    # Write temporary card file
    from TTXPheno.Tools.cardFileWriter import cardFileWriter
    c = cardFileWriter.cardFileWriter()


    def cuBWtoctWZ( cuB, cuW ):
        ''' transforms C_tZ and C_tW to C_uB and C_uW
            C_tZ = Re( -sW*C_uB + cW*C_uW )
            C_tW = Re( C_uW )
            arXiv: 1802.07237
        '''
        sW=0.4715
        cW=0.8819

        ctW = cuW
        ctZ = -sW*cuB + cW*cuW

        return ctZ, ctW


    def calculation( variables ):
    #def calculation( var1, var2 ):

            if args.variables[0] == 'cuB' and args.variables[1] == 'cuW':
                var1, var2 = variables #cuB cuW
                ctZ, ctW = cuBWtoctWZ( var1, var2 )
                kwargs = { 'ctZ':ctZ, 'ctW':ctW }
            else:
                var1, var2 = variables
                kwargs = { args.variables[0]:var1, args.variables[1]:var2 }

            # uncertainties
            c.reset()
            c.addUncertainty('lumi',        'lnN')
            c.addUncertainty('JEC',         'lnN')
            c.addUncertainty('fake',        'lnN')

            signal_rate                  = {}
            for i_region, region in enumerate(regions):

                signal_rate[region] = ttXSample.weightInfo.get_weight_yield( ttX_coeffList[region], **kwargs)

                bin_name = "Region_%i" % i_region
                nice_name = region.__str__()
                c.addBin(bin_name, ['_'.join(s.name.split('_')[1:3]) for s in bg], nice_name)
                c.specifyObservation( bin_name, observation[region] )

    #            c.specifyFlatUncertainty( 'lumi', 1.05 )
    #            c.specifyFlatUncertainty( 'lumi', 1.026 )
                c.specifyFlatUncertainty( 'lumi', 1.05 )

                c.specifyExpectation( bin_name, 'signal', signal_rate[region] )
                c.specifyUncertainty( 'JEC', bin_name, 'signal', signal_jec_uncertainty[region])
                c.specifyUncertainty( 'fake',bin_name, 'signal', signal_fakerate_uncertainty[region])

                #c.specifyExpectation( bin_name, 'ttX_SM', ttX_SM_rate[region] )
                #c.specifyUncertainty( 'JEC', bin_name, 'ttX_SM', ttX_SM_jec_uncertainty[region])
                #c.specifyUncertainty( 'fake',bin_name, 'ttX_SM', ttX_SM_fakerate_uncertainty[region])

                for background in bg:
                    c.specifyExpectation( bin_name, '_'.join( background.name.split('_')[1:3] ), background_rate[region][background.name] )
                    c.specifyUncertainty( 'JEC', bin_name, '_'.join( background.name.split('_')[1:3] ), background_jec_uncertainty[region][background.name])
                    c.specifyUncertainty( 'fake',bin_name, '_'.join( background.name.split('_')[1:3] ), background_fakerate_uncertainty[region][background.name])
                    
            nameList = ttXSample.name.split('_')[1:3] + args.variables + args.binning + [ args.level, args.version, args.order, args.luminosity, "14TeV" if args.scale14TeV else "13TeV", args.selection, 'small' if args.small else 'full', var1, var2 ]
            cardname = '%s_nll_card'%'_'.join( map( str, nameList ) )
            c.writeToFile( './tmp/%s.txt'%cardname )

            profiledLoglikelihoodFit = ProfiledLoglikelihoodFit( './tmp/%s.txt'%cardname )
            profiledLoglikelihoodFit.make_workspace(rmin=rmin, rmax=rmax)
            #expected_limit = profiledLoglikelihoodFit.calculate_limit( calculator = "frequentist" )
            nll = profiledLoglikelihoodFit.likelihoodTest()
            logger.info( "NLL: %f", nll)
            profiledLoglikelihoodFit.cleanup(removeFiles=True)
            del profiledLoglikelihoodFit
            ROOT.gDirectory.Clear()

            # in very large WC regions, the fit fails, not relevant for the interesting regions
            if nll is None or abs(nll) > 1000000: nll = 999

            return var1, var2, nll


    # Limit plot
    from TTXPheno.Analysis.ProfiledLoglikelihoodFit import ProfiledLoglikelihoodFit

    results = []

    for varX in xRange:
        # do not run all calc in one pool, memory leak!!!
        pool = Pool( processes = args.cores )
        results += pool.map( calculation, [ (varX, varY) for varY in yRange ] )
        del pool

    with open('tmp/'+filename, 'w') as f:
        for item in results:
            f.write( "%s\n" % ','.join( map( str, list(item) ) ) )

else:
    with open('data/'+filename, 'r') as f:
        data = f.readlines()

    results = []
    for line in data:
        vals = map( float, line.split('\n')[0].split(',') )
        if args.scale is not None: vals[2] = vals[2]*float(args.scale)/float(args.luminosity)/2
        results.append( tuple( vals ) )


#Plot

#scale to SM
results.sort( key = lambda res: ( abs(res[0]), abs(res[1]), res[2] ) )
nll_SM = results[0][2]

results = [ (x, y, 2*(result - nll_SM)) for x, y, result in results ]

def toGraph2D( name, title, data ):
    result = ROOT.TGraph2D( len(data) )
    debug = ROOT.TGraph()
    result.SetName( name )
    result.SetTitle( title )
    for i, datapoint in enumerate(data):
        x, y, val = datapoint
        result.SetPoint(i, x, y, val)
        debug.SetPoint(i, x, y)
    c = ROOT.TCanvas()
    result.Draw()
    debug.Draw()
    del c
    #res = ROOT.TGraphDelaunay(result)
    return result, debug

#get TGraph2D from results list
a, debug = toGraph2D( args.process, args.process, results )#res_dic)
nxbins   = max(1, min(500, int(binningX[0])*int(args.binMultiplier)))
nybins   = max(1, min(500, int(binningY[0])*int(args.binMultiplier)))

#re-bin
hist = a.GetHistogram().Clone()
a.SetNpx(nxbins)
a.SetNpy(nybins)
hist = a.GetHistogram().Clone()

#smoothing
if args.smooth: hist.Smooth()

cans = ROOT.TCanvas("can_%s"%args.process,"",500,500)

#calculate contour lines (1sigma, 2sigma) for 2D
contours = {'ttZ_3l': [1.515*1.515, 2.486*2.486], 'ttgamma_1l': [1.515*1.515, 2.486*2.486], 'ttgamma_2l': [1.515*1.515, 2.486*2.486]}
if args.contours:
    histsForCont = hist.Clone()
    c_contlist = ((ctypes.c_double)*(len(contours[args.process])))(*contours[args.process])
    histsForCont.SetContour(len(c_contlist),c_contlist)
    histsForCont.Draw("contzlist")
    cans.Update()
    conts = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
    #cont_m2 = conts.At(0).Clone()
    #cont_m1 = conts.At(1).Clone()
    cont_p1 = conts.At(0).Clone()
    cont_p2 = conts.At(1).Clone()

pads = ROOT.TPad("pad_%s"%args.process,"",0.,0.,1.,1.)
pads.SetRightMargin(0.20)
pads.SetLeftMargin(0.14)
pads.SetTopMargin(0.11)
pads.Draw()
pads.cd()

hist.Draw("colz")

#draw contour lines
if args.contours:
    for conts in [cont_p2]:
        for cont in conts:
            cont.SetLineColor(ROOT.kOrange+7)
            cont.SetLineWidth(2)
#            cont.SetLineStyle(7)
            cont.Draw("same")
    for conts in [cont_p1]:
        for cont in conts:
            cont.SetLineColor(ROOT.kSpring-1)
            cont.SetLineWidth(2)
#            cont.SetLineStyle(7)
            cont.Draw("same")


hist.GetZaxis().SetTitle("-2 #Delta ln L")

if not None in args.zRange:
    hist.GetZaxis().SetRangeUser( args.zRange[0], args.zRange[1] )
#    hist.GetXaxis().SetRangeUser( -0.3 , 0.3 )
#    hist.GetYaxis().SetRangeUser( -0.3 , 0.3 )
#    hist.GetXaxis().SetRangeUser( -1 , 1 )
#    hist.GetYaxis().SetRangeUser( -1 , 1 )
#    hist.GetXaxis().SetRangeUser( -8 , 12 )
#    hist.GetYaxis().SetRangeUser( -8 , 12 )


if args.variables[0] == 'cuB' and args.variables[1] == 'cuW':
    hist.GetXaxis().SetTitle('C^{(33)}_{uB} (#Lambda/TeV)^{2}' )
    hist.GetYaxis().SetTitle('C^{(33)}_{uW} (#Lambda/TeV)^{2}' )
else:
    hist.GetXaxis().SetTitle('C_{' + args.variables[0].replace('c','').replace('p','#phi').replace('M','') + '} (#Lambda/TeV)^{2}' )
    hist.GetYaxis().SetTitle('C_{' + args.variables[1].replace('c','').replace('p','#phi').replace('M','') + '} (#Lambda/TeV)^{2}' )

hist.GetXaxis().SetTitleFont(42)
hist.GetYaxis().SetTitleFont(42)
hist.GetZaxis().SetTitleFont(42)
hist.GetXaxis().SetLabelFont(42)
hist.GetYaxis().SetLabelFont(42)
hist.GetZaxis().SetLabelFont(42)

hist.GetXaxis().SetTitleOffset(1.4)
hist.GetYaxis().SetTitleOffset(1.4)

hist.GetXaxis().SetTitleSize(0.04)
hist.GetYaxis().SetTitleSize(0.04)
hist.GetZaxis().SetTitleSize(0.04)
hist.GetXaxis().SetLabelSize(0.04)
hist.GetYaxis().SetLabelSize(0.04)
hist.GetZaxis().SetLabelSize(0.04)

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextFont(42)
latex1.SetTextAlign(11)

latex1.DrawLatex(0.15, 0.92, 'CMS Simulation'),
latex1.DrawLatex(0.45, 0.92, 'L=%i fb{}^{-1} (%s TeV)' % (int(args.luminosity) if not args.scale else int(args.scale), "14" if args.scale14TeV else "13"))

#latex1.DrawLatex(0.15, 0.92, ' '.join(args.process.split('_')[:2]) + ' (' + args.detector + ')')
#latex1.DrawLatex(0.55, 0.92, '%3.1f fb{}^{-1} @ 13 TeV'%(float(args.luminosity) if args.scale is None else float(args.scale)) )

plot_directory_ = os.path.join(\
    plot_directory,
    '%s_%s'%(args.level, args.version),
    args.detector,
    args.sample,
    'backgrounds',
    'nll_small' if args.small else 'nll',
    args.selection)

if not os.path.isdir( plot_directory_ ):
    os.makedirs( plot_directory_ )

for e in [".png",".pdf",".root"]:
    cans.Print( plot_directory_ + '/' + '_'.join(args.variables + ['lumi'+str(args.luminosity) if args.scale is None else 'lumi'+str(args.scale), "14TeV" if args.scale14TeV else "13TeV"]) + e)

