#!/usr/bin/env python
''' Analysis script for standard plots
'''

# Standard imports
import ROOT, os, imp, sys, copy
ROOT.gROOT.SetBatch(True)
import itertools
import pickle
from math                               import isnan, ceil, pi

# TTXPheno
from TTXPheno.Tools.helpers              import getCollection, getObjDict

# RootTools
from RootTools.core.standard            import *
from TTXPheno.samples.benchmarks        import *

# Internal Imports
from TTXPheno.Tools.user                import plot_directory
from TTXPheno.Tools.hepMCCutInterpreter import cutInterpreter

# Default Parameter
loggerChoices = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET']

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='INFO', nargs='?', choices=loggerChoices,                                help="Log level for logging")
argParser.add_argument('--selection',          action='store',      default='all')#lepSel3-offZ-nJet2p-nBJet1p')
argParser.add_argument('--version',            action='store',      default='v0')
argParser.add_argument('--sample',             action='store',      default='tt', choices = ["tt", "ttZ"])
argParser.add_argument('--pdf',                action='store',      default='1d0')
argParser.add_argument('--small',              action='store_true', default=False,                                                                   help='Run only on a small subset of the data?', )
argParser.add_argument('--normalize',          action='store_true', default=False,                                                                   help="Normalize yields" )
argParser.add_argument('--c',                  action='store',      default=0.1, type=float,                                                         help="BSM fraction" )
args = argParser.parse_args()

# Logger
import TTXPheno.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

# Samples
from TTXPheno.samples.hepmc_samples_11_06      import *
hepSample = ttbarZ if args.sample == "ttZ" else ttbar
nloXSec   = 0.0915/(0.10099) if args.sample == "ttZ" else 831.76 #inclusive NLO xsec

hepSample.root_samples_dict = { name:sample for name, sample in hepSample.root_samples_dict.iteritems() if name.startswith(args.pdf+"_") or name == "PP"}

sample_directory = hepSample.name
if args.small:     sample_directory += "_small"
if args.normalize: sample_directory += "_normalize"

def drawObjects( lumi_scale ):
    tex = ROOT.TLatex()
    tex.SetNDC()
    tex.SetTextSize(0.04)
    tex.SetTextAlign(11) # align right
    lines = [
      (0.15, 0.95, 'Higgs-PDF Simulation (c=%s)'%(str(args.c))), 
      (0.65, 0.95, '%3.1f fb{}^{-1} (13 TeV)' %lumi_scale)
    ]
    return [tex.DrawLatex(*l) for l in lines] 


addFac = 1#000. #FIXME
if args.normalize:
    scaling = { i:0 for i in xrange(len(hepSample.root_samples_dict)) }
else:
    sigmaC  = (1-args.c)**2*hepSample.samples_dict['PP'].xSection + \
              (1-args.c)*args.c*hepSample.samples_dict[args.pdf+'_GH'].xSection + \
              (1-args.c)*args.c*hepSample.samples_dict[args.pdf+'_HG'].xSection + \
              args.c**2*hepSample.samples_dict[args.pdf+'_HH'].xSection

    hepSample.root_samples_dict['PP'].weight =           lambda event, sample: addFac*nloXSec*(1-args.c)**2/sigmaC
    hepSample.root_samples_dict[args.pdf+'_GH'].weight = lambda event, sample: addFac*nloXSec*args.c*(1-args.c)/sigmaC
    hepSample.root_samples_dict[args.pdf+'_HG'].weight = lambda event, sample: addFac*nloXSec*args.c*(1-args.c)/sigmaC
    hepSample.root_samples_dict[args.pdf+'_HH'].weight = lambda event, sample: addFac*nloXSec*(args.c)**2/sigmaC


# Plotting
def drawPlots( plots, mode ):

    # add signal histos to total histo
    for plot in plots:
