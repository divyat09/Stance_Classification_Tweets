
**Divyat Mahajan**  
**3rd Year Undergraduate Student**  
**Department of** **Mathematics and Statistics**  
**Indian Institute of Technology Kanpur**  
**Email: [divyatmahajan@gmail.com](divyatmahajan@gmail.com) Homepage: [Click here](http://home.iitk.ac.in/~divyatm)**

<!--more-->
<hr>

# Stance Classification of Tweets in Online Debates

### Mentors:

  * Professor [Vincent Ng](http://www.hlt.utdallas.edu/~vince/), Department of Computer Science,   UTD
  * Professor [Purushottam Kar](http://www.cse.iitk.ac.in/users/purushot/), Department of Computer Science, IIT Kanpur
  * Professor [Piyush Rai](http://www.cse.iitk.ac.in/users/piyush/), Department of  Computer Science, IIT Kanpur

### Project Description:  

##### Introduction   

My research project dealt around a task in International Workshop on Semantic Evaluation 2016: [Detecting Stance in Tweets]( http://alt.qcri.org/semeval2016/task6/). It involves automatic classification of  tweets into two categories as Support and Against for a given target. A tweet can directly opinion about the main target, express opinion on some other entity apart from the target given or express no opinion at all. I worked on developing an approach that improves stance prediction for the case where tweets do not express an opinion about the main target but about some other secondary targets.    

##### Approach  

The approach is based on first labeling the tweets with their secondary targets i.e. the entries about which they express an opinion. Then training a classifier to predict a particular secondary target for a tweet and hence classifying tweets on the basis of their secondary targets. Finally, training separate classifiers that predict stance toward the main target for each class of tweet based on its secondary target. It hopes to make better predictions as now we have separate classifier for every class of tweets based on secondary targets.  

##### Implementation  
I  manually annotated the Training Set tweets with their secondary targets namely Baby Rights, Women Rights, Adoption, Christianity, and Others. Then, I made a list of special words from all unique words in tweets which have PMI >0.70 with at least one of the secondary targets. After that, I used the list of special words made above to make feature vectors using the bag of words approach. Finally, I used Support Vector Machine with linear kernel and above feature vectors  both for predicting secondary target and stance for Test Set tweets.

##### Results
 I got results with an accuracy of 54% in case of secondary target prediction over 5 classes. In the case of stance prediction, I got results with an accuracy above 70% in 4 out of 5 classes of tweets based on secondary targets. Only in the class of tweets with secondary target Others I got results where accuracy was 37%


##### Future Work
A lot of work can be done in automating the procedure for generating and annotating tweets  with a class of secondary targets from Training Dataset. Also, we can use Distant Supervision Technique to expand the current Training Dataset. Another area for improvement is the procedure to generate feature vectors by using better approaches like N-grams,etc.




##### Project Report:

[Click here](http://home.iitk.ac.in/~divyatm/RTE_Report.pdf)

##### Results and Accuracy of SVM Classifiers:

[Click here](https://docs.google.com/document/d/1KbAxn9uipJcs8SKqeDPZ37B2pT6QDru89Sz1wncNxng/view?usp=sharing)
