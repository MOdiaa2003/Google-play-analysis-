# Google-play-analysis

# Introduction:
int is project we will use python(pandas,matplotlib,seaborn,missingno[visualizing missing values],numpy) to cleaning,analyzing,answering questions about data contains in info about 
apps in google store ,this contains 10.8k of rows which describes following attributes (App	Category	Rating	Reviews	Size	Installs	Type	Price	Content Rating	Genres	Last Updated	Current Ver	Android Ver)
We start by cleaning our data. Tasks during this section include:
Drop NaN values from rating column
Change the type of columns (to_numeric,astype)
droping duplicated rows
Once we have cleaned up our data a bit, we move the data exploration section. 
# Questions :
1- Which app has the most reviews?

2- What category has the highest number of apps uploaded to the store?

3-To which category belongs the most expensive app?

4- What's the name of the most expensive game?

5-Which is the most popular Finance App?

6-What Teen Game has the most reviews?

7- How many Tb (tebibytes) were transferred (overall) for the most popular Lifestyle app?

# tools i used:
1. Python:
   - Primary programming language for data analysis.

2. Pandas:
   - Enables efficient loading, cleaning, and transformation of datasets.

3. Matplotlib:
   - Essential for creating insightful visualizations to interpret and communicate data.

4. Jupyter Notebook:
   - Interactive computing environment for data analysis and visualization.
   - Provides an intuitive interface for conducting exploratory data analysis and documenting workflows.

5. Git & GitHub:
   - Version control system for tracking changes in project files.
     
# techniqes used:
To answer these questions we walk through many different pandas & matplotlib methods. They include:
1-Adding column
2-format category column
3-Parsing cells as strings to make new columns (.str)
4-Using the .apply() and lambda methods
5-Using groupby to perform aggregate analysis
6-Plotting bar charts and lines graphs to visualize our results

# conclusions

1. A notable gap in the number of reviews exists between Facebook, Instagram, and the other top 8 social media apps.
2. Hypothesis: The number of installs might explain this gap, suggesting a correlation between installs and reviews.
3. The correlation coefficient of 0.83 indicates a strong positive linear relationship between installs and reviews.
4. As installs increase, reviews tend to increase, and vice versa, supporting the hypothesis.
5. The prevalence of family apps doubles that of the second-highest category, "Game".
6. The "Family" category encompasses diverse subcategories like Educational Apps, Entertainment, and Health.
7. App Store policies and competition may influence developers' decisions to prioritize the "Family" category.
8. The "Finance" and "Lifestyle" categories host the top 10 most expensive apps due to their niche appeal.
9. Finance apps cater to wealth management, investments, and financial success, justifying higher prices.
10. Lifestyle apps target personal interests and preferences, often pricing for exclusivity and personal branding.