#        for hep_histo in plot.histos[1:-3]:
#            plot.histos[-2][0].Add(hep_histo[0])
        plot.histos[5][0].Add(plot.histos[2][0]) #HG
        plot.histos[5][0].Add(plot.histos[3][0]) #GH
        plot.histos[5][0].Add(plot.histos[4][0]) #HH

    # add bg histos to all
    for plot in plots:
        for bg_histo in plot.histos[-1]:
            for signal_histos in plot.histos[:-1]:
                signal_histos[0].Add(bg_histo)

    for plot in plots:
        for i_h, h in enumerate(plot.histos):
            for j_hi, hi in enumerate(h):
                if i_h == len(plot.histos)-1 or i_h == len(plot.histos)-2:
                    # fill style for bg
                    hi.style = styles.lineStyle(bgcolors[j_hi])
                elif i_h == len(plot.histos)-3:
                    # fill style for signal PP
                    hi.style = styles.lineStyle( ROOT.kBlack, width=3  )
                else:
                    # fill style for signal Higgs
                    hi.style = styles.lineStyle( colors.values()[i_h-2], width=2, dashed=True  )

    for log in [False, True]:
        plot_directory_ = os.path.join( plot_directory, 'hepmc/checks_%s'%args.version, sample_directory, args.selection, args.pdf, "c%s"%str(args.c).replace(".","p"),"log" if log else "lin" )

        for plot in plots:
            if not max(l[0].GetMaximum() for l in plot.histos): 
                continue # Empty plot
            postFix = ""# (legacy)"
            extensions_ = ["pdf", "png"] if mode in ['all', 'SF', 'mue'] else ['png']

            plotting.draw( plot,
	                       plot_directory = plot_directory_,
                           extensions = extensions_,
#                           ratio = {'yRange': (0.2, 1.8), 'histos':[(i,len(mc)) for i in xrange(len(mc + hepSample.root_samples_dict.values())) ], 'texY':'Ratio'},
#	                       ratio = None,
	                       logX = False, logY = log, sorting = True,
	                       yRange = (0.9, "auto") if log else (0.001, "auto"),
	                       scaling = scaling if args.normalize else {},
	                       legend = [ (0.15,0.88-0.03*sum(map(len, plot.histos)),0.95,0.88), 3],
	                       drawObjects = drawObjects( lumi_scale ) if not args.normalize else drawObjects( lumi_scale ),
                           copyIndexPHP = True,
                         )

def getYieldPlot( index ):
    return Plot(
                name      = 'yield',
                texX      = 'yield',
                texY      = 'Number of Events',
                attribute = lambda event, sample: 0.5 + index,
                binning   = [ 3, 0, 3 ],
                )

recoJetVarString      = "pt/F,eta/F,phi/F,bTag/F,bTagPhys/I,nCharged/I,nNeutrals/I,pt_JEC_up/F,pt_JEC_up/F,bTag_loose/I,bTag_medium/I,bTag_tight/I,bTag_looswMTD/I,bTag_mediumMTD/I,bTag_tightMTD/I"
recoJetVars           = [ item.split("/")[0] for item in recoJetVarString.split(",") ]

recoTopVarString      = "pt/F"#,eta/F,phi/F,mass/F"
recoTopVars           = [ item.split("/")[0] for item in recoTopVarString.split(",") ]

recoLeptonVarString   = "pt/F,eta/F,phi/F,pdgId/I,isolationVar/F,isolationVarRhoCorr/F,sumPtCharged/F,sumPtNeutral/F,sumPtChargedPU/F,sumPt/F,ehadOverEem/F"
recoLeptonVars        = [ item.split("/")[0] for item in recoLeptonVarString.split(",") ]

recoPhotonVarString   = "pt/F,phi/F,eta/F,isolationVar/F,isolationVarRhoCorr/F,sumPtCharged/F,sumPtNeutral/F,sumPtChargedPU/F,sumPt/F,ehadOverEem/F,genIndex/I,minLeptonDR/F,minLeptonPt/F,minJetDR/F"
recoPhotonVars        = [ item.split("/")[0] for item in recoPhotonVarString.split(",") ]



