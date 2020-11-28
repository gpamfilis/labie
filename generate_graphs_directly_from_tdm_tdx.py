import os

import pandas as pd
import seaborn as sns
import tdm_loader
from matplotlib import pyplot as plt
from labie.utils import get_time_step_from_summary_file, generate_time_steps_from_tdm_file

sns.set_theme()

base_dir = '/home/kasper/Dropbox/George Maria/PTRMS 24-26NOV2020/'
file_name = '24nov2020.tdm'
mz_label = 'm/z 95.00 ch29'
file_summary_name = '24nov2020_Summary.txt'

data_file = tdm_loader.OpenFile(base_dir + file_name)

for channel_group in range(1, data_file.no_channel_groups() + 1):
    # channel_group = 2
    try:
        m_z_data = data_file.channel_dict(channel_group)[mz_label]
    except Exception as e:
        print(e)
        continue
    os.makedirs(base_dir + '{0}/{1}'.format(file_name.split('.')[0], channel_group), exist_ok=True)

    number_of_data_points = m_z_data.shape[0]

    time_step_from_summary_file = get_time_step_from_summary_file(base_dir + file_summary_name, number_of_data_points)

    time_steps = generate_time_steps_from_tdm_file(base_dir, file_name, number_of_data_points)

    index = pd.Index(time_steps, name='Relative Time')
    data_mz = pd.DataFrame(m_z_data, index=index, columns=[mz_label])

    for column in data_mz.columns:
        # print(column)
        data_mz[column].plot()
        plt.ylabel(column)
        plt.xticks(rotation=70)
        plt.tight_layout()
        plt.savefig(
            base_dir + '{0}/{1}/{2}.svg'.format(file_name.split('.')[0], channel_group, column.replace('/', '_')),
            format='svg',
            dpi=1200)
        plt.close()
