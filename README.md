***Information:
This is my Capstone for Practicum 2022 Spring class. This app allows users to register to the site, send email to verify registration, allow login to be able to see secure user details and also allow to upload data. Currently, users are able upload datasets (up to 1800MB in size) to the site, and it gets stored in MongoDB. Then, users are able to edit the uploaded dataset by changing row, columns names, deleting rows or columns and saving this dataset locally to their machine. Then, it generates 
visualizations regarding the dataset displaying info about the dataset, variable distributions, interaction diagrams, correlation scores, missing values and sample data.
Users can download the visualizations to their local machine. 



***Application Structure: 
Built in Flask and Dash.
Uses Flask_User and Flask_Login libraries to manage users
Uses PyMongo to manage databases

***How to run:
  1. Create a new python environment
  2. pip install -r requirements.txt
  3. Inside the main directory, run '''flask run'''
  4. Go to http://127.0.0.1:5000



Some quick commands:
```
pip freeze > requirements.txt
```