# Read variables and sequences
read_variables  = ["lumiweight1fb/F",

                   "nBTag/I",
                   "nBTag_JEC_down/I","nBTag_JEC_up/I",
                   "nBTag_loose/I","nBTag_medium/I","nBTag_tight/I","nBTag_looswMTD/I","nBTag_mediumMTD/I","nBTag_tightMTD/I",

                   "recoBjNonZlep_index/I",
                   "recoBjNonZhad_index/I",
                   "recoBjLeadlep_index/I",
                   "recoBjLeadhad_index/I",

                   "nrecoPhoton/I",
                   "recoPhoton[%s]"   %recoPhotonVarString,

                   "nrecoJets_JEC_down/I","nrecoJets_JEC_up/I",
                   "nrecoJet/I",
                   "recoJet[%s]"      %recoJetVarString,

                   "nrecoLep/I",
                   "recoLep[%s]"   %recoLeptonVarString,

                   "recoMet_pt/F", "recoMet_phi/F",

                   "recoZ_l1_index/I",
                   "recoZ_l2_index/I",
                   "recoNonZ_l1_index/I",
                   "recoNonZ_l2_index/I",
                   "recoZ_pt/F",
                   "recoZ_eta/F",
                   "recoZ_phi/F",
                   "recoZ_mass/F",
                   "recoZ_lldPhi/F",
                   "recoZ_lldR/F",
                   "recoZ_cosThetaStar/F",

                   "reweight_BTag_B/F",
                   "reweight_BTag_L/F",
                   "reweight_id_mu/F",
                   "reweight_id_ele/F",

                  ]

read_variables += [ "recoBj0_" + var for var in recoJetVarString.split(",") ]
read_variables += [ "recoBj1_" + var for var in recoJetVarString.split(",") ]



def addBTag( event, sample ):
    event.jets = getCollection( event, 'recoJet', [ "bTag" ], 'nrecoJet' )
    event.nBTag = len( filter( lambda j: j["bTag"], event.jets ) )

def makeObservables( event, sample ):
    ''' Compute all relevant observables
    '''
    # double b kinematic
    event.lldPhi = deltaPhi( event.recoLep_phi[0], event.recoLep_phi[1] )
    event.lldR   = deltaR( { "pt":event.recoLep_pt[0], "eta":event.recoLep_eta[0], "phi":event.recoLep_phi[0] }, { "pt":event.recoLep_pt[0], "eta":event.recoLep_eta[0], "phi":event.recoLep_phi[0] } )

def printObjects(event, sample):
    if not "ttbar_" in sample.name: return
    print "weight", event.lumiweight1fb


# Sequence
sequence = [\
            addBTag,
#            makeObservables,
#            printObjects,
           ]

# Import samples
sample_file     = "$CMSSW_BASE/python/TTXPheno/samples/benchmarks.py"
loadedSamples   = imp.load_source( "samples", os.path.expandvars( sample_file ) )

ttZSample       = getattr( loadedSamples, "fwlite_ttZ_ll_LO_order3_8weights" )
ttSample        = getattr( loadedSamples, "fwlite_tt_full_LO_order2_15weights_comp_CMS" )
WZSample        = getattr( loadedSamples, "fwlite_WZ_lep_LO_order2_15weights_CMS" )
ZGammaSample    = getattr( loadedSamples, "fwlite_Zgamma_LO_order2_15weights_CMS" )
tWZSample       = getattr( loadedSamples, "fwlite_tWZ_LO_order2_15weights_CMS" )
tWSample        = getattr( loadedSamples, "fwlite_tW_LO_order2_15weights_CMS" )
tZqSample       = getattr( loadedSamples, "fwlite_tZq_LO_order2_15weights_CMS" )
ttWSample       = getattr( loadedSamples, "fwlite_ttW_LO_order3_8weights" )
ttgammaSample   = getattr( loadedSamples, "fwlite_ttgamma_bg_LO_order2_15weights_CMS" )
WJetsSample     = getattr( loadedSamples, "fwlite_WJetsToLNu_order2_15weights_CMS" )

# cross section correction (t and tbar) + NLO correction
WJetsSample.weight = lambda event, sample: .1
tWSample.weight = lambda event, sample: 2

if args.sample == "ttZ":
    mc = [\
          WZSample,
#          ZGammaSample,
#          ttSample,
#          ttWSample,
          ttgammaSample,
          tZqSample,
          tWZSample,
#          tWSample,
    ]
