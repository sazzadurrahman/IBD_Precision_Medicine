# IBD_Precision_Medicine
Prototype for IBD Precision Medicine
______________________________________________________________________________________________________________________________

The objective of the project is to build a prototype data aggregation interface that will allow users to easily interact with the combined datasets (clinical data, human tissue experimental data and genomics data) and to produce reports demonstrating data associations through visualizations. In order to obtain this aim, the following tasks are performed:

a.	Extract clinical, experimental and genomics data
b.	Analyse and visualize the data
c.	Create interface for visualization process
d.	Identify the best drug response and find matching single-nucleotide polymorphism (SNP) among patients
e.	Find the genes based on matching SNPs


# Instructions to setup and run the app

First, make sure your computer has Anaconda Distribution or Python 3.5 installed.

# Install the following packages
pip install plotly

pip install dash

pip install scikit-allel

pip install biopython


# For Anaconda Distribution, install the packages as follows:
conda install plotly

conda install -c conda-forge dash

conda install -c conda-forge scikit-allel

conda install -c anaconda biopython

_________________________________________________________________________________________________
The master file is main.py

It will open the dashboard at http://127.0.0.1:2019, where 2019 is the specified port number.
