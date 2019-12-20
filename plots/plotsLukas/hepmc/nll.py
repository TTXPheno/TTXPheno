''' Plot script WC parameter LogLikelihood
'''

''' 
recottZRegionsHepMC1l = getRegions2D("recoMet_pt", [0,100,200,300,-1], "recoJet_pt[0]", [0,100,200,400,-1])# + [Region("recoZ_pt", (400, -1))]
recottZRegionsHepMCOld = getRegions2D("recoMet_pt", [0,100,200,400,600,-1], "recoJet_pt[0]", [0,100,200,400,-1])# + [Region("recoZ_pt", (400, -1))]
recottZRegionsHepMCBin = getRegions2D("recoMet_pt", [400,600], "recoJet_pt[0]", [0,100,200,400,-1])# + [Region("recoZ_pt", (400, -1))]
recottZRegionsHepMCShort = getRegions2D("recoMet_pt", [0,100,200,-1], "recoJet_pt[0]", [0,100,200,400,-1])# + [Region("recoZ_pt", (400, -1))]
recottZRegionsHepMCLong = getRegions2D("recoMet_pt", [0,100,200,300,400,500,600,-1], "recoJet_pt[0]", [0,100,200,400,-1])# + [Region("recoZ_pt", (400, -1))]
recottZRegionsHepMCFine = getRegions2D("recoMet_pt", [0,100,200,300,400,600,-1], "recoJet_pt[0]", [0,100,200,400,-1])# + [Region("recoZ_pt", (400, -1))]
'''
# Standard imports 
import sys
import ROOT
import imp
import pickle
import ctypes
import numpy as np
import itertools
import operator

from shutil import copyfile

from math import sqrt
# turn off graphics
ROOT.gROOT.SetBatch( True )

# RootTools
from RootTools.core.standard import *

from Analysis.Tools.MergingDirDB                import MergingDirDB

from multiprocessing import Pool

# Logger
import TTXPheno.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   'DEBUG', logFile = None)
logger_rt = logger_rt.get_logger('INFO', logFile = None)

# TTXPheno
from TTXPheno.samples.benchmarks        import * 
from TTXPheno.Tools.user                import plot_directory, cardfileLocation, cache_directory
from TTXPheno.Tools.hepMCCutInterpreter import cutInterpreter

ROOT.gStyle.SetNumberContours(255)

# Arguments
import argparse

argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--version',            action='store',     default='v2', help='Appendix to plot directory')
argParser.add_argument('--bestFit',            action='store_true', help='Run combine with bestFit scenario (wide r ranges)')
argParser.add_argument('--removeCardFiles',    action='store_true', help='remove cardfiles after calculation?')
argParser.add_argument('--selection',          action='store',     default='lepSel3-onZ-njet3p-nbjet1p-Zpt0', help="Specify cut.")
argParser.add_argument('--small',              action='store_true', default=False, help='Run only on a small subset of the data?')
argParser.add_argument('--contours',           action='store_true', help='draw 1sigma and 2sigma contour line?')
argParser.add_argument('--binning',            action='store',     default = [10, 0.0, 0.003], type=float, nargs=3, help = "argument parameters")
argParser.add_argument('--yRange',             action='store',     default = [0, 6], type=float, nargs=2, help = "argument parameters")
argParser.add_argument('--cores',              action='store',     default=1, type=int, help='number of cpu cores for multicore processing')
argParser.add_argument('--overwrite',          action='store_true', help='overwrite datafile?')
argParser.add_argument('--fitOnly',            action='store_true', help='plot only?')
argParser.add_argument('--sample',             action='store',      default='ttZ', choices = ["tt", "ttZ"])
argParser.add_argument('--pdf',                action='store',      default='1d0')

args = argParser.parse_args()

lumi_scale = 136.6
nloXSec   = 0.0915/(0.10099) if args.sample == "ttZ" else 831.76 #inclusive NLO xsec

