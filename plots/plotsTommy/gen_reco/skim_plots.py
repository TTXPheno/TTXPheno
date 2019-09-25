#!/usr/bin/env python

# Standard imports and batch mode
import ROOT, os, itertools
ROOT.gROOT.SetBatch(True)

from math                               import sqrt, cos, sin, pi, cosh
import copy
import pickle

# RootTools
from RootTools.core.standard            import *

# TTXPheno
from TTXPheno.Tools.user                import plot_directory
from TTXPheno.Tools.WeightInfo          import WeightInfo
from TTXPheno.Tools.helpers             import deltaPhi, deltaR, getCollection, getObjDict

# Import samples
from TTXPheno.samples.benchmarks import *


#
# Arguments
#
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',       action='store',      default='INFO',      nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--small',          action='store_true',                                                                        help="Run the file on a small sample (for test purpose), bool flag set to True if used" )
argParser.add_argument('--parameters',     action='store',      default = ['cpt', '1', 'ctp', '1', 'ctpI', '1', 'cpQM', '1', 'cpQ3', '1'],            type=str, nargs='+', help = "argument parameters")
#argParser.add_argument('--parameters',     action='store',      default = ['cpt', '0', 'ctp', '0', 'ctpI', '0', 'cpQM', '0', 'cpQ3', '0'],            type=str, nargs='+', help = "argument parameters")
argParser.add_argument('--order',          action='store',      default=4,               type=int, help='Polynomial order of weight string (e.g. 2)')
argParser.add_argument('--selection',      action='store',      default='lepSel3-njet1p-nbjet1p')
argParser.add_argument('--level',          action='store',     default='reco', nargs='?', choices=['reco', 'gen'], help='Which level of reconstruction? reco, gen')
argParser.add_argument('--luminosity',     action='store',     default=136.6, help='Luminosity for weighting the plots')
argParser.add_argument('--variables',      action='store',     default = ['cpt', 'ctp', 'ctpI', 'cpQM', 'cpQ3'], type=str, nargs='+', help = "argument variables")
args = argParser.parse_args()

# Import additional functions/classes specified for the level of reconstruction
if args.level == 'reco':
    from TTXPheno.Tools.cutInterpreterReco  import cutInterpreter
    from TTXPheno.Tools.objectSelection     import isGoodRecoJet as isGoodJet
    from TTXPheno.Tools.objectSelection     import isGoodRecoLepton as isGoodLepton
else:
    from TTXPheno.Tools.cutInterpreterGen   import cutInterpreter
    from TTXPheno.Tools.objectSelection     import isGoodGenJet as isGoodJet
    from TTXPheno.Tools.objectSelection     import isGoodGenLepton as isGoodLepton

preTag = 'reco' if args.level == 'reco' else 'gen'
tag    = 'reco' if args.level == 'reco' else 'genLep'

#
# Logger
#
import TTXPheno.Tools.logger as logger 
import RootTools.core.logger as logger_rt 
logger = logger.get_logger( args.logLevel, logFile = None) 
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

# Make subdirectory
subDirectory = []
if args.small: subDirectory.append("small")
subDirectory = '_'.join( subDirectory )

# Format WC input parameters
colors = [ ROOT.kRed+1, ROOT.kGreen+2, ROOT.kOrange+1, ROOT.kViolet+9, ROOT.kSpring-7, ROOT.kRed+2,  ROOT.kPink-9, ROOT.kBlue,  ROOT.kRed-7, ROOT.kRed-10, ROOT.kRed+3,  ROOT.kGreen-7, ROOT.kGreen-10, ROOT.kGreen+3,  ROOT.kPink-7, ROOT.kPink-10, ROOT.kPink+3, ROOT.kGray+2, ROOT.kYellow-7 ]
colorsBg = [ ROOT.kAzure-3, ROOT.kGreen-2, ROOT.kCyan-9, ROOT.kRed+2, ROOT.kGray+2, ROOT.kYellow-7, ROOT.kViolet+6, ROOT.kBlue+2 ]

params = []
if args.parameters is not None:
    coeffs = args.parameters[::2]
    str_vals = args.parameters[1::2]
    vals = list( map( float, str_vals ) )
    for i_param, (coeff, val, str_val) in enumerate(zip(coeffs, vals, str_vals)):
        params.append( [{
            'legendText': ' '.join([coeff,str_val]),
            'WC' : { coeff:val },
            'color' : colors[i_param],
            }])

