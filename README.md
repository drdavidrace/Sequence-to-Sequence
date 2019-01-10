
# Sequence-to-Sequence

This is the base repository to transcribing audio of mathematics in video to something that is close to a more correct transcription that available through the standard Speech-to-Text mechanisms.  The fundamental challenge with the products like Google/MS/IBM Voice-to-Text is that the training doesn't really understand when the text is a technical discussion.  This means that the *"common"* transcription heavily outweighs the intended transcription.

An additional challenge for training anything for this type of transcription lies with the limited amount of data.  For instance, I have several (orders of 10) classes of Cal 1, Cal 2, Cal 3, and Pre-Cal; however, this is not enough to do full full training.

# Methodology Discussion

This problem will be attacked via transfer learning.  Ideally, we will get a transcription from Google, and use a pre-trained word embedding to train a translation using RNNs for the classes that I have existing transcriptions.  This might be a long shot, but we will move toward this goal.

This work will be done using PyTorch as a baseline.  *I don't have access to a GPU right now, so I will just use my local cpu for the processing.  This is sub-optimal, but we will see where this goes.*

# Word Embeddings

These are the several pre-trained word embeddings, including:

1. GloVe - Jeffrey Pennington, Richard Socher, and Christopher D. Manning. 2014. [GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/pubs/glove.pdf).

2. Other

I will start with the smallest mapping and work upwards until enough of the words from the existing transcriptions are found.
