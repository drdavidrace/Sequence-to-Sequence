# Transcription Analysis

This file contains a working description of the steps working with the transcriptions.  There are several obvious errors in the transcriptions, so this will attempt to document them until we have a working product with a high probability of performing a transcription.  Generally, we will assume that the mathematics terms will be in most of the embeddings, but it is likely that the matematics equations give us some problems.  These will probably be the biggest headache.

## 10 Jan 2019 -

I am downloading the smallest GloVe file and trying out that against the vocabulary in some of the transcriptions.  The smallest file has 400K tokens and is around 171MB of data.  Not huge, but it gets large in a hurry.  As this progresses, this likely requires use of "out-of-core" capabilities.  If I were using multiple computers for this processing, then probably *dask* would be my first choice.  However since the initial study is on my local computer I will stick with bcolz.