params.append( [{'legendText':'SM', 'WC':{}, 'color':ROOT.kBlack}] )

# Variables
# List of variables where gen is replaced by reco for reco
read_variables_gen = [
                      "lumiweight1fb/F",
                      "genMet_pt/F", "genMet_phi/F",
                      "ngenJet/I", #"genJet[pt/F,eta/F,phi/F]",
                      "ngenLep/I", #"genLep[pt/F,eta/F,phi/F,pdgId/I]",
                      "genW_pt/F", "genW_eta/F", "genW_phi/F", "genW_mass/F",
                      "genBj0_pt/F", "genBj0_phi/F", "genBj0_eta/F",
                      "genBj1_pt/F", "genBj1_phi/F", "genBj1_eta/F",
                     ]

# List of variables where genLep is replaced by reco for reco
read_variables_genLep = []

if args.level == 'reco':
    read_variables_gen    = [ variable.replace('gen', 'reco') for variable in read_variables_gen ]
    read_variables_genLep = [ variable.replace('genLep', 'reco') for variable in read_variables_genLep ]
    read_variables_gen.append("recoJet[pt/F,eta/F,phi/F,bTag/F]")
    read_variables_gen.append("recoLep[pt/F,eta/F,phi/F,pdgId/I,isolationVar/F,isolationVarRhoCorr/F,sumPtCharged/F,sumPtNeutral/F,sumPtChargedPU/F,sumPt/F,ehadOverEem/F,genIndex/I]")
else:
    read_variables_gen.append("genLep[pt/F,phi/F,eta/F,pdgId/I]")
    read_variables_gen.append("genJet[pt/F,eta/F,phi/F,matchBParton/I]")

read_variables = read_variables_gen + read_variables_genLep
read_variables = list( set( read_variables ) ) # remove double entries
#read_variables.append( VectorTreeVariable.fromString('p[C/F]', nMax=2000) )

# define signal samples
sample = []

from TTXPheno.samples.benchmarks import *

#sample = tWW1j_LO_order4_5weights
sample = fwlite_tWZ_LO_order2_15weights_CMS

# ------- TODO ----------
# Background
TTBar = fwlite_tt_full_LO_order2_15weights_CMS
#TW = TW_LO_GEN
#TTZ = TTZ_LO_GEN
#WZ = WZ_LO_GEN

#bg = [ TTBar, TW, TTZ, WZ ]
bg = [ TTBar ]

# Polynomial parametrization
w = WeightInfo( sample.reweight_pkl )
w.set_order(int(args.order))

def checkReferencePoint( sample ):
    ''' check if sample is simulated with a reference point
    '''
    return pickle.load(file(sample.reweight_pkl))['ref_point'] != {}

if args.small:
    for s in [sample] + bg:
        s.reduceFiles( to = 10 )

# configure samples
for s in [sample] + bg:
    # Scale the plots with number of events used (implemented in ref_lumiweight1fb)
    s.event_factor = s.nEvents / float( s.chain.GetEntries() )
    s.setSelectionString( cutInterpreter.cutString(args.selection) )
    if checkReferencePoint( s ):
        s.read_variables = ["ref_lumiweight1fb/F", VectorTreeVariable.fromString('p[C/F]', nMax=2000)]

# draw all WC + SM as line
stackList = [ [sample] for param in params ]

# draw all bg filled
bgParams = []
stackList += [ bg ]
bgParams = [[ {'legendText':s.name.split('_')[1], 'WC':{}, 'color':colorsBg[i]} for i, s in enumerate(bg) ]]

stack = Stack( *stackList )

allParams = params + bgParams

#print allParams
#exit()

# Reweight
def get_reweight( param, sample_ ):
   
    print w.get_weight_string( **param['WC'] )
    func_ = w.get_weight_func( **param['WC'] )   
    
    def reweightRef( event, sample ):
        return func_( event, sample ) * event.ref_lumiweight1fb * float(args.luminosity) * float(sample.event_factor)
        
    def reweightNoRef( event, sample ):
        return event.lumiweight1fb * float(args.luminosity) * float(sample.event_factor)
    
    return reweightRef if checkReferencePoint( sample_ ) else reweightNoRef

weight = [ [ get_reweight( allParams[i][j], sample_ ) for j, sample_ in enumerate(stackComponent) ] for i, stackComponent in enumerate(stack) ]


