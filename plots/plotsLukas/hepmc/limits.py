''' Plot script WC parameter LogLikelihood
'''

# Standard imports 
import sys, os
from shutil import copyfile
import ROOT
ROOT.gROOT.SetBatch( True )

# RootTools
from RootTools.core.standard import *

from Analysis.Tools.MergingDirDB        import MergingDirDB
from TTXPheno.Tools.user                import plot_directory, cardfileLocation, cache_directory

# Logger
import TTXPheno.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   'DEBUG', logFile = None)
logger_rt = logger_rt.get_logger('INFO', logFile = None)

ROOT.gStyle.SetNumberContours(255)

# Arguments
import argparse

argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--version',            action='store',     default='v10',                    help='Appendix to plot directory')
argParser.add_argument('--selection',          action='store',     default='lepSel1-njet4p-nbjet1p', help="Specify cut.")
argParser.add_argument('--sample',             action='store',     default='tt', choices = ["tt", "ttZ"])

args = argParser.parse_args()

lumi_scale = 136.6

# Samples
from TTXPheno.samples.hepmc_samples_11_06  import *
hepSample = ttbarZ if args.sample == "ttZ" else ttbar
hepSample.root_samples_dict = { name:sample for name, sample in hepSample.root_samples_dict.iteritems() if "HG" in name}

baseDir         = os.path.join( cache_directory, "hepmc", "limits" )
cacheFileName   = os.path.join( baseDir, "calculatedLimits" )
limitCache      = MergingDirDB( cacheFileName )

res     = {}
res[68] = {}
res[95] = {}
for i, (pdf, val) in enumerate(hepSample.root_samples_dict.iteritems()):
    pdf = pdf.split("_")[0]
    print pdf
    pdfVal  = float(pdf.split("-")[1])
    if int(pdfVal) == 37: continue
    sConfig = "_".join( [args.sample, args.selection, pdf] )
    
    if not limitCache.contains( sConfig ): continue

    tmpRes  = limitCache.get( sConfig )
    res[68][pdfVal] = tmpRes[68]
    res[95][pdfVal] = tmpRes[95]


print res[68]
print res[95]
def toGraph( name, title, data ):
    result  = ROOT.TGraph( len(data) )
    result.SetName( name )
    result.SetTitle( title )
    data = data.items()
    data.sort(key=lambda (x,val): -x)
    for j, (x,val) in enumerate(data):
        result.SetPoint(j, x, val)
    c = ROOT.TCanvas()
    result.Draw()
    del c
    #res = ROOT.TGraphDelaunay(result)
    return result

# Plot ranges

allVal = res[68].values() + res[95].values()
allKey = res[68].keys()   + res[95].keys()

minX = min( allKey )
maxX = max( allKey )
minY = min( allVal )
maxY = max( allVal )

print minX, maxX, minY, maxY
polString = "[0]+[1]*x+[2]*x**2+[3]*x**3+[4]*x**4+[5]*x**5+[6]*x**6+[7]*x**7+[8]*x**8+[9]*log(x)"
# get TGraph from results data list
xhist68 = toGraph( "f68", "f68", res[68] )
xhist95 = toGraph( "f95", "f95", res[95] )
func68  = ROOT.TF1("func68",polString, min(allVal), max(allVal) ) 
func95  = ROOT.TF1("func95",polString, min(allVal), max(allVal) ) 
func68.SetNpx(10000)
func95.SetNpx(10000)
xhist68.Fit(func68,"NO")
xhist95.Fit(func95,"NO")

ROOT.gStyle.SetPadLeftMargin(0.14)
ROOT.gStyle.SetPadRightMargin(0.1)
ROOT.gStyle.SetPadTopMargin(0.11)

# Plot
cans = ROOT.TCanvas("cans","cans",500,500)

xhist68.GetXaxis().SetRangeUser( minX, maxX )
xhist68.GetYaxis().SetRangeUser( minY*0.3, maxY*1.3 )

