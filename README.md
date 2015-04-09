# ntt2ntt
A pipeline for clustering spikes in Neuralynx ntt files using python, MClust and KlustaKwick!

Usage:
```bash
      ./pipe /path/to/data/
```
# List of Files:

* kkRunner.sh, a bash script for running KlustaKwik on all TTs in parallel.
* nttWriter.py, to write cluster files(.clu) to ntt Neuralynx files.
* scriptWriter.py, to write an matlab script which will be used by pipe.sh to run MClust and get feature files(.fet.n)...
* pipe.sh, to do everything @ once!

#Notes:

* Keep in mind that you need to make files executable before being able to run them ( chmod +x foo.sh) and probably correct the path to your python for .py files.
* You can also run different scripts sepaprately. For example, one can do :
```bash
        $ ./nttWriter.py /path/to/data
```
in order to write cluster information (.clu) to .ntt files.