# Text on the plots
def drawObjects( ):
    tex = ROOT.TLatex()
    tex.SetNDC()
    tex.SetTextSize(0.04)
    tex.SetTextAlign(11) # align right
    lines = [
      (0.15, 0.95, 'CMS Simulation'), 
    ]
    return [tex.DrawLatex(*l) for l in lines] 

# Helpers
def addTransverseVector( p_dict ):
    ''' add a transverse vector for further calculations
    '''
    p_dict['vec2D'] = ROOT.TVector2( p_dict['pt']*cos(p_dict['phi']), p_dict['pt']*sin(p_dict['phi']) )

def addTLorentzVector( p_dict ):
    ''' add a TLorentz 4D Vector for further calculations
    '''
    p_dict['vec4D'] = ROOT.TLorentzVector()
    p_dict['vec4D'].SetPtEtaPhiM( p_dict['pt'], p_dict['eta'], p_dict['phi'], 0 )
#    p_dict['vec4D'] = ROOT.TLorentzVector( p_dict['pt']*cos(p_dict['phi']), p_dict['pt']*sin(p_dict['phi']),  p_dict['pt']*sinh(p_dict['eta']), 0 )

def UnitVectorT2( phi ):
    ''' 2D Unit Vector
    '''
    return ROOT.TVector2( cos(phi), sin(phi) )

def makeJets( event, sample, level ):
    ''' Add a list of filtered jets to the event (full list is required for lepton cross cleaning)
    '''
    preTag = 'reco' if level == 'reco' else 'gen'
    tag    = 'reco' if level == 'reco' else 'genLep'

    # load jets
    btag = 'bTag' if level == 'reco' else 'matchBParton'
    event.jets = getCollection( event, '%sJet'%preTag, ['pt', 'eta', 'phi', btag ], 'n%sJet'%preTag )
    event.bjets = list( filter( lambda j: j[btag], event.jets ) )

    # get (second) hardest bjets
    event.bj0 = {'pt':getattr( event, '%sBj0_pt'%preTag ), 'phi':getattr( event, '%sBj0_phi'%preTag ), 'eta':getattr( event, '%sBj0_eta'%preTag )}
    event.bj1 = {'pt':getattr( event, '%sBj1_pt'%preTag ), 'phi':getattr( event, '%sBj1_phi'%preTag ), 'eta':getattr( event, '%sBj1_eta'%preTag )}

    # Add extra vectors
    for p in [event.bj0, event.bj1]:
        addTransverseVector( p )
        addTLorentzVector( p )

    # Import additional functions/classes specified for the level of reconstruction
    if level == 'reco': from TTXPheno.Tools.objectSelection  import isGoodRecoJet       as isGoodJet
    else:               from TTXPheno.Tools.objectSelection  import isGoodGenJet      as isGoodJet

    # selection checks
    event.foundBj0 =  isGoodJet( event.bj0 )
   
    # choose your selection on b-jets
    event.passing_bjets = event.foundBj0

def makeMET( event, sample, level ):
    ''' Make a MET vector to facilitate further calculations
    '''
    preTag = 'reco' if level == 'reco' else 'gen'
    tag    = 'reco' if level == 'reco' else 'genLep'

    event.MET = {'pt':getattr(event, '%sMet_pt'%preTag), 'phi':getattr(event, '%sMet_phi'%preTag)}
    addTransverseVector( event.MET )

def makeW( event, sample, level ):
    ''' Make a W vector to facilitate further calculations (either recoZ, genLepZ or genZ)
    '''
    event.W_unitVec2D = UnitVectorT2( getattr( event, '%sW_phi'%level     ) )
    event.W_vec4D     = ROOT.TLorentzVector()
    event.W_vec4D.SetPtEtaPhiM( getattr( event, '%sW_pt'%level ), getattr( event, '%sW_eta'%level ), getattr( event, '%sW_phi'%level ), getattr( event, '%sW_mass'%level     ) )
    event.W_unitVec3D = event.W_vec4D.Vect().Unit()

