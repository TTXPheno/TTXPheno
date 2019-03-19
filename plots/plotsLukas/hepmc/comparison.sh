python comparison.py $@ --version v2 --pdf 0d1  --sample tt --selection lepSel1-njet4p-nbjet1p &
python comparison.py $@ --version v2 --pdf 1d0  --sample tt --selection lepSel1-njet4p-nbjet1p &
python comparison.py $@ --version v2 --pdf 10d0 --sample tt --selection lepSel1-njet4p-nbjet1p &

python comparison.py $@ --version v2 --pdf 0d1  --sample tt --selection lepSel2-offZ-njet2p-nbjet1p &
python comparison.py $@ --version v2 --pdf 1d0  --sample tt --selection lepSel2-offZ-njet2p-nbjet1p &
python comparison.py $@ --version v2 --pdf 10d0 --sample tt --selection lepSel2-offZ-njet2p-nbjet1p &

python comparison.py $@ --version v2 --pdf 0d1  --sample ttZ --selection lepSel3-onZ-njet3p-nbjet1p-Zpt0 &
python comparison.py $@ --version v2 --pdf 1d0  --sample ttZ --selection lepSel3-onZ-njet3p-nbjet1p-Zpt0 &
python comparison.py $@ --version v2 --pdf 10d0 --sample ttZ --selection lepSel3-onZ-njet3p-nbjet1p-Zpt0 &
