# ntt2ntt
A pipeline for clustering spikes in Neuralynx ntt files using python, MClust and KlustaKwick!


# List of Files:

* kkRunner.sh, a bash script for running KlustaKwik on all TTs in parallel.
* nttWriter.py, to write cluster files(.clu) to ntt Neuralynx files.
* scriptWriter.py, to write an matlab script which will be used by pipe.sh to run MClust and get feature files(.fet.n)...
* pipe.sh, to do everything @ once!