def makeLeps( event, sample, level ):
    ''' Add important leptons (no full list of leptons is required for now)
    '''
    preTag = 'reco' if level == 'reco' else 'gen'
    tag    = 'reco' if level == 'reco' else 'genLep'

    # Define W leptons
    event.W_l0 = getObjDict( event, '%sLep_'%preTag, ['pt', 'eta', 'phi', 'pdgId'], 0 )
    event.W_l1 = getObjDict( event, '%sLep_'%preTag, ['pt', 'eta', 'phi', 'pdgId'], 1 )

    # Add extra vectors
    for p in [ event.W_l0, event.W_l1]:
        addTransverseVector( p )
        addTLorentzVector( p )

    # Import additional functions/classes specified for the level of reconstruction
    if level == 'reco': from TTXPheno.Tools.objectSelection  import isGoodRecoLepton    as isGoodLepton
    else:               from TTXPheno.Tools.objectSelection  import isGoodGenLepton   as isGoodLepton

    # We may loose some events by cross-cleaning or by thresholds.
    event.foundWl0     = isGoodLepton( event.W_l0 )
    event.foundWl1     = isGoodLepton( event.W_l1 )
    event.found2lep    = event.W_l0['pdgId'] * event.W_l1['pdgId'] > 0

    # choose your selection on leptons
    event.passing_leptons = event.found2lep and event.foundWl0 and event.foundWl1

def makeObservables( event, sample, level):
    ''' Compute all relevant observables
    '''
    # double b kinematic
    event.bbdPhi = deltaPhi( event.bj0['phi'], event.bj1['phi'] )
    event.bbdR   = deltaR( event.bj0, event.bj1 )

    # double l kinematic
    event.lldPhi = deltaPhi( event.W_l0['phi'], event.W_l1['phi'] )
    event.lldR   = deltaR( event.W_l0, event.W_l1 )

    # signed lepton pt
    event.lep0chargept = event.W_l0['pt'] if event.W_l0['pdgId']>0 else -event.W_l0['pt']
    event.lep1chargept = event.W_l1['pt'] if event.W_l1['pdgId']>0 else -event.W_l1['pt']

    # choose your final selection
    event.passing_checks = event.passing_leptons and event.passing_bjets

sequence = []
level = args.level

sequence.append( lambda event, sample: makeJets( event, sample, level ) )
sequence.append( lambda event, sample: makeMET( event, sample, level ) )
sequence.append( lambda event, sample: makeW( event, sample, level ) )
sequence.append( lambda event, sample: makeLeps( event, sample, level ) )
sequence.append( lambda event, sample: makeObservables( event, sample, level ) )

# Use some defaults
Plot.setDefaults( stack = stack, weight = weight, addOverFlowBin=None )

plots = []

plots.append( Plot(
    name      = 'MET_pt',
    texX      = 'E_{T}^{miss} (GeV)',
    texY      = 'Number of Events / 25 GeV',
    attribute = lambda event, sample: event.MET['pt'] if event.passing_checks else float('nan'),
    binning   = [ 24, 0, 600 ],
))

plots.append( Plot(
    name      = 'l0_pt',
    texX      = 'p_{T}(l_{0}) (GeV)',
    texY      = 'Number of Events / 25 GeV',
    attribute = lambda event, sample: event.W_l0['pt'] if event.passing_checks else float('nan'),
    binning   = [ 12, 0 , 300 ],
))

plots.append( Plot(
    name      = 'l0_eta',
    texX      = '#\eta(l_{0})',
    texY      = 'Number of Events',
    attribute = lambda event, sample: event.W_l0['eta'] if event.passing_checks else float('nan'),    
    binning   = [ 20, -3, 3 ],
))

plots.append( Plot(
    name      = 'l1_pt',
    texX      = 'p_{T}(l_{1}) (GeV)',
    texY      = 'Number of Events / 25 GeV',
    attribute = lambda event, sample: event.W_l1['pt'] if event.passing_checks else float('nan'),
    binning   = [ 12, 0, 300 ],
))

plots.append( Plot(
    name      = 'l1_eta',
    texX      = '#\eta(l_{1})',
    texY      = 'Number of Events',
    attribute = lambda event, sample: event.W_l1['eta'] if event.passing_checks else float('nan'),
    binning   = [ 20, -3, 3 ],
))

plots.append( Plot(
    name      = 'jet1_pt',
    texX      = 'p_{T}(leading jet) (GeV)',
    texY      = 'Number of Events / 25 GeV',
    attribute = lambda event, sample: event.jets[0]['pt'] if event.passing_checks and len(event.jets) > 0 else float('nan'),
    binning   = [ 24, 0, 600 ],
))

plots.append( Plot(
    name      = 'jet1_eta',
    texX      = '#\eta(leading jet)',
    texY      = 'Number of Events',
    attribute = lambda event, sample: event.jets[0]['eta'] if event.passing_checks and len(event.jets) > 0 else float('nan'),
    binning   = [ 20, -3, 3 ],
))

