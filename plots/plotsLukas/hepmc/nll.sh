python nll.py --version v2 --cores 1 --pdf 0d1 --sample ttZ --selection lepSel3-onZ-njet3p-nbjet1p-Zpt0  --binning 10 0 0.003 &
python nll.py --version v2 --cores 1 --pdf 0d1 --sample tt  --selection lepSel2-offZ-njet2p-nbjet1p      --binning 10 0 0.0003 &
python nll.py --version v2 --cores 1 --pdf 0d1 --sample tt  --selection lepSel1-njet4p-nbjet1p           --binning 10 0 0.000025 &

python nll.py --version v2 --cores 1 --pdf 1d0 --sample ttZ --selection lepSel3-onZ-njet3p-nbjet1p-Zpt0  --binning 10 0 0.003 &
python nll.py --version v2 --cores 1 --pdf 1d0 --sample tt  --selection lepSel2-offZ-njet2p-nbjet1p      --binning 10 0 0.0003 &
python nll.py --version v2 --cores 1 --pdf 1d0 --sample tt  --selection lepSel1-njet4p-nbjet1p           --binning 10 0 0.000035 &

python nll.py --version v2 --cores 1 --pdf 10d0 --sample ttZ --selection lepSel3-onZ-njet3p-nbjet1p-Zpt0 --binning 10 0 0.003 &
python nll.py --version v2 --cores 1 --pdf 10d0 --sample tt  --selection lepSel2-offZ-njet2p-nbjet1p     --binning 10 0 0.0003 &
python nll.py --version v2 --cores 1 --pdf 10d0 --sample tt  --selection lepSel1-njet4p-nbjet1p          --binning 10 0 0.00007 &