else:
    mc = [\
#          WZSample,
#          ZGammaSample,
#          ttZSample,
#          ttWSample,
#          ttgammaSample,
#          WJetsSample,
#          tZqSample,
#          tWZSample,
#          tWSample,
    ]

#colors
colors = {'PP':ROOT.kGreen+2, 'HH':ROOT.kOrange+10, 'HG':ROOT.kViolet+6, 'GH':ROOT.kBlue+2, 'ttZ':ROOT.kGray}
bgcolors = [ ROOT.kRed+1, ROOT.kGreen+2, ROOT.kOrange+1, ROOT.kViolet+9, ROOT.kSpring-7, ROOT.kRed+2,  ROOT.kPink-9, ROOT.kBlue,  ROOT.kRed-7, ROOT.kRed-10, ROOT.kRed+3,  ROOT.kGreen-7, ROOT.kGreen-10 ]

for i, s in enumerate(mc):
    s.styles = styles.lineStyle( bgcolors[i] )

lumi_scale = 136.6
stackList = [ ]

# Sample definition
totalSignal = []
stackList += [ [ttZSample if args.sample == "ttZ" else ttSample] ]
for name, sample in hepSample.root_samples_dict.iteritems():
    if name == "PP":
        totSample = copy.deepcopy(sample)
        totSample.texName = args.sample + " (total)"
        totSample.style   = styles.lineStyle( ROOT.kBlack, width=3  )
        sample.texName = name
        sample.style   = styles.lineStyle( colors["PP"], width=2, dashed=True  )
        stackList.insert( 1, [sample] )
    else:
        sample.texName = "%s (%s)" %(name.split("_")[1], name.split("_")[0].split("-")[1].replace("d","."))
        sample.style   = styles.lineStyle( colors[name.split("_")[1]], width=2, dashed=True  )
        stackList.append( [sample] )
#    totalSignal.append(sample)
#stackList.append( totalSignal )

#stackList += [ [totSample] ]
stackList += [ [ttZSample if args.sample == "ttZ" else ttSample] ]
stackList += [ [totSample] ]
#stackList += [ mc ]
stack = Stack( *stackList )

#for sample in stack.samples:
#    print sample.name, sample.weightString
eventScale = 1.
if args.small:
    ttSample.reduceFiles( factor = 10 )
    #for sample in stack.samples:
    #    sample.normalization=1.
    #    sample.reduceFiles( factor=10 )
    #    #eventScale = 1./sample.normalization
    #    #sample.addWeightString(eventScale)

weight_ = lambda event, sample: lumi_scale * event.lumiweight1fb / 2.5 #correct plots by hand (sorry)

# Use some defaults (set defaults before you create/import list of Plots!!)
Plot.setDefaults( stack=stack, weight=staticmethod( weight_ ), selectionString=cutInterpreter.cutString( args.selection ) )#, addOverFlowBin='upper' )

