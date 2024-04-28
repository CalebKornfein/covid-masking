Welcome to our github! Here you can find the code we used to produce results for the manuscript:

> Face Masking Behaviors Examined in Vaccinated Populations Across Five Emergency Departments in the United States

**REPRODUCING RESULTS**

1. Clone the repository locally:

> `git clone https://github.com/CalebKornfein/covid-masking.git`

2. Set up a conda environment. Conda can be downloaded [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#). We use conda version 4.12.0 and Python version 3.9.12, which can be installed [here](https://www.python.org/downloads/). Once conda is successfully installed, you can clone a version of our environment by opening terminal, navigating to the base of the latency github folder, and running the command:

>`conda env create -f environment.yml python=3.9.12`

3. Download the required python packages from the requirements.txt file:

> `pip install -r requirements.txt`

4. Run clean.py, which transforms the original unclean dataset into a cleaned version for analysis, using:

> `python clean.py`

5. Run analysis.py, which calculates the count statistics found in Table 1 and Table 2 of the manuscript, as well as the Chi-square tests. The results of analysis.py are outputted into the results_v2/ folder. Run with:

> `python analysis.py`

NOTE: the input dataset is not available in the public github as it pertains to de-identified patient data. If you would like to reproduce the results, please contact caleb.kornfein@gmail.com
