# Introduction

Poker Vision is a deep learning network and application that allows users to evaluate a Texas Hold'em hand. It consists of an object recognition model to identify playing cards and an evaluation algorithm to score hands. The application also tells the user the best hand they can make with their current cards. We use the [YOLO](https://arxiv.org/abs/1506.02640) (You Only Look Once) V3 architecture for playing card classification, and we augmented the [Chen formula](https://www.thepokerbank.com/strategy/basic/starting-hand-selection/chen-formula/) for scoring hands.

The full paper for our project can be viewed [here](https://drive.google.com/file/d/1ht_av-7p3Rovhn_TwHZn6xNgFsd26FsC/view?usp=sharing).

# Training

The model was trained using [Darknet](https://github.com/AlexeyAB/darknet) for 72 hours and 9,000 iterations on NVIDIA Tesla K80. 

ALthough Darknet was used to train the model, the parameters were transferred to a python implementation of the model which is used in the application for evaluation. 

# Running the application
To evaulate a hand, run **score_hand.py**. This script takes one or two arguments, each of which is a path to an image file relative to the project root. These two images represent your personal hand and the community cards and will be evaluated as a single hand. 

You can also run the card detector without evaluating it as a hand. To do this, run **detect.py**. Add the optional **--help** flag for for arguments.

