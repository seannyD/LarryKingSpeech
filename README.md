# Analysing transcripts of Larry King's speech

## Data

To save space, the intermediate stages of processing are not included in this repository.  The original transcripts are in a zipped file `data/transcripts.zip`.

## Processing

The file `processing/doProcessing.sh` produces all the processing steps:

```
python findLinks.py
python findKingSpeech.py
python cleanText.py
 
# (transcribe skips files that already exist)
#rm ../data/king_phon/*.txt
python transcribe.py
```

`analysis/gatherData.R` combines the linguistic and humidity variables.

## Analysis

The main analysis is in `analysis/analyseData.pdf`.