plots.append( Plot(
    name      = 'jet2_pt',
    texX      = 'p_{T}(2nd leading jet) (GeV)',
    texY      = 'Number of Events / 25 GeV',
    attribute = lambda event, sample: event.jets[1]['pt'] if event.passing_checks and len(event.jets) > 1 else float('nan'),
    binning   = [ 24, 0, 600 ],
))

plots.append( Plot(
    name      = 'jet2_eta',
    texX      = '#\eta(2nd leading jet)',
    texY      = 'Number of Events',
    attribute = lambda event, sample: event.jets[1]['eta'] if event.passing_checks and len(event.jets) > 1 else float('nan'),
    binning   = [ 20, -3, 3 ],
))

plots.append( Plot(
    name      = 'njets',
    texX      = 'N_{jets}',
    texY      = 'Number of Events',
    attribute = lambda event, sample: getattr( event, 'n%sJet'%preTag ),
    binning   = [ 10, 0, 10 ],
))

plots.append( Plot(
    name      = 'nbjets',
    texX      = 'N_{btags}',
    texY      = 'Number of Events',
    attribute = lambda event, sample: len(event.bjets),
    binning   = [ 4, 0, 4 ],
))

plotting.fill(plots, read_variables = read_variables, sequence = sequence, max_events = -1 if args.small else -1)

for plot in plots:
    histoIndexSM    = len(params) - 1
    histoIndexBg    = len(params) if len(bgParams) != 0 else float('inf')

    for i_h, h in enumerate(plot.histos):
        for j_hi, hi in enumerate(h):
            if i_h == histoIndexBg:
                # fill style for bg
                hi.style = styles.fillStyle(allParams[i_h][j_hi]['color'])
            else:
                # fill style for signal and WC
                hi.style = styles.lineStyle(allParams[i_h][j_hi]['color'])
                hi.SetLineWidth(2)
                if i_h == histoIndexSM:
                    hi.SetLineWidth(3)


for log in [False, True]:
    plot_directory_ = os.path.join(plot_directory, '%s'%(args.level), subDirectory, args.selection if args.selection is not None else 'no_selection', 'log' if log else 'lin')
    
    # plot the legend
    l_plot = copy.deepcopy(plots[0])
    for i_h, h in enumerate(l_plot.histos):
        for j_hi, hi in enumerate(h):
            hi.legendText = allParams[i_h][j_hi]['legendText']
            if i_h == histoIndexBg: 
                hi.style = styles.fillStyle(allParams[i_h][j_hi]['color'])
            else:
                hi.style = styles.lineStyle(allParams[i_h][j_hi]['color'])
            hi.Scale(0.)
            hi.GetXaxis().SetTickLength(0.)
            hi.GetYaxis().SetTickLength(0.)
            hi.GetXaxis().SetLabelOffset(999.)
            hi.GetYaxis().SetLabelOffset(999.)
    l_plot.name = "legend"
    l_plot.texX = ' '
    l_plot.texY = ' '

    plotting.draw(l_plot,
        plot_directory = plot_directory_,
        ratio = None,
        logX = False, logY = log, sorting = True,
        legend = ( (0.17,0.9-0.05*sum(map(len, l_plot.histos))/3,0.9,0.9), 3),
        drawObjects = drawObjects(),
        copyIndexPHP = True,
    )

    # plot the plots
    for p, plot in enumerate(plots):
        histoIndexSM    = len(params) - 1
        histoIndexBg    = len(params) if len(bgParams) != 0 else float('inf')

        for i_h, h in enumerate(plot.histos):
            for j_hi, hi in enumerate(h):
                hi.legendText = allParams[i_h][j_hi]['legendText']
                hi.GetXaxis().SetTickLength(0.04)
                hi.GetYaxis().SetTickLength(0.04)
                hi.GetYaxis().SetTitleOffset(1.)
                hi.GetXaxis().SetTitleSize(0.035)
                hi.GetYaxis().SetTitleSize(0.035)
   
        if not max(l[0].GetMaximum() for l in plot.histos): continue # Empty plot
        
        plotting.draw(plot, 
            plot_directory = plot_directory_,
            ratio = None,
            logX = False, logY = log, sorting = True, 
            yRange = (0.03, "auto") if log else (0., "auto"),
            legend = ( (0.17,0.9-0.05*sum(map(len, plot.histos))/3,0.9,0.9), 3),
            drawObjects = drawObjects(),
            copyIndexPHP = True,
        )