if "lepSel1" in args.selection:
    if   "old" in args.version:   from TTXPheno.Analysis.regions import recottZRegionsHepMCOld as regions
    elif "bin" in args.version:   from TTXPheno.Analysis.regions import recottZRegionsHepMCBin as regions
    elif "short" in args.version: from TTXPheno.Analysis.regions import recottZRegionsHepMCShort as regions
    elif "long" in args.version:  from TTXPheno.Analysis.regions import recottZRegionsHepMCLong as regions
    elif "fine" in args.version:  from TTXPheno.Analysis.regions import recottZRegionsHepMCFine as regions
    else:                         from TTXPheno.Analysis.regions import recottZRegionsHepMC1l as regions
else:
    from TTXPheno.Analysis.regions import recottZRegionsHepMC as regions

if args.binning[0] > 1:
    xRange = np.linspace( args.binning[1], args.binning[2], int(args.binning[0]), endpoint=False)
else:
    xRange = [ 0.5 * ( args.binning[2] - args.binning[1] ) ]

# Samples
from TTXPheno.samples.hepmc_samples_11_06  import *
hepSample = ttbarZ if args.sample == "ttZ" else ttbar
hepSample.root_samples_dict = { name:sample for name, sample in hepSample.root_samples_dict.iteritems() if name.startswith(args.pdf+"_") or name == "PP"}

baseDir       = os.path.join( cache_directory, "hepmc", "limits" )
if not os.path.exists( baseDir ): os.makedirs( baseDir )

cacheFileName   = os.path.join( baseDir, "calculatedLimits" )
limitCache      = MergingDirDB( cacheFileName )

sample_directory = hepSample.name
if args.small:     sample_directory += "_small"

addon = []
#save data file
filename = '_'.join( ['hepMCnll', args.sample ] + map( str, args.binning ) + [ args.selection ] + addon ) + '.data'

def getHiggsWeight( c ):
    sigmaC  = (1-c)**2*hepSample.samples_dict['PP'].xSection + \
              (1-c)*c*hepSample.samples_dict[args.pdf+'_GH'].xSection + \
              (1-c)*c*hepSample.samples_dict[args.pdf+'_HG'].xSection + \
              c**2*hepSample.samples_dict[args.pdf+'_HH'].xSection

    return sigmaC

#do the calculation
if not os.path.isfile('dat/' + filename) or args.overwrite:

    if not args.fitOnly:

        # Import samples
        sample_file     = "$CMSSW_BASE/python/TTXPheno/samples/benchmarks.py"
        loadedSamples   = imp.load_source( "samples", os.path.expandvars( sample_file ) )

        ttZSample       = getattr( loadedSamples, "fwlite_ttZ_ll_LO_order3_8weights" )
        ttSample        = getattr( loadedSamples, "fwlite_tt_full_LO_order2_15weights_CMS" )
        WZSample        = getattr( loadedSamples, "fwlite_WZ_lep_LO_order2_15weights_CMS" )
        ZGammaSample    = getattr( loadedSamples, "fwlite_Zgamma_LO_order2_15weights_CMS" )
        tWZSample       = getattr( loadedSamples, "fwlite_tWZ_LO_order2_15weights_CMS" )
        tWSample        = getattr( loadedSamples, "fwlite_tW_LO_order2_15weights_CMS" )
        tZqSample       = getattr( loadedSamples, "fwlite_tZq_LO_order2_15weights_CMS" )
        ttWSample       = getattr( loadedSamples, "fwlite_ttW_LO_order3_8weights" )
        ttgammaSample   = getattr( loadedSamples, "fwlite_ttgamma_bg_LO_order2_15weights_CMS" )
        WJetsSample     = getattr( loadedSamples, "fwlite_WJetsToLNu_order2_15weights_CMS" )

        if args.sample == "ttZ":
            bg = [\
                  WZSample,
#                  ZGammaSample,
#                  ttSample,
#                  ttWSample,
                  ttgammaSample,
                  tZqSample,
                  tWZSample,
#                  tWSample,
            ]
        else:
            bg = [\
                  WZSample,
                  ZGammaSample,
                  ttZSample,
                  ttWSample,
#                  ttgammaSample,
                  tZqSample,
                  tWZSample,
                  tWSample,
                  WJetsSample,
            ]

        signalPP = hepSample.root_samples_dict['PP']
        signalGH = hepSample.root_samples_dict[args.pdf+'_GH']
        signalHG = hepSample.root_samples_dict[args.pdf+'_HG']
        signalHH = hepSample.root_samples_dict[args.pdf+'_HH']
        hepmcweight = nloXSec/signalPP.xSection
        mgSample = ttZSample if args.sample == "ttZ" else ttSample
        mgScale = mgSample.getYieldFromDraw( weightString="lumiweight1fb", selectionString=cutInterpreter.cutString( args.selection ) )["val"]
        ppScale = signalPP.getYieldFromDraw( weightString="lumiweight1fb*%f"%hepmcweight, selectionString=cutInterpreter.cutString( args.selection ) )["val"]
        fancyScale = mgScale / abs(ppScale) if ppScale else 1.
        print fancyScale

        signal   = [ signalPP, signalGH, signalHG, signalHH ] 

        # set selection string
        selectionString      = cutInterpreter.cutString(args.selection)

        # configure samples
        for sample in signal:
            sample.setWeightString( 'lumiweight1fb*%f*%f/2.5'%(lumi_scale, fancyScale ) ) #correct plots by hand (sorry)
            sample.setSelectionString( selectionString )
            print sample.weightString, sample.name
        for sample in bg:
            sample.setWeightString( 'lumiweight1fb*%f*%f/2.5'%(lumi_scale, 2. if sample.name == tWSample.name else .1 if sample.name == WJetsSample.name else 1.) )
            sample.setSelectionString( selectionString )
            print sample.weightString, sample.name
