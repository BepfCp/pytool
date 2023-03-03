import os
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# official example
# fmri = sns.load_dataset("fmri")
'''
subject  timepoint event    region    signal
0        s13         18  stim  parietal -0.017552
1         s5         14  stim  parietal -0.080883
2        s12         18  stim  parietal -0.081033
3        s11         18  stim  parietal -0.046134
4        s10         18  stim  parietal -0.037970
...      ...        ...   ...       ...       ...
1059      s0          8   cue   frontal  0.018165
1060     s13          7   cue   frontal -0.029130
1061     s12          7   cue   frontal -0.004939
1062     s11          7   cue   frontal -0.025367
1063      s0          0   cue  parietal -0.006899
'''
# sns.lineplot(x="timepoint", y="signal",
#              hue="region", style="event",
#              data=fmri)
# plt.show()

# 1. create empty DataFrame with columns specified
data = pd.DataFrame(columns=['method', '#labeled_review', 'val_accuracy', 'episode'])

# 2. read .npy data
out_path = 'out'
for method in os.listdir(out_path):
    split_data_dir = os.path.join(out_path, method)
    for file in os.listdir(split_data_dir):
        episode = int(file.split('.')[0])
        file_path = os.path.join(split_data_dir, file)
        all_acc = np.load(file_path)
        for i, acc in enumerate(all_acc):
            new_row = {
                'method': method,
                '#labeled_review': i+1,
                'val_accuracy': acc,
                'episode': episode
            }
            data.loc[data.shape[0]] = new_row
# 3. plot          
sns.lineplot(x='#labeled_review', y='val_accuracy',
             hue='method',
             data=data)

plt.show()