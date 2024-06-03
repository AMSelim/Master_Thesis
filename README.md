
# EEG-Based Speech Imagery BCI Through A Transfer From Overt To Silent Speech
This repository holds the codebase for the implementation of my Computer Science M.Sc. Thesis at Saarland University with the [Ubiquitous Media Technology Lab](https://umtl.cs.uni-saarland.de/).

## Important Notes
- I wrote the codes implemented in this repository under the supervision of Matthias Eiletz for the technical implementation. 
- I excluded any codes and documents that were UMTL property or were not mine to share.
- The dataset is not included in this repository. For any inquiries on the dataset, please get in touch with my supervisor at UMTL, Maurice Rekrut. 

## Description 
In Human-Computer Interaction, Speech Imagery is defined as speech production in the absence of any audible sounds.  It can be used across multiple domains, for example, in the medical domain for some forms of paralysis and Amyotrophic lateral sclerosis (ALS) patients, in the industrial domain for loud settings where workers cannot communicate efficiently using overt speech, and any other domain where overt speech is not possible. One of the methods used to detect Speech Imagery is measuring brain activity using Electroencephalography (EEG) devices. However, collecting training data for detecting Speech Imagery from EEG signals is a burdensome process because the participants must sit for long periods of time repeating the same group of words silently, which is quite time-consuming, mentally exhausting, boring, and difficult to validate the correctness of the words being said. 

In order to overcome these difficulties, we used a game with a purpose (GWAP) to collect EEG data for imagined speech recognition from overt speech EEG data. We collected EEG data from 15 participants during an online processing gamified study, where they controlled a robot in a maze-like teleoperation game, with five command words being said either overtly or silently. We used the overt speech EEG data to train a machine learning classifier on a within-participant basis, which was then tested on silent speech EEG data. In addition, we evaluated the effect of the GWAP-based study by training and testing a separate machine learning algorithm on only the imagined speech EEG data. The main claim of the proposed system is that there are sufficient similarities between both forms of speech to enable a successful transfer learning outcome, while the GWAP improved the enjoyment and engagement of the EEG data collection study without negatively affecting the data quality. 

## Repository Explanation
The project is structured into three main folders
 - Thesisserver
 - ThesisClient
 - OfflineProcessing

Each part is documented within its own folder. The OfflineProcessing is independent of the other two codebases, but it uses the data collected by the client and server setup.
The data collection study for my thesis was in a client-server setup. The Thesisserver and ThesisClient depended on one another as they communicated together, over two separate PCs, during the data collection while also processing the data in a real-time manner, but it was not the main focus of the thesis, which is why we conducted offline processing afterwards.
The figure below shows the overview of the whole online processing pipeline together.
![Online Processing Overview](./documents/Online_Processing_Overview.png)

## Game Assets
 - The robot asset we used in the game was acquired from [pngkey.com](pngkey.com) with the licence **No Attribution Required for Educational and Personal Purposes**. 
 - Both the box and gear assets were acquired from [Ajay Karat | Devil's Work.shop](https://devilsworkshop.itch.io/) with the licence **Public Domain Dedication**.

## Citation
If you find this work useful to your research, please consider citing our publications.

The game and technical implementation [publication](https://dl.acm.org/doi/10.1145/3656650.3656654):
```
@inproceedings{10.1145/3656650.3656654,
author = {Mohamed Selim, Abdulrahman and Rekrut, Maurice and Barz, Michael and Sonntag, Daniel},
title = {Speech Imagery BCI Training Using Game with a Purpose},
year = {2024},
isbn = {9798400717642},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3656650.3656654},
doi = {10.1145/3656650.3656654},
abstract = {Games are used in multiple fields of brain–computer interface (BCI) research and applications to improve participants’ engagement and enjoyment during electroencephalogram (EEG) data collection. However, despite potential benefits, no current studies have reported on implemented games for Speech Imagery BCI. Imagined speech is speech produced without audible sounds or active movement of the articulatory muscles. Collecting imagined speech EEG data is a time-consuming, mentally exhausting, and cumbersome process, which requires participants to read words off a computer screen and produce them as imagined speech. To improve this process for study participants, we implemented a maze-like game where a participant navigated a virtual robot capable of performing five actions that represented our words of interest while we recorded their EEG data. The study setup was evaluated with 15 participants. Based on their feedback, the game improved their engagement and enjoyment while resulting in a 69.10\% average classification accuracy using a random forest classifier.},
booktitle = {Proceedings of the 2024 International Conference on Advanced Visual Interfaces},
articleno = {43},
numpages = {5},
keywords = {BCI, EEG, Game with a purpose (GWAP), Imagined speech, User study},
location = {<conf-loc>, <city>Arenzano, Genoa</city>, <country>Italy</country>, </conf-loc>},
series = {AVI '24}
}
```

The EEG-focused [publication](https://ieeexplore.ieee.org/abstract/document/9945447):
```
@INPROCEEDINGS{9945447,  
author={Rekrut, Maurice and Selim, Abdulrahman Mohamed and Krüger, Antonio},  
booktitle={2022 IEEE International Conference on Systems, Man, and Cybernetics (SMC)},   
title={Improving Silent Speech BCI Training Procedures Through Transfer from Overt to Silent Speech},   
year={2022},
pages={2650-2656},  
doi={10.1109/SMC53654.2022.9945447}}
```
