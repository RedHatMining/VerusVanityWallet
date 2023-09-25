# Verus Vanity Wallet Miner

### Install Requirements
    pip install -r requirements.txt
### How To Run The Code
    vanity_V2.py [-h] [-of OUTPUT_FILE] [--case_sensitive] [-t THREADS] [-f FORMAT] prefix_file
    Vanity Bitcoin address generator
    
    positional arguments:
      prefix_file           Path to the file containing prefixes
    
    options:
      -h, --help            show this help message and exit
      -of OUTPUT_FILE, --output_file OUTPUT_FILE
                            Name and extension of the file to save the results
      --case_sensitive      Case sensitive search
      -t THREADS, --threads THREADS
                            Number of threads to use
      -f FORMAT, --format FORMAT
                            The format of the vanity prefix, suffix, or substring

### How To Make The Prefix File
    1. gather names, phrases, places, etc
    2. add a R to the start of each of them
    3. for each of them you have put it on a line as an example i have added a list od DC characters in a file called DC.txt
    4. save your file and run the code