#            if sample.name == WJetsSample.name: sample.addWeightString(".1")
#            if sample.name == tWSample.name: sample.addWeightString("2.") #xsec correction t and tbar
        # somehow has to be separate from the next loop
        if args.small:
            for sample in signal + bg:
                sample.normalization=1.
                sample.reduceFiles( factor=10 )
                eventScale = 1./sample.normalization
                sample.addWeightString(eventScale)

        observation                    = {}

        signal_btagging_uncertainty    = {}
        signal_mistagging_uncertainty  = {}
        signal_jes_uncertainty         = {}
        signal_leptonId_uncertainty    = {}

        signal_SM_rate                  = {}
        signal_coeffList                = {}

        background_rate                   = {}
        background_btagging_uncertainty   = {}
        background_mistagging_uncertainty = {}
        background_jes_uncertainty        = {}
        background_leptonId_uncertainty   = {}

        nonPromptObservation              = {}

        SMsigmaC = getHiggsWeight( 0 )

        for i_region, region in enumerate(regions):
            # compute signal yield for this region (this is the final code)

            i_r = i_region % 4
            logger.info( "At region %s", region )

            # signal SM
            signal_SM_rate[region]    = signalPP.getYieldFromDraw( selectionString=region.cutString(), weightString="%f"%(nloXSec/SMsigmaC) )['val']

            background_rate[region]                   = {}
            background_btagging_uncertainty[region]   = {}
            background_mistagging_uncertainty[region] = {}
            background_leptonId_uncertainty[region]   = {}
            background_jes_uncertainty[region]        = {}

            for i_background, background in enumerate(bg):
                # compute bg yield for this region (this is the final code)
                background_rate                   [region][background.name] = background.getYieldFromDraw( selectionString=region.cutString() )['val']

                background_jes_uncertainty        [region][background.name] = (1 + .05/(i_r+1.))*(background.name in [WZSample.name, ttZSample.name, ttWSample.name, tZqSample.name, tWZSample.name, tWSample.name]) + (1 + .1/(i_r+1.))*(background.name==ZGammaSample.name) + (1 + .08/(i_r+1.))*(background.name==WJetsSample.name)
                background_btagging_uncertainty   [region][background.name] = (1 + .02/(i_r+1.))*(background.name in [WZSample.name, ttZSample.name, ttWSample.name, tZqSample.name, tWZSample.name, tWSample.name]) + (1 + .02/(i_r+1.))*(background.name==ZGammaSample.name) + (1 + .02/(i_r+1.))*(background.name==WJetsSample.name)
                background_mistagging_uncertainty [region][background.name] = (1 + .01/(i_r+1.))*(background.name in [WZSample.name, ttZSample.name, ttWSample.name, tZqSample.name, tWZSample.name, tWSample.name]) + (1 + .01/(i_r+1.))*(background.name==ZGammaSample.name) + (1 + .04/(i_r+1.))*(background.name==WJetsSample.name)
                background_leptonId_uncertainty   [region][background.name] = (1 + .015/(i_r+1.))*(background.name in [WZSample.name, ttZSample.name, ttWSample.name, tZqSample.name, tWZSample.name, tWSample.name]) + (1 + .01/(i_r+1.))*(background.name==ZGammaSample.name) + (1 + .015/(i_r+1.))*(background.name==WJetsSample.name)

            observation[region] = int( sum( background_rate[region].values() + [signal_SM_rate[region]] ) )


    # Write temporary card file
    from TTXPheno.Tools.cardFileWriter import cardFileWriter
    # non CMS NLL plot
    from TTXPheno.Analysis.ProfiledLoglikelihoodFit import ProfiledLoglikelihoodFit


    def calculation( c_var ):

        sigmaC = getHiggsWeight( c_var )

        nameList = [args.sample] + args.binning + [ args.selection, 'small' if args.small else 'full', c_var ]
        cardname = '%s_nll_card'%'_'.join( map( str, nameList ) )
        cardFilePath = os.path.join( cardfileLocation, cardname + '.txt' )

        c = cardFileWriter.cardFileWriter()

        if not args.fitOnly:
#            print 'run cardfile'

            # uncertainties
            c.reset()
            c.addUncertainty('Luminosity', 'lnN')
            c.addUncertainty('JER',             'lnN')
            c.addUncertainty('btagging',       'lnN')
            c.addUncertainty('mistagging',     'lnN')
            c.addUncertainty('LeptonID',       'lnN')

            signal_rate                  = {}
            for i_region, region in enumerate(regions):

                i_r = i_region % 4

                signal_rate[region]    = signalPP.getYieldFromDraw( selectionString=region.cutString(), weightString="%f"%(nloXSec*(1-c_var)**2/sigmaC) )['val']
                signal_rate[region]   += signalGH.getYieldFromDraw( selectionString=region.cutString(), weightString="%f"%(nloXSec*(1-c_var)*c_var/sigmaC) )['val']
                signal_rate[region]   += signalHG.getYieldFromDraw( selectionString=region.cutString(), weightString="%f"%(nloXSec*(1-c_var)*c_var/sigmaC) )['val']
                signal_rate[region]   += signalHH.getYieldFromDraw( selectionString=region.cutString(), weightString="%f"%(nloXSec*c_var**2/sigmaC) )['val']

                signal_btagging_uncertainty   [region] = 1 + .015/(i_r+1.)
                signal_mistagging_uncertainty [region] = 1 + .01/(i_r+1.)
                signal_leptonId_uncertainty   [region] = 1 + .01/(i_r+1.)
                signal_jes_uncertainty        [region] = 1 + .05/(i_r+1.)

                bin_name = "Region_%i" % i_region
                nice_name = region.__str__()
                c.addBin(bin_name, ['_'.join(s.name.split('_')[1:3]) for s in bg], nice_name)

                c.specifyObservation( bin_name, observation[region] )

                c.specifyExpectation( bin_name, 'signal', signal_rate[region]                                 )

                c.specifyFlatUncertainty( 'Luminosity', 1.026 )
                c.specifyUncertainty( 'JER',         bin_name, 'signal', signal_jes_uncertainty[region]        )
                c.specifyUncertainty( 'btagging',   bin_name, 'signal', signal_btagging_uncertainty[region]   )
                c.specifyUncertainty( 'mistagging', bin_name, 'signal', signal_mistagging_uncertainty[region] )
                c.specifyUncertainty( 'LeptonID',   bin_name, 'signal', signal_leptonId_uncertainty[region] )

                for background in bg:
                    c.specifyExpectation( bin_name, '_'.join( background.name.split('_')[1:3] ), background_rate[region][background.name] )
                    c.specifyUncertainty( 'JER',           bin_name, '_'.join( background.name.split('_')[1:3] ), background_jes_uncertainty[region][background.name])
                    c.specifyUncertainty( 'btagging',     bin_name, '_'.join( background.name.split('_')[1:3] ), background_btagging_uncertainty[region][background.name])
                    c.specifyUncertainty( 'mistagging',   bin_name, '_'.join( background.name.split('_')[1:3] ), background_mistagging_uncertainty[region][background.name])
                    c.specifyUncertainty( 'LeptonID',     bin_name, '_'.join( background.name.split('_')[1:3] ), background_leptonId_uncertainty[region][background.name])
                    
            c.writeToFile( cardFilePath )

        else:
            logger.info( "Running only NLL Fit with given CardFile %s"%cardFilePath)

        if not os.path.isfile( cardFilePath ):
            raise ValueError('CardFiles not found! Run script without --fitOnly!')

        if args.bestFit: r = (0.99, 1.01)
        else: r = (0., 2.)

        profiledLoglikelihoodFit = ProfiledLoglikelihoodFit( cardFilePath )
        profiledLoglikelihoodFit.make_workspace(rmin=r[0], rmax=r[1])
        nll = profiledLoglikelihoodFit.likelihoodTest()
        profiledLoglikelihoodFit.cleanup(removeFiles=args.removeCardFiles)
        del profiledLoglikelihoodFit

        logger.info( "NLL: %f", nll)
        ROOT.gDirectory.Clear()

        # in very large WC regions, the fit fails, not relevant for the interesting regions
        if nll is None or abs(nll) > 10000 or abs(nll) < 1: nll = 999

        del c

        return c_var, nll


    results = []

    SM = calculation( 0 )

    pool = Pool( processes = args.cores )
    results += pool.map( calculation, xRange )
    pool.close()
    del pool

    with open('/tmp/'+filename, 'w') as f:
        for item in [SM]+results:
            f.write( "%s\n" % ','.join( map( str, list(item) ) ) )

