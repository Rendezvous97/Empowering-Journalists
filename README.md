# Empowering-Journalists

To use the tool, you will need to do the following:

1. Download the repository

2. Install all the required libraries using:

pip install requirments.txt

3. You will need to get an APIkey from google cloud to use the Vision and Language APIs. The code requires the file location for the JSON API key.

4. Add the image file path and title text to the code in journalisttool.py

5. run journalisttool.py using:

python journalisttool.py

------------------------------------------------------------------------------------------------------------------
The Journalists' Tool to Establish Image-Text Relavence 
------------------------------------------------------------------------------------------------------------------
1. Problem
------------------------------------------------------------------------------------------------------------------
Given India’s low literacy rate, images play a vital role in the spread of information. Images also have the ability to capture people’s attention quicker than text1. This characteristic of a picture, unfortunately, can also be used to disseminate misinformation on a wide scale. The danger of fake information propagated through images is especially evident in India, wherein it has resulted in unwanted consequences, including death.

Viral social media posts and message forwards usually consist of an image and an associated title. Although the image might depict one a particular phenomenon or event, the text could purposefully be chosen to incite the viewer. For example, an image of two people having a physical altercation in which one person is wearing a skull cap can easily be misunderstood if the associated text were “Riots broken out at Faridabad - Muslims versus Hindus once again”. Although this was a hypothetical example, it is not impossible for us to envision a similar method of fake news propagation that could end up having fatal consequences.

------------------------------------------------------------------------------------------------------------------
2. Our Solution
------------------------------------------------------------------------------------------------------------------

We believe that curbing this subset of fake news would involve providing the necessary tools to journalists and users who take the time to sift through trustworthy content. In this light, our solution is to devise a methodology and program to assist a journalist to identify if an image and associated title are trustworthy. The fundamentals of our approach are based on corroboration of news, i.e, the image must be used in credible news websites with text similar to that of the associated title for the image and text to be reliable. If not, we recommend that the journalist (or user) perform a human verification procedure.

------------------------------------------------------------------------------------------------------------------
3. Methodology
------------------------------------------------------------------------------------------------------------------
3.1. Step 1: Where else has the image been used?
------------------------------------------------------------------------------------------------------------------

● In our case, the user encodes the image path and associated text in the code. An extension can be made wherein these two elements are derived from social media applications and websites such as Facebook and Twitter.

● The user image is then run through Google’s Vision API that performs a reverse image search that outputs page URLs of websites that have used the same picture as the user image.

❖ Elements obtained after Step 1:

➢ A list of page URLs in which the user image has been used.

------------------------------------------------------------------------------------------------------------------
3.2. Step 2: Are these pages credible?
------------------------------------------------------------------------------------------------------------------

● The program searches through the list of page URLs that we obtained in Step 1 to check if any of them are credible news sources.

● Credible sources are determined beforehand. The user or journalist has the ability to encode whichever source she believes is trustworthy within the program code as a list. We also provide a default credible list of news websites.

❖ Elements obtained after Step 2:

➢ A list of credible page URLs in which the user image has been used.

------------------------------------------------------------------------------------------------------------------
3.3. Step 3: How do we get the Title of these News Articles?
------------------------------------------------------------------------------------------------------------------

● The program scrapes each URL from the list obtained in Step 2 in order to extract the titles of each news article.

● The HTML request and parsing is performed using the Request and BeatifulSoup4 libraries respectively.

● Our initial motivation was to extract the caption (or alternate text) used with each image but most websites choose not to add an alternate text or make it too generic for any meaning to be derived).

❖ Elements obtained after Step 3:

➢ A list of titles of the news articles from the credible page URLs in which the
user image has been used.

------------------------------------------------------------------------------------------------------------------
3.4. Step 4: How can we compare these Titles to the Associated Title?
------------------------------------------------------------------------------------------------------------------

● In this step, the program is made to decipher the semantic similarity between the titles we have extracted and the original associated title.

● To perform this text meaning comparison, the program uses Google’s pre-trained news article text corpus which is trained on the Word2Vec algorithm. After reading the file in binary mode (which takes a few minutes), it computes the Word Mover’s Distance.

● For each credible URL, the program calculates and assigns a value which is the distance of the meaning of the title from the associated title. After averaging out all these distances, the program decides whether or not the image-text combination is reliable or requires human-verification. This is done by adding a threshold value to the average distance.

● In our code, we have added a threshold value of 1 after a significant number of trials. This means that any average word mover’s distance greater than 1 will be flagged and the user will be prompted to perform human verification for that image-text combination.

❖ Elements obtained after Step 4:

➢ Word Mover’s (WM) distances between each scraped title and the associated title.

➢ Average (WM) distances of the titles.

------------------------------------------------------------------------------------------------------------------
3.5. Step 5: If Human Verification is Needed, How do we Help?
------------------------------------------------------------------------------------------------------------------

● In order to be as helpful as possible to a journalist, our program provides the user a plethora of information to aid in manual verification. This information includes content analysis from the input image and entity analysis from the associated text. These elements of information are derived using Google’s Natural Language Processing API and Vision API. Content analysis provides a content category prediction that the image might be whereas the entity analysis predicts the subject of the text. Entity analysis also provides a ‘salience’ value which reflects the relevance of the object to the whole title.

❖ Elements obtained after Step 5:

➢ Content analysis of the user image 

➢ The best guess of the user image 

➢ Entity analysis of the scraped titles

------------------------------------------------------------------------------------------------------------------
4. Implementation Issues and Limitations
------------------------------------------------------------------------------------------------------------------

❖ The alternate text/caption for the image is either missing in which case nothing can be used or is too generic. If the caption is too generic then comparing it to the associated text may not give us a conclusive answer. We overcame this by taking the title of the article instead.

❖ Reading the Word2Vec trained text corpus was taking more than 5 minutes since it consists of 3.5 GB worth of data. In order to save time, we limited the amount of data read to only 500,000 data points. As a result, the program now takes only one minute to read the Google corpus as a binary file. With more time, the accuracy of the algorithm and hence, the precision of the distance is bound to increase.

❖ The URLs obtained after running through the reverse image search may not match with any of the credible ones. In this case, the program doesn’t continue and prompts human verification. One way to avoid this could be to increase the set of credible URLs thereby increasing the chances of getting a match.

❖ In certain cases, the image used may be too generic or irrelevant in comparison to the title of the article in which case the reverse image search may not give URLs with similar titles. This could lead to false results as the distance value could cross the threshold but the article may not be fake at all.

------------------------------------------------------------------------------------------------------------------
5. Future Scope and Conclusion
------------------------------------------------------------------------------------------------------------------

It is evident that there is a need for a tool that empowers journalists and news consumers so that they can sift through trustworthy content and not be misinformed. By using the current tools which have been made available on the cloud (Google Vision and NLP API) we attempt to solve the current problem of fake news propagation. Through this report, we have showcased the relevance of such a tool which is both effective and empowers the user to be aware of trustworthy articles with respect to their understanding of reliability. Future scope for this project could be to create a mobile application and toolbar application that draws over other applications in order to derive the user image and associated title. Additionally, the program could sift through the entire article content to see which part pertains to the image to make the decision more accurate.
