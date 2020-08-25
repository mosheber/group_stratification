# group_stratification
Stratify data rows by group, to ensure that the probability distribution per group per split will be as similar as possible. 

Can be used to split medical images, with patients as groups. 
Thus, the splitter splits the data into 2 sets, in which there is no overlap of patients between
the sets, and the patients in each set have similar distributions (similar amounts of images).

Similarity between probability distribution of splits, is determined by the Jensen-Shannon distance.


#Usage:
```python
# df:
# --- image_id --- group_id ----
# --- 0 --- patient_0 ----
# --- 1 --- patient_1 ----
# --- 2 --- patient_0 ----
# --- 3 --- patient_1 ----

from group_stratification.splitter import SplitOptimizer

splitOptimizer = SplitOptimizer(group_id='group_id')

a_data_df_joined, b_data_df_joined, results_df = splitOptimizer.find_optimal_split(df,test_size=0.2,max_iter=200)

# 100%|██████████| 200/200 [00:01<00:00, 164.03it/s]
# best splits are: [5, 10, 1, 6, 7, 3, 15, 0, 13, 16, 18, 8, 14, 2, 9, 12, 17, 11],[4, 19]

```
