# group_stratification
Stratify data rows by group, to ensure that the probability distribution per group per split will be as similar as possible. 

Can be used to split medical images, with patients as groups. 
Thus, the splitter splits the data into 2 sets, in which there is no overlap of patients between
the sets, and the patients in each set have similar distributions (similar amounts of images).

Similarity between probability distribution of splits, is determined by the Jensen-Shannon distance.
