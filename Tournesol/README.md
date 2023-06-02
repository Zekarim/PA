# Predicting Video Ratings for Users

This repository contains code and notebooks for predicting video ratings for users using different algorithms and libraries.

## 5.2.1. Preprocessing Data

The `prepare.ipynb` notebook focuses on the preprocessing steps performed on the Tournesol dataset to prepare it for analysis. The following steps are carried out:

1. Data loading: The dataset is loaded from the "individual_criteria_scores.csv" file.
2. Data filtering: The dataset is filtered to keep only the rows with the "largely_recommended" criteria.
3. Column selection: Only the "public_username" (renamed as "user_id"), "video" (renamed as "item_id"), and "score" columns are kept.
4. Filtering users: Users with less than a specified number of ratings are filtered out. In this case, the parameter used is 0.
5. Rating scale transformation: The original rating scale, ranging from -100 to 100, is transformed into a new scale ranging from 0 to 10. This transformation enables consistency and ease of interpretation.
6. Saving preprocessed data: The preprocessed dataset is saved as a CSV file named "data_parameter.csv", where "parameter" represents the value used for filtering the users based on the number of ratings.

The preprocessing steps ensure that the datasets are refined and ready for further analysis and model implementation.

## 5.2.2. ALS Recommendation

The `als.ipynb` notebook demonstrates the implementation of the Alternating Least Squares (ALS) algorithm for implicit feedback data. The following steps are performed:

1. Preprocessing Data: The code loads the video rating data from a CSV file (`data_10.csv`) and performs necessary preprocessing steps, including dropping missing values, converting categorical names into numerical IDs, and creating a lookup frame for video ID to video name mapping.
2. ALS Implementation: The code defines the `implicit_als` function, which takes a sparse user-by-item matrix as input and iteratively computes user and item vectors using the ALS formulas. The function returns user vectors (`X`) and item vectors (`Y`).
3. Model Training: The `implicit_als` function is called with the sparse matrix `data_sparse` as input to train the ALS model. The model is trained by iterating over specified parameters, such as the confidence rate (`alpha_val`), the number of iterations, the regularization value (`lambda_val`), and the number of latent features.
4. User Recommendations: The code defines the `recommend` function, which generates personalized video recommendations for a given user based on the trained ALS model. The function takes the user ID, user and item vectors, item lookup frame, and the desired number of recommendations as input. It calculates recommendation scores by taking the dot-product of user vectors with item vectors and returns a DataFrame with recommended video names and scores.
5. Generating Recommendations: The `recommend` function is called to generate video recommendations for a user with ID 2 (`user_id`). The recommendations are then printed.
The implementation of the ALS algorithm for implicit feedback data allows the generation of personalized video recommendations based on user-item interactions. By training the model on the provided dataset and leveraging the computed user and item vectors, it becomes possible to recommend videos that align with users' preferences.

## 5.2.3. Implicit Recommendation using ALS

The `implicit_als_test.ipynb` notebook explores the application of the Alternating Least Squares (ALS) algorithm for predicting video ratings based on user-item interactions. The following steps are performed:

1. Data loading and preprocessing: The dataset is loaded from the "data_100.csv" file. The columns are renamed, and numeric user and artist IDs are created.
2. Data splitting: The preprocessed data is split into training and test sets.
3. Model training: The ALS algorithm from the Implicit library is used to train the recommendation model. The ALS model is initialized with specific parameters, such as the number of factors (20) and regularization (0.1). The confidence of the item-user matrix is calculated by multiplying it with an alpha value (200).
4. Generating personalized recommendations: The trained model is used to generate personalized video recommendations for a specific user. The `recommend` method is used to get a list of recommended artist IDs along with their corresponding scores. The scores are rescaled to a 0-10 rating scale.
5. Evaluation: The actual ratings for the recommended videos are compared with the predicted ratings. Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) metrics are calculated to evaluate the model's performance.
6. Error visualization: A plot is generated to visualize the RMSE and MAE values for different minimum ratings. The x-axis represents the minimum rating parameter used in the data filtering step, and the y-axis represents the error values.

The notebook provides insights into the model's performance and the impact of the minimum rating parameter on the recommendation accuracy.

## 5.2.4. ALS with Implicit Library

The `implicit_als_test.ipynb` notebook provides a code snippet for implementing the ALS algorithm using the Implicit library. The following steps are performed:

1. Data loading and preprocessing: The dataset is loaded from the "data_100.csv" file. Unique usernames and videos are extracted from the dataset, and an empty matrix is created to store the scores.
2. Matrix filling: The matrix is filled with scores based on the user-item interactions in the dataset. NaN values are filled with zeros.
3. User and item mapping: Dictionaries are created to map usernames and videos to user and item IDs, respectively.
4. Matrix transformation: The score matrix is converted to a sparse CSR matrix for efficient computation.
5. Train-test split: The interaction matrix is split into training and test sets, with a fraction of user interactions moved to the test set.
6. Parameter grid search: A grid of parameters (factors, regularization, and iterations) is defined. The ALS model is initialized with each parameter combination, and the model is fit to the training set. Precision at K is calculated to evaluate the model's performance on the test set.
7. Best parameter selection: The best parameter combination is determined based on the highest precision at K value.
8. Model training: The ALS model is re-initialized with the best parameters, and it is fit to the entire interaction matrix.
9. Generating recommendations: The trained model is used to generate personalized video recommendations for a specific user.
10. Evaluation: The actual ratings for the recommended videos are compared with the predicted ratings. Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) metrics are calculated to evaluate the model's performance.
11. Error visualization: Plots are generated to visualize the RMSE and MAE values for different minimum ratings.
12. Model saving and loading: The trained model is saved to a file and can be loaded for future use.

The notebook provides insights into the model's performance, parameter tuning, and recommendation generation using the ALS algorithm from the Implicit library.

## 5.2.5. SVD++ with Surprise Library

The `surprise_svdpp.ipynb` notebook provides a code snippet for implementing the SVD++ algorithm using the Surprise library. The following steps are performed:

1. Data loading: The dataset is loaded from the "data_0.csv" file.
2. Data preprocessing: The ratings are normalized if needed and a Reader object is defined to specify the rating scale.
3. Dataset creation: The dataset is created from the loaded data and the Reader object.
4. Train-test split: The dataset is split into training and test sets.
5. Model training: The SVD++ algorithm is initialized with specific hyperparameters (e.g., number of factors, regularization, learning rate). The algorithm is trained on the training set.
6. Model evaluation: The algorithm's performance is evaluated on the test set using metrics such as RMSE (Root Mean Squared Error) and MAE (Mean Absolute Error). Cross-validation is also performed to assess the model's generalization performance.
7. Confusion matrix: A confusion matrix is created to visualize the distribution of predicted ratings compared to the actual ratings.
8. Hyperparameter tuning (optional): Grid search can be performed to find the best combination of hyperparameters based on the lowest RMSE score.
9. Model saving and loading: The trained model can be saved to a file and loaded for future use.
10. Generating recommendations: The model can be used to generate top-N recommendations for each user.
11. Conversion of predicted scores (optional): If needed, the predicted scores can be transformed to a different rating scale.

The notebook provides insights into the model's performance, hyperparameter tuning, recommendation generation, and model saving/loading using the SVD++ algorithm from the Surprise library.