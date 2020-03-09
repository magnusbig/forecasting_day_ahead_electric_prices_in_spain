


class EDA:
    '''
    Class created to perform EDA
    '''
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    def __init__(self, df):
        self.df = None

    def missing_values(self, df):
        '''
        Formula to return column names with missing values and number of missing values

        Credit: Noelle Brown
        '''
        missing_val = df.isnull().sum()
        if missing_val.any():
            print(f'Total missing values: {missing_val.sum()}')
            mv = missing_val.reset_index()
            mv.columns = ['Variable Name', 'Number of Missing Values']
            return mv[mv['Number of Missing Values'] > 0]
        else:
            print('No Missing Values')

    def check_outliers(self, df, cols, z_score):
        '''
        Function to check list of numerical columns and return a dictionary
        with the number of outliers above and below a certain std from the
        mean of that column
        '''
        outliers = {}
        for col in cols:
            z = df[col].std() * z_score
            min_bound = df[col].mean() - z
            max_bound = df[col].mean() + z
            min_outliers = df[df[col] < min_bound][col].count()
            max_outliers = df[df[col] > max_bound][col].count()
            outliers[col] = {'upper outliers': max_outliers,
                             'lower outliers': min_outliers}
        return outliers

    def pythonic_columns(self, df):
        '''
        Function to create pythonic column names with underscores instead of
        spaces and all undercase

        Code adapted from
        https://stackoverflow.com/questions/41476150/removing-space-from-dataframe-columns-in-pandas/41476181
        '''
        # Ensure no whitespace on either end
        df.columns = df.columns.str.strip()
        # Replace spaces with _
        df.columns = df.columns.str.replace(' ', '_')
        # Undercase
        df.columns = df.columns.str.lower()

    def corr_hm(self, df, cols, width = 10, height = 8):
        '''
        Function to create a correlation heatmap with a mask for the upper,
        right half

        takes in a DataFrame and Columns desire, can set width and height
        '''
        # mask from
        # https://seaborn.pydata.org/examples/many_pairwise_correlations.html
        # Generate a mask for the upper triangle
        plt.figure(figsize=(width,height))
        mask = np.zeros_like(df[cols].corr(), dtype=np.bool)
        mask[np.triu_indices_from(mask)] = True

        sns.heatmap(df[cols].corr(), annot=True, cmap='coolwarm',
                    mask = mask, vmin=-1, vmax=1);

    def subplot_boxplots(self, df, y_, cols, width = 20,height = 15, titles = None, xlabels = None):
        '''
        Function to create multiple boxplots of 
        Thanks Jakob for helping me make this work
        https://stackoverflow.com/questions/20174468/how-to-create-subplots-of-pictures-made-with-the-hist-function-in-matplotlib-p

        '''
        nrows = int(np.ceil(len(cols)/2)) # Makes sure you have enough rows
        fig, ax = plt.subplots(nrows=nrows, ncols=2, figsize=(width,height))
        ax = ax.ravel() # Ravel turns a matrix into a vector, which is easier to iterate
        for idx, ax in enumerate(ax): # Gives us an index value to get into all our lists
            sns.boxplot(x=cols[idx], y=y_, data=df, ax=ax)
# In[ ]:
