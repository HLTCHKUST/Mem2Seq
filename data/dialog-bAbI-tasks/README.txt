Dialog bAbI tasks data
-----------------------------------------------------------------------
In this directory is the set of 6 tasks for testing end-to-end dialog systems in the restaurant domain as described in the paper "Learning End-to-End Goal-Oriented Dialog" by Bordes & Weston (http://arxiv.org/abs/1605.07683). The aim is that each task tests a unique aspect of dialog. Tasks are designed to complement the set of 20 bAbI tasks for story understanding already released with the paper "Towards AI Complete Question Answering: A Set of Prerequisite Toy Tasks" by Weston et al. (http://arxiv.org/abs/1502.05698).


** Data **
For each task, there are 1000 dialogs for training, 1000 for development and 1000 for testing. For tasks 1-5, we also include a second test set (with suffix -OOV.txt) that contains dialogs including entities not present in training and development sets.

The file format for each task is as follows:
ID user_utterance [tab] bot_utterances
...
The IDs for a given  dialog start at 1 and increase. When the IDs in a file reset back to 1 you can consider the following sentences as a new dialog. When the bot speaks two times in a row, we used the special token "<SILENCE>" to fill in for the missing user utterance.

For example (for task 1):
1 hi	hello what can i help you with today
2 can you make a restaurant reservation with italian cuisine for six people in a cheap price range	i'm on it
3 <SILENCE>	where should it be
4 rome please	ok let me look into some options for you
5 <SILENCE>	api_call italian rome six cheap

The goal of the tasks is to predict the bot utterances, that can be sentences or API calls (sentences starting with the special token "api_call").

Along with the train, dev and test sets, we also include a knowledge base file (dialog-babi-kb-all.txt) that contain all entities appearing in dialogs for tasks 1-5. We also include a file containing the candidates to select the answer from (dialog-babi-candidates.txt) for tasks 1-5, that is simply made of all the bot utterances in train, dev, test for these tasks.

Task 6 is a bit different since its data comes from the Dialog State Tracking Challenge 2 (http://camdial.org/~mh521/dstc/), which we modified to convert it into the same format as the other tasks. There is no OOV test set associated with this task and the knowledge base (dialog-babi-task6-dstc2-kb.txt) is imperfect. This task has its own candidates file (dialog-babi-task6-dstc2-candidates.txt).


** License **
This dataset is released under Creative Commons Attribution 3.0 Unported license. A copy of this license is included with the data.


** Contact **
For more details on the dataset and baselines, see the paper "Learning End-to-End Goal-Oriented Dialog" by Antoine Bordes and Jason Weston (http://arxiv.org/abs/1605.07683). For any information, contact Antoine Bordes : abordes (at) fb (dot) com .

