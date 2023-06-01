# Predicting Video Ratings for Users

This repository contains code and notebooks for predicting video ratings for users using different algorithms and libraries. The implemented algorithms and their performances are discussed in detail in the following sections.

## 5.2.1. Preprocessing Data (prepare.ipynb)

The `prepare.ipynb` notebook focuses on the preprocessing steps performed on the Tournesol dataset to prepare it for analysis. The following steps are carried out:

1. Data filtering: Users with less than 60 video ratings are filtered out to focus on users with sufficient data for analysis.
2. Rating scale transformation: The original rating scale, ranging from -100 to 100, is transformed into a new scale ranging from 0 to 10. This transformation enables consistency and ease of interpretation.
3. Saving preprocessed data: The preprocessed dataset is saved as a CSV file named "data_parameter.csv", where "parameter" represents the value used for filtering the users based on the number of ratings.
4. data_60.csv contains the data for users with at least 60 ratings, being the best parameter for the current dataset.

The preprocessing steps ensure that the dataset is refined and ready for further analysis and model implementation.

## 5.2.2. Implicit Recommendation using ALS

The `als.ipynb` notebook explores the application of the Alternating Least Squares (ALS) algorithm for predicting video ratings based on user-item interactions. The following steps are performed:

1. ALS algorithm implementation: The ALS algorithm is used to compute user and item vectors that capture the similarity between users, their preferences, and the similarity between items and their interactions. The algorithm solves a set of equations during each iteration to update the user and item vectors and optimize their accuracy.
2. Generating personalized recommendations: A function called `recommend` is developed to generate personalized video recommendations for individual users. This function takes a user ID, trained user and item vectors, and other relevant data as input. It calculates recommendation scores by taking the dot product of user vectors with item vectors and scales the scores between 0 and 1 using the MinMaxScaler. The top recommended videos are selected based on the highest scores.
3. Limitations: It is important to note that ALS adaptation for explicit ratings may have limitations. While ALS is suitable for proposing new videos to users, it may not be the most efficient approach for accurately predicting the scores users would assign to specific videos.

## 5.2.3. ALS with Implicit Library

The `implicit_als.ipynb` notebook provides a code snippet for implementing the ALS algorithm using the Implicit library. The steps involved in this process are as follows:

1. Data preprocessing: The data is filtered and transformed, including selecting a specific criterion, converting user and video names to numerical IDs, and filtering users to keep those with a minimum of 10 interactions. Ratings are kept within the range of -100 to 100.
2. Splitting data: The preprocessed data is split into training and test sets.
3. Model training: Sparse matrices are created to represent item-user and user-item interactions for training the ALS model. The model is initialized with specific parameters, such as the number of factors, regularization, and the number of iterations. The confidence of the item-user matrix is calculated by applying an alpha value to emphasize higher-rated interactions. The model is trained using the ALS algorithm, which alternates between updating user and item vectors to minimize the reconstruction error.
4. Model evaluation: Metrics such as precision, recall, mean average precision, mean absolute error (MAE), and root mean squared error (RMSE) are computed to evaluate the model's performance on the test set.

The notebook provides insights into the model's performance and suggests areas for improvement.

## 5.2.4. SVD++ with Surprise Library (Tournesol_ratings.ipynb)

In the `surprise_svdpp.ipynb` notebook, the necessary preprocessing steps are performed, and the recommendation model is trained using the Surprise library. The steps involved in this process are as follows:

1. Data preprocessing: Ratings are normalized on a scale of 0 to 10 to ensure consistency and easier interpretation.
2. Model training: The SVD++ algorithm is used to train the recommendation model. The trained model is saved for future use.
3. Model evaluation: The Root Mean Squared Error (RMSE) and Mean Absolute Error (MAE) scores are calculated to assess the model's predictions against the actual ratings. A confusion matrix is created to visualize the distribution of predicted ratings compared to the actual ratings.
4. Personalized recommendations: The trained model is used to generate personalized recommendations for a specific user.

The results and analysis provide insights into the model's performance and suggestions for improvement.