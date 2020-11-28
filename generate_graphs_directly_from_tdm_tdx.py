import os
import re
from datetime import datetime

import json
import numpy as np
import pandas as pd
import seaborn as sns
import tdm_loader
import xmltodict
from matplotlib import pyplot as plt

sns.set_theme()

base_dir = '/home/kasper/Dropbox/George Maria/PTRMS 24-26NOV2020/'
file_name = '24nov2020.tdm'
mz_label = 'm/z 95.00 ch29'
file_summary_name = '24nov2020_Summary.txt'

with open(base_dir + file_name) as xml_file:
    data_dict = xmltodict.parse(xml_file.read())

with open(base_dir + "{0}.json".format(file_name), "w") as json_file:
    json.dump(data_dict, json_file)

data_file = tdm_loader.OpenFile(base_dir + file_name)

# for channel in range(1,data_file.no_channel_groups()+1):


m_z_data = data_file.channel_dict(2)[mz_label]

number_of_data_points = m_z_data.shape[0]

summary = open(base_dir + file_summary_name, "r")

times = [t for t in summary.readlines() if 'Start Time' in t or 'Stop Time' in t]

start_time_m = times[0]
stop_time_m = times[1]

start_time_m1 = re.sub('[^A-Za-z0-9]+', ' ', start_time_m).split(' ')[-7:-1]
stop_time_m1 = re.sub('[^A-Za-z0-9]+', ' ', stop_time_m).split(' ')[-7:-1]

start_datetime_string = ' '.join(start_time_m1)
stop_datetime_string = ' '.join(stop_time_m1)

start_datetime_datetime = datetime.strptime(start_datetime_string, '%B %d %Y %H %M %S')
stop_datetime_datetime = datetime.strptime(stop_datetime_string, '%B %d %Y %H %M %S')

with open(base_dir + "{0}.json".format(file_name), "r") as json_file:
    data = json.load(json_file)

tdm_channel_list = data['usi:tdm']['usi:data']['tdm_channel']

relative_time_dict = [td for td in tdm_channel_list if td['name'] == 'Relative Time'][0]

absolute_time_dict = [td for td in tdm_channel_list if td['name'] == 'Absolute Time'][0]

relative_time_minimum = float(relative_time_dict['minimum'])
relative_time_maximum = float(relative_time_dict['maximum'])

time_step = round((stop_datetime_datetime - start_datetime_datetime).seconds / number_of_data_points, 3)

time_steps = np.linspace(relative_time_minimum, relative_time_maximum, num=number_of_data_points).round(3)

index = pd.Index(time_steps, name='Relative Time')

data_mz = pd.DataFrame(m_z_data, index=index, columns=[mz_label])

for column in data_mz.columns:
    print(column)
    data_mz[column].plot()
    plt.ylabel(column)
    plt.xticks(rotation=70)
    plt.tight_layout()
    os.makedirs(base_dir + '{0}'.format(file_name.split('.')[0]), exist_ok=True)
    plt.savefig(base_dir + '{0}/{1}.svg'.format(file_name.split('.')[0], column.replace('/', '_')), format='svg',
                dpi=1200)
    plt.close()
