Idea: generate entire statespace (maybe try for 2D first?)
If you have range [-1,1] for each value then you can take say 5 points in that range.
(or maybe do 3 points: -1, 0, 1 or -0.5, 0, 0.5)
for a single affine transformation with 12 values: 5^12 = 244mm possible transformations.
An IFS with degree (# affine transforms) 4 will have 

Want to avoid:
IFS that are not contractive on average
Affine transforms with too little variance (good objects have a lot of 0s)

Once we have sampled an adequete number of IFS, iterate each one and classify using PointNet.
If there is high confidence, we know that the object resembles something IRL.


Idea: train a simple supervised FC network to go from word (embedding, e.g. word2vec) to IFS
Even though the dataset will not encompass every word, hopefully it learns a function to convert from word embedding space to IFS space which can interpolate nicely to unseen words.

Dataset:
Each word is labeled with and IFS.
We get each sample by the following:
    1. generate random IFS
    2. iterate the random IFS to get a point cloud fractal
    3. run PointNet++ on the fractal cloud to get a classification

Training:
    Input: word2vec embedding
    Output: IFS
    Loss: distance between predicted and label IFS
Prediction:
    Word -> word2vec -> FC model -> IFS -> fractal point cloud

Potential issue: will have multiple different IFS labels for the same word.
Hopefully it learns to generate the average IFS of these labels.