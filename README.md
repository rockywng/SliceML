# SliceML
SliceML is a web-based NLP tool used for performing rapid sentiment analysis on YouTube comments to derive greater insight on video performance. The site can be accessed at sliceml.ca and currently averages 70+ unique monthly users, ranging from individuals to businesses. SliceML is still actively being worked on with new features scheduled to be released soon!

# Usage
Navigate to the site (sliceml.ca). Then, copy paste the link to a YouTube video from the navigation bar in your browser (including the https beginning).

![Screenshot 2022-03-29 163738](https://user-images.githubusercontent.com/55059833/160702657-4ac7922e-95bc-4dc5-b916-be199cd541da.png)

The given video will then be scraped to retrieve its comments. The comments will then be used as input to the NLP model. A positivity percentage will then be displayed based on the output of the model.

![Screenshot 2022-03-29 163738](https://user-images.githubusercontent.com/55059833/160703295-68940722-b104-4b39-9b9c-bb547edef187.png)

Invalid inputs will return an appropriate error message.

# Model Training
Specific aspects of the training process such as the training data and training script are excluded from this repository in the interest of maintaining confidentiality. The training process involved scraping over 500 000 YouTube comments from a variety of videos, with an approximately 35-30-35 split between positive, neutral and negative comments. Comments were then cleaned, tokenized and lemmatized in preparation for training. The NLP model was then trained on this data and exported as a .sav file for production use.

# Screenshots
![Screenshot 2022-03-29 163738](https://user-images.githubusercontent.com/55059833/160704116-669bdbb9-d4dc-4e3a-978e-a3fb08a87c93.png)