else:
    with open('dat/'+filename, 'r') as f:
        data = f.readlines()

    results = []
    for i, line in enumerate(data):
        vals = map( float, line.split('\n')[0].split(',') )
        if i == 0:
            if vals[0] != 0:
                raise ValueError('SM Point in data file is not valid!')
            SM = tuple( vals )
        else: results.append( tuple( vals ) )


#Plot

results = [ (x, 2*(res-SM[1])) for x, res in results]
results.sort( key = lambda res: res[0] )

def toGraph( name, title, data ):
    result  = ROOT.TGraph( len(data) )
    result.SetName( name )
    result.SetTitle( title )
    for j, datapoint in enumerate(data):
        x, val = datapoint
        result.SetPoint(j, x, val)
    c = ROOT.TCanvas()
    result.Draw()
    del c
    #res = ROOT.TGraphDelaunay(result)
    return result

# Plot ranges

polString = "[0]*x**2+[1]*x**3+[2]*x**4+[3]*x**5+[4]*x**6+[5]*x**7+[6]*x**8"
# get TGraph from results data list
xhist = toGraph( "f", "f", results )
func  = ROOT.TF1("func",polString,args.binning[1], args.binning[2] ) 
func.SetNpx(10000)
xhist.Fit(func,"NO")
x68max = func.GetX( 0.989, args.binning[1], args.binning[2] )
x95max = func.GetX( 3.84, args.binning[1], args.binning[2] )
xmax   = func.GetX( args.yRange[1], args.binning[1], args.binning[2] )

sConfig = "_".join( [args.sample, args.selection, args.pdf] )
res = { 95:x95max, 68:x68max }
limitCache.add( sConfig, res, overwrite=True )

xhist.SetLineWidth(0)

func.SetFillColor(ROOT.kWhite)
func.SetFillStyle(1001)
func.SetLineWidth(3)
func.SetLineColor(ROOT.kBlack)

print '68', x68max
print '95', x95max

ROOT.gStyle.SetPadLeftMargin(0.14)
ROOT.gStyle.SetPadRightMargin(0.1)
ROOT.gStyle.SetPadTopMargin(0.11)

# Plot
cans = ROOT.TCanvas("cans","cans",500,500)

if not None in args.yRange:
    xhist.GetYaxis().SetRangeUser( args.yRange[0], args.yRange[1] )
    xhist.GetXaxis().SetRangeUser( args.binning[1], args.binning[2] )

func95 = ROOT.TF1("func95",polString, args.binning[1],x95max ) 
xhist.Fit(func95,"NO")
func95.SetFillColor(ROOT.kOrange+7)
func95.SetFillStyle(1001)
func95.SetLineWidth(0)
func95.SetNpx(1000)