def getPlots():
    plotList = []

    plotList.append( Plot( name = "dl_pt",
      texX = 'p_{T}(ll) [GeV]', texY = "Number of Events",
      attribute = lambda event, sample: event.recoZ_pt,
      binning=[10,0,400],
    ) )
        
    plotList.append( Plot( name = 'dl_phi',
      texX = '#phi(ll)', texY = "Number of Events",
      attribute = lambda event, sample: event.recoZ_phi,
      binning=[10,-pi,pi],
    ) )

    plotList.append( Plot( name = 'dl_eta',
      texX = '#eta(ll)', texY = "Number of Events",
      attribute = lambda event, sample: event.recoZ_eta,
      binning=[10,-3,3],
    ) )
    
    plotList.append( Plot( name = "dl_mass_onZ",
      texX = 'm(ll) [GeV]', texY = "Number of Events",
      attribute = lambda event, sample: event.recoZ_mass,
      binning=[20,70,110],
    ) )
    
    plotList.append( Plot( name = "dl_mass",
      texX = 'm(ll) [GeV]', texY = "Number of Events",
      attribute = lambda event, sample: event.recoZ_mass,
      binning=[30,5,305],
    ) )
    
    plotList.append( Plot( name = 'dl_dPhi',
      texX = '#Delta#phi(ll)', texY = "Number of Events",
      attribute = lambda event, sample: event.recoZ_lldPhi,
      binning=[10,0,pi],
    ) )

    plotList.append( Plot( name = 'dl_dPhi_det',
      texX = '#Delta#phi(ll)', texY = "Number of Events",
      attribute = lambda event, sample: event.recoZ_lldPhi,
      binning=[40,0,pi],
    ) )

    plotList.append( Plot( name = 'dl_dR',
      texX = '#DeltaR(ll)', texY = "Number of Events",
      attribute = lambda event, sample: event.recoZ_lldR,
      binning=[10,0,5],
    ) )

    plotList.append( Plot( name = 'dl_dR_det',
      texX = '#DeltaR(ll)', texY = "Number of Events",
      attribute = lambda event, sample: event.recoZ_lldR,
      binning=[40,0,5],
    ) )

    plotList.append( Plot( name = 'dl_cosThetaStar',
      texX = 'cos#theta*(ll)', texY = "Number of Events",
      attribute = lambda event, sample: event.recoZ_cosThetaStar,
      binning=[10,-1,1],
    ) )

    plotList.append( Plot( name = "j0_pt",
      texX = 'p_{T}(lead jet) [GeV]', texY = "Number of Events",
      attribute = lambda event, sample: event.recoJet_pt[0],
      binning=[20,0,600],
    ) )

    plotList.append( Plot( name = "j0_phi",
      texX = '#phi(lead jet)', texY = "Number of Events",
      attribute = lambda event, sample: event.recoJet_phi[0],
      binning=[20,-pi,pi],
    ) )
    
    plotList.append( Plot( name = "j0_eta",
      texX = '#eta(lead jet)', texY = "Number of Events",
      attribute = lambda event, sample: event.recoJet_eta[0],
      binning=[20,-3,3],
    ) )

    plotList.append( Plot( name = "j1_pt",
      texX = 'p_{T}(sub-lead jet) [GeV]', texY = "Number of Events",
      attribute = lambda event, sample: event.recoJet_pt[1],
      binning=[20,0,600],
    ) )

    plotList.append( Plot( name = "j1_phi",
      texX = '#phi(sub-lead jet)', texY = "Number of Events",
      attribute = lambda event, sample: event.recoJet_phi[1],
      binning=[20,-pi,pi],
    ) )
    
    plotList.append( Plot( name = "j1_eta",
      texX = '#eta(sub-lead jet)', texY = "Number of Events",
      attribute = lambda event, sample: event.recoJet_eta[1],
      binning=[20,-3,3],
    ) )

    plotList.append( Plot( name = "b0_pt",
      texX = 'p_{T}(b_{0}) [GeV]', texY = "Number of Events",
      attribute = lambda event, sample: event.recoBj0_pt,
      binning=[20,0,400],
    ) )

    plotList.append( Plot( name = "b0_phi",
      texX = '#phi(b_{0})', texY = "Number of Events",
      attribute = lambda event, sample: event.recoBj0_phi,
      binning=[20,-pi,pi],
    ) )
    
    plotList.append( Plot( name = "b0_eta",
      texX = '#eta(b_{0})', texY = "Number of Events",
      attribute = lambda event, sample: event.recoBj0_eta,
      binning=[20,-3,3],
    ) )

    plotList.append( Plot( name = "b1_pt",
      texX = 'p_{T}(b_{1}) [GeV]', texY = "Number of Events",
      attribute = lambda event, sample: event.recoBj1_pt,
      binning=[20,0,400],
    ) )
    
    plotList.append( Plot( name = "b1_phi",
      texX = '#phi(b_{1})', texY = "Number of Events",
      attribute = lambda event, sample: event.recoBj1_phi,
      binning=[20,-pi,pi],
    ) )
    
    plotList.append( Plot( name = "b1_eta",
      texX = '#eta(b_{1})', texY = "Number of Events",
      attribute = lambda event, sample: event.recoBj1_eta,
      binning=[20,-3,3],
    ) )
    
    plotList.append( Plot( name = 'Met_pt_coarse',
      texX = 'E_{T}^{miss} [GeV]', texY = "Number of Events",
      attribute = lambda event, sample: event.recoMet_pt,
      binning=[10,0,300],
    ) )
    
    plotList.append( Plot( name = 'Met_pt_wide_coarse',
      texX = 'E_{T}^{miss} [GeV]', texY = "Number of Events",
      attribute = lambda event, sample: event.recoMet_pt,
      binning=[10,0,400],
    ) )
    
    plotList.append( Plot( name = 'Met_pt',
      texX = 'E_{T}^{miss} [GeV]', texY = "Number of Events",
      attribute = lambda event, sample: event.recoMet_pt,
      binning=[20,0,300],
    ) )
    
    plotList.append( Plot( name = 'Met_phi',
      texX = '#phi(E_{T}^{miss})', texY = "Number of Events",
      attribute = lambda event, sample: event.recoMet_phi,
      binning=[10,-pi,pi],
    ) )

    plotList.append( Plot( name = 'l0_pt',
      texX = 'p_{T}(lead lep) [GeV]', texY = "Number of Events",
      attribute = lambda event, sample: event.recoLep_pt[0],
      binning=[20,0,300],
    ) )
    
    plotList.append( Plot( name = 'l0_phi',
      texX = '#phi(lead lep)', texY = "Number of Events",
      attribute = lambda event, sample: event.recoLep_phi[0],
      binning=[20,-pi,pi],
    ) )

    plotList.append( Plot( name = 'l0_eta',
      texX = '#eta(lead lep)', texY = "Number of Events",
      attribute = lambda event, sample: event.recoLep_eta[0],
      binning=[20,-3,3],
    ) )
    
    plotList.append( Plot( name = 'l1_pt',
      texX = 'p_{T}(sub-lead lep) [GeV]', texY = "Number of Events",
      attribute = lambda event, sample: event.recoLep_pt[1],
      binning=[20,0,300],
    ) )
    
    plotList.append( Plot( name = 'l1_phi',
      texX = '#phi(sub-lead lep)', texY = "Number of Events",
      attribute = lambda event, sample: event.recoLep_phi[1],
      binning=[20,-pi,pi],
    ) )

    plotList.append( Plot( name = 'l1_eta',
      texX = '#eta(sub-lead lep)', texY = "Number of Events",
      attribute = lambda event, sample: event.recoLep_eta[1],
      binning=[20,-3,3],
    ) )
    
    plotList.append( Plot( name = "nJet",
      texX = 'N_{jets}', texY = "Number of Events",
      attribute = lambda event, sample: event.nrecoJet,
      binning=[10,0,10],
    ) )

    plotList.append( Plot( name = "nBJet",
      texX = 'N_{b-jets}', texY = "Number of Events",
      attribute = lambda event, sample: event.nBTag,
      binning=[5,0,5],
    ) )

    plotList.append( Plot( name = "nLepton",
      texX = 'N_{lep}', texY = "Number of Events",
      attribute = lambda event, sample: event.nrecoLep,
      binning=[5,0,5],
    ) )

    plotList.append( Plot( name = "nPhoton",
      texX = 'N_{#gamma}', texY = "Number of Events",
      attribute = lambda event, sample: event.nrecoPhoton,
      binning=[3,0,3],
    ) )

    return plotList

plots = getPlots()

# Loop over channels
allPlots = {}
#allModes = [ 'all', 'mumumu', 'mumue', 'muee', 'eee' ]
allModes = [ 'all' ]

for index, mode in enumerate( allModes ):
    logger.info( "Computing plots for mode %s", mode )

    # Define 2l selections
    leptonSelection = cutInterpreter.cutString( mode )

    for sample in stack.samples: sample.setSelectionString( [ leptonSelection ] )

    plotting.fill( plots, read_variables=read_variables, sequence=sequence )

    logger.info( "Plotting mode %s", mode )
    allPlots[mode] = copy.deepcopy(plots) # deep copy for creating SF/all plots afterwards!
    drawPlots( allPlots[mode], mode )

