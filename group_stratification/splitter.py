from sklearn.model_selection import train_test_split
from tqdm import tqdm
from scipy.spatial import distance
import numpy as np
import pandas as pd

class SplitOptimizer:
  def __init__(self,group_id='group_id'):
    """
    Example usage:

    df:
    --- image_id --- group_id ----
    --- 0 --- patient_0 ----
    --- 1 --- patient_1 ----
    --- 2 --- patient_0 ----
    --- 3 --- patient_1 ----

    from group_stratification.splitter import SplitOptimizer
    splitOptimizer = SplitOptimizer(group_id='group_id')
    a_data_df_joined,b_data_df_joined,results_df = splitOptimizer.find_optimal_split(df,test_size=0.2,max_iter=200)
    # 100%|██████████| 200/200 [00:01<00:00, 164.03it/s]
    # best splits are: [5, 10, 1, 6, 7, 3, 15, 0, 13, 16, 18, 8, 14, 2, 9, 12, 17, 11],[4, 19]
    """
    self.group_id = group_id

  def to_group_df(self,groups):
    return pd.DataFrame(groups,columns=[self.group_id])

  def get_sample_vectors(self,groups,data_df):
    group_df = self.to_group_df(groups).set_index(self.group_id)
    data_df_joined = data_df.join(group_df,on=self.group_id,how='inner')
    return list(data_df_joined[self.group_id]),data_df_joined

  def get_probabily_vector(self,groups,data_df):
    sample_vector,data_df_joined = self.get_sample_vectors(groups,data_df)
    counts, _ = np.histogram(sample_vector)
    return counts,data_df_joined

  def get_probabilty_similarity(self,a,b):
    return distance.jensenshannon(a/a.max(),b/b.max())

  def find_optimal_split(self, df,test_size=0.2,max_iter=100):
    """
    Input: 
      - df: Pandas dataframe with a column group_id, which has rows per group (for example, medical images per patient).
      - test_size: Ratio on which to split
      - max_iter: Amount of rounds of optimization to find the best split, that has the most similar distributions per split. 
    Output:
      - a_data_df_joined: df, only with the first split. 
      - b_data_df_joined: df, only with the second split.
      - results_df: all the splits found, with their respective distance scores. 
    """
    groups = list(set(df[self.group_id]))
    results = []
    for i in tqdm(list(range(max_iter))):
      a,b = train_test_split(groups,test_size=test_size)  
      
      a_probabily_vector,a_data_df_joined = self.get_probabily_vector(a,df)
      b_probabily_vector,b_data_df_joined = self.get_probabily_vector(b,df)
      
      sim = self.get_probabilty_similarity(a_probabily_vector,b_probabily_vector)
      results.append({
          'a':a,
          'b':b,
          'a_probabily_vector':a_probabily_vector,
          'b_probabily_vector':b_probabily_vector,
          'a_data_df_joined':a_data_df_joined,
          'b_data_df_joined':b_data_df_joined,
          'distance':sim
      })
    results_df = pd.DataFrame(results).sort_values(by='distance')
    a_data_df_joined, b_data_df_joined = results_df.iloc[0]['a_data_df_joined'],results_df.iloc[0]['b_data_df_joined']
    a_best, b_best = results_df.iloc[0]['a'],results_df.iloc[0]['b']
    print('\nbest splits are: {},{}'.format(a_best,b_best))
    return a_data_df_joined, b_data_df_joined, results_df