func68 = ROOT.TF1("func68",polString, args.binning[1],x68max ) 
xhist.Fit(func68,"NO")
func68.SetFillColor(ROOT.kSpring-1)
func68.SetFillStyle(1001)
func68.SetLineWidth(0)
func68.SetNpx(1000)

if not None in args.yRange:
    func.GetYaxis().SetRangeUser( args.yRange[0], args.yRange[1] )
    func.GetXaxis().SetRangeUser( args.binning[1], args.binning[2] )
    func68.GetYaxis().SetRangeUser( args.yRange[0], args.yRange[1] )
    func68.GetXaxis().SetRangeUser( args.binning[1], args.binning[2] )
    func95.GetYaxis().SetRangeUser( args.yRange[0], args.yRange[1] )
    func95.GetXaxis().SetRangeUser( args.binning[1], args.binning[2] )
    xhist.GetXaxis().SetRangeUser( 0, xmax )

xhist.Draw("ALO")
func.Draw("COSAME")
func95.Draw("FOSAME")
func68.Draw("FOSAME")
#xhist.Draw("LOSAME")
func.Draw("COSAME")

#cans.SetLogx()
# Redraw axis, otherwise the filled graphes overlay
cans.RedrawAxis()

# dashed line at 1
line5 = ROOT.TLine(args.binning[1], 0.989, xmax, 0.989 )
line5.SetLineWidth(1)
line5.SetLineStyle(7)
line5.SetLineColor(ROOT.kBlack)
# dashed line at 4
line6 = ROOT.TLine(args.binning[1], 3.84, xmax, 3.84 )
line6.SetLineWidth(1)
line6.SetLineStyle(7)
line6.SetLineColor(ROOT.kBlack)

line5.Draw()
line6.Draw()

cans.Update()
xhist.GetYaxis().SetTitle("-2 #Delta ln L")

leg = ROOT.TLegend(0.3,0.7,0.7,0.87)
leg.SetBorderSize(0)
leg.SetTextSize(0.038)
leg.AddEntry(func,"log-likelihood ratio","l")
leg.AddEntry(func68,"68% CL","f")
leg.AddEntry(func95,"95% CL","f")
leg.Draw()

xhist.SetTitle( "" )
xhist.GetXaxis().SetTitle( "c" )

xhist.GetXaxis().SetTitleFont(42)
xhist.GetYaxis().SetTitleFont(42)
xhist.GetXaxis().SetLabelFont(42)
xhist.GetYaxis().SetLabelFont(42)

xhist.GetXaxis().SetTitleOffset(0.97)
xhist.GetYaxis().SetTitleOffset(1.3)

xhist.GetXaxis().SetTitleSize(0.045)
xhist.GetYaxis().SetTitleSize(0.045)
xhist.GetXaxis().SetLabelSize(0.04)
xhist.GetYaxis().SetLabelSize(0.04)

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextFont(42)
latex1.SetTextAlign(11)

latex1.DrawLatex(0.15, 0.92, '#bf{Higgs-PDF Simulation}'),
latex1.DrawLatex(0.6, 0.92, '#bf{%3.1f fb{}^{-1} (13 TeV)}' % (lumi_scale))

#latex2 = ROOT.TLatex()
#latex2.SetNDC()
#latex2.SetTextSize(0.04)
#latex2.SetTextFont(42)
#latex2.SetTextAlign(11)

#latex2.DrawLatex(0.15, 0.9, 'with Stat. uncert. only' if args.statOnly else 'with YR18 syst. uncert.' if not args.noExpUnc else 'with Stat. and Theory uncert. only'),

plot_directory_ = os.path.join( plot_directory, 'hepmc/NLL_%s'%args.version, sample_directory, args.selection )
phpFile = os.path.join( os.environ["CMSSW_BASE"], "src", "RootTools", "plot", "php", "index.php" )

if not os.path.isdir( plot_directory_ ):
    os.makedirs( plot_directory_ )
    copyfile( phpFile, plot_directory_+"/index.php" )

for e in [".png",".pdf",".root"]:
    cans.Print( plot_directory_ + '/' + args.pdf + e)