xhist68.SetMarkerColor(ROOT.kSpring-1)
xhist68.SetLineColor(ROOT.kSpring-1)
xhist68.SetFillColor(ROOT.kSpring-1)
#xhist68.SetLineWidth(2)
xhist68.SetLineWidth(1504)
xhist68.SetFillStyle(3005)

xhist95.SetMarkerColor(ROOT.kOrange+7)
xhist95.SetLineColor(ROOT.kOrange+7)
xhist95.SetFillColor(ROOT.kOrange+7)
#xhist95.SetLineWidth(2)
xhist95.SetLineWidth(1504)
xhist95.SetFillStyle(3005)

func95.SetFillColor(ROOT.kOrange+7)
func95.SetFillStyle(1001)
func95.SetLineWidth(0)
func95.SetNpx(1000)

func68.SetFillColor(ROOT.kSpring-1)
func68.SetFillStyle(1001)
func68.SetLineWidth(0)
func68.SetNpx(1000)

leg = ROOT.TLegend(0.25,0.7,0.45,0.87)
leg.SetBorderSize(0)
leg.SetTextSize(0.038)
leg.AddEntry(xhist68,"68% CL","l")
leg.AddEntry(xhist95,"95% CL","l")

xhist68.SetTitle( "" )
xhist68.GetXaxis().SetTitle( "PDF" )
xhist68.GetYaxis().SetTitle("Limits")

xhist68.GetXaxis().SetTitleFont(42)
xhist68.GetYaxis().SetTitleFont(42)
xhist68.GetXaxis().SetLabelFont(42)
xhist68.GetYaxis().SetLabelFont(42)

xhist68.GetXaxis().SetTitleOffset(0.97)
xhist68.GetYaxis().SetTitleOffset(1.3)

xhist68.GetXaxis().SetTitleSize(0.045)
xhist68.GetYaxis().SetTitleSize(0.045)
xhist68.GetXaxis().SetLabelSize(0.04)
xhist68.GetYaxis().SetLabelSize(0.04)

xhist68.Draw("AC")
xhist95.Draw("CSAME")
#xhist68.Draw("CSAME")
leg.Draw("SAME")
#func95.Draw("LOSAME")
#func68.Draw("LOSAME")

#cans.SetLogx()
# Redraw axis, otherwise the filled graphes overlay
cans.RedrawAxis()

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.04)
latex1.SetTextFont(42)
latex1.SetTextAlign(11)

latex1.DrawLatex(0.15, 0.92, 'Higgs-PDF Sim. (%s)'%(hepSample.name.replace("bar",""))),
latex1.DrawLatex(0.6, 0.92, '%3.1f fb{}^{-1} (13 TeV)' % (lumi_scale))

#latex2 = ROOT.TLatex()
#latex2.SetNDC()
#latex2.SetTextSize(0.04)
#latex2.SetTextFont(42)
#latex2.SetTextAlign(11)

#latex2.DrawLatex(0.15, 0.9, 'with Stat. uncert. only' if args.statOnly else 'with YR18 syst. uncert.' if not args.noExpUnc else 'with Stat. and Theory uncert. only'),

plot_directory_ = os.path.join( plot_directory, 'hepmc/NLL_%s'%args.version, hepSample.name, args.selection )
phpFile = os.path.join( os.environ["CMSSW_BASE"], "src", "RootTools", "plot", "php", "index.php" )

if not os.path.isdir( plot_directory_ ):
    os.makedirs( plot_directory_ )
    copyfile( phpFile, plot_directory_+"/index.php" )

for logx in [False, True]:
    for logy in [False, True]:

        cans.SetLogx(int(logx))
        cans.SetLogy(int(logy))
        cans.Update()

        for e in [".png",".pdf",".root"]:
            cans.Print( plot_directory_ + '/limits%s%s'%("_logx" if logx else "", "_logy" if logy else "") + e)
