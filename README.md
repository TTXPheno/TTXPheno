# TTXPheno
## Get code for TTXPheno studies

```
cmsrel CMSSW_9_4_3
cd CMSSW_9_4_3/src
cmsenv
git cms-init
git clone https://github.com/TTXPheno/TTXPheno
# looping & plotting - needed for the examples
git clone https://github.com/TTXPheno/RootTools
scram b -j40
```

## Delphes
```
export PYTHIA8=/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/pythia8/223-mlhled2/
export LD_LIBRARY_PATH=$PYTHIA8/lib:$LD_LIBRARY_PATH
cd $CMSSW_BASE/..
git clone https://github.com/TTXPheno/delphes.git
patch $CMSSW_BASE/../delphes/cards/delphes_card_CMS.tcl < $CMSSW_BASE/src/TTXPheno/patches/slim_delphes.diff # Reduce Delphes output
cd delphes
./configure
sed -i -e 's/c++0x/c++1y/g' Makefile
make -j 4 
```

## Prerequisites
Add your user-specific locations to [user.py](https://github.com/TTXPheno/TTXPheno/blob/master/Tools/python/user.py).
You can do that also later and thus fix potential 'ImportError' from `user.py`  when they occur. 

## How to make a flat ntuple from a GEN file
Define the sample in e.g. [fwlite_benchmarks.py](https://github.com/TTXPheno/TTXPheno/blob/master/samples/python/fwlite_benchmarks.py) and do 
```
voms-proxy-init -voms cms -out ~/private/.proxy
cd TTXPheno/postprocessing
python genPostProcessing.py --overwrite --sample fwlite_ttZ_ll_LO_highStat_scan --addReweights --small
```
Remove `--small` to process the full sample. Add `--nJobs=10` and `--job=0` etc. options to run only on the first 10% of events. In Vienna you could also do 
```
export X509_USER_PROXY=~/private/.proxy
submitBatch.py --dpm genPostProcessing.sh # append `#SPLIT200` to a line
``` 
For other places we can add submission scripts.

## Examples
Polynomial parametrization:
```
python Tools/python/HyperPoly.py
```

## Using the Plot Scripts  
General plots for gen-level and reco-level distributions can be made using the plot-script in
```
plots/plotsLukas/gen_reco/skim_plots.py
``` 
Choose the following arguments for general settings  
``` 
--sample        (specify signal sample from TTXPheno/sample/python/benchmarks.py)  
--detector      (choose the detector, e.g. CMS, ATLAS or phase2_CMS. Make sure the samples are there and have the naming \<samplename\>_\<detector\>)  
--small         (use small sample for testing)  
--version       (specify output directory)  
--processFile   (specify the parameter file imported from addons/\<processFile\>.py)  
--level         (use 'gen' or 'reco', be carful you chose the right variables in read_variables in addons/\<processFile\>.py)  
--selection     (specify selection string, see TTXPheno/Tools/python/cutinterpreter\<level\>.py for more details)  
--backgrounds   (add backgrounds to the distributions, backgrounds are specified in the 'bg' list in the script)  
--noninfoSignal (add non-informative signal to the distributions, non-info signal is specified in the 'noninfo' list in the script)  
--luminosity    (define the luminosity to which the distribution is scaled to (e.g. 150))  
--leptonFlavor  (very specific to the choices of processFile, basically adds new selections on the lepton flavor, choose 'all' for no additional selection)  
``` 
Choose the following arguments for BSM settings  
``` 
--parameters    (add values for SM-EFT parameters in the form \<param\> \<value\>, e.g. cpt 3 cpQM 5 ctZ 5)  
--order         (specify polynomial order for BSM sample reweighting, strongly recommended: 2)  
--scaleLumi     (area-normalize the BSM models to the SM)  
``` 
Choose the following arguments for differential Fisher Information (FI) settings  
``` 
--addFisherInformation           (flag to add the ideal FI in arbitrary units to the plot, signal only)  
--addFisherInformationBackground (flag to add the real FI in arbitrary units to the plot, considering backgrounds)  
--variables                      (choose the BSM variable for which the FI is plotted, use one only!)  
--binThreshold                   (choose the minimum number of events per bin for the FI. If less, the FI is not considered for this bin! Used to set max. stat. error / bin)  
``` 

Before you start:  
Add your settings to "TTXPheno/Tools/python/user.py"  
Make sure you have your setting file in 'addons/\<processFile\>.py' and choose this file with '--processFile'  
Add the variables from the root file, the selections/calculated variables and the plots you like to this file  
If you want to add the Fisher information, add the line "fisherInfoVariables.append('\<root-variable\>')" below the definition of the plot. Use 'None' as root-variable is you do not need the FI in the plot at any time.  
Choose your selection according to the convention in 'TTXPheno/Tools/python/cutinterpreter\<level\>.py'  
Change the list 'bg' and 'noninfo' in the 'skim_plots.py' script to include the right backgrounds/non-informative signals and adapt the settings for these samples (e.g. overlap-removal)  
  
Example command for a differential FisherInfo plot for the variable 'cpt' with at least 100 events per bin on top of the distributions for the chosen SM-EFT parameters, which are area-normalized to the SM for the CMS detector, ttZ (3l) 13TeV L=150/fb, with backgrounds and non-info signal on reco-level  
``` 
python skim_plots.py --sample fwlite_ttZ_ll_LO_order2_15weights_ref --detector CMS --version v1 --processFile ttZ_3l_paper --level reco  --selection lepSel3-onZ-njet3p-nbjet1p-Zpt0-leptonIso3 --backgrounds --noninfoSignal --luminosity 150   --leptonFlavor all --parameters cpQM 5 cpt 5 ctZ 5 ctZI 5 --scaleLumi --addFisherInformation --addFisherInformationBackground --binThreshold 100 --variables cpt  
``` 
