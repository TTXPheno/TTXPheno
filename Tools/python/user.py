import os

if os.environ['USER'] in ['schoef', 'rschoefbeck', 'schoefbeck']:
    results_directory   = "/afs/hephy.at/data/rschoefbeck02/TopEFT/results/" #for analysis results and cache files
    tmp_directory       = "/afs/hephy.at/data/rschoefbeck02/TTXPheno_tmp/" #for on-the-fly tmp stuff
    skim_output_directory      = "/afs/hephy.at/data/rschoefbeck01/TTXPheno/skims/" # where you want the flat ntuples to go
    plot_directory      = "/afs/hephy.at/user/r/rschoefbeck/www/TTXPheno/"  # where the plots go
    cardfileLocation    = '/afs/hephy.at/data/rschoefbeck01/TTXPheno/results/cardfiles/'

if os.environ['USER'] in ['dspitzbart', 'dspitzba']:
    tmp_directory       = "/afs/hephy.at/data/dspitzbart01/Top_tmp/"
    skim_directory      = "/afs/hephy.at/data/dspitzbart01/TTXPheno/skims/"
    skim_output_directory = "/afs/hephy.at/data/dspitzbart01/TTXPheno/skims/"
    plot_directory      = "/afs/hephy.at/user/d/dspitzbart/www/TTXPheno/"

if os.environ['USER'] in ['llechner']:
    results_directory      = "/afs/hephy.at/data/llechner01/TTXPheno/results/" #for analysis results and cache files
    skim_output_directory  = "/afs/hephy.at/data/llechner02/TTXPheno/skims/"
    plot_directory         = "/afs/hephy.at/user/l/llechner/www/TTXPheno"
    combineReleaseLocation = '/afs/hephy.at/user/l/llechner/public/CMSSW_8_1_0/src'
    cardfileLocation       = '/afs/hephy.at/data/llechner01/TTXPheno/results/cardfiles/'


if os.environ['USER'] in ['grohsjea']:
    results_directory     = "/afs/cern.ch/work/g/grohsjea/samples/eft/ttx/results/"
    tmp_directory         = "/afs/cern.ch/work/g/grohsjea/debug/eft/ttx/tmp/"
    skim_output_directory = "/afs/cern.ch/work/g/grohsjea/samples/eft/ttx/skims/"
    plot_directory        = "/afs/desy.de/user/a/agrohsje/www/hidden/eft/ttx/"

if os.environ["USER"] in ["ttschida"]:
    plot_directory                      = "/afs/hephy.at/user/t/ttschida/www/HiggsWithoutHiggs/TTXPheno/"
    results_directory                   = "/afs/hephy.at/data/cms04/ttschida/TTXPheno/results/"
    tmp_directory                       = "/afs/hephy.at/data/cms04/ttschida/TTXPheno/tmp/"
    cache_directory                     = "/afs/hephy.at/data/cms04/ttschida/TTXPheno/cache/"
    gridpack_directory                  = "/afs/hephy.at/data/cms04/ttschida/TTXPheno/gridpacks/"
    postprocessing_output_directory     = "/afs/hephy.at/data/cms04/ttschida/TTXPheno/Tuples/"
    skim_output_directory               = "/afs/hephy.at/data/cms04/ttschida/TTXPheno/skims/"
