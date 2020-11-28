import json
import re
from datetime import datetime

import numpy as np
import xmltodict


def get_time_step_from_summary_file(summary_file_path, number_of_data_points):
    summary = open(summary_file_path, "r")
    times = [t for t in summary.readlines() if 'Start Time' in t or 'Stop Time' in t]
    start_time_m = times[0]
    stop_time_m = times[1]
    start_time_m1 = re.sub('[^A-Za-z0-9]+', ' ', start_time_m).split(' ')[-7:-1]
    stop_time_m1 = re.sub('[^A-Za-z0-9]+', ' ', stop_time_m).split(' ')[-7:-1]
    start_datetime_string = ' '.join(start_time_m1)
    stop_datetime_string = ' '.join(stop_time_m1)
    start_datetime_datetime = datetime.strptime(start_datetime_string, '%B %d %Y %H %M %S')
    stop_datetime_datetime = datetime.strptime(stop_datetime_string, '%B %d %Y %H %M %S')
    time_step_from_file_summary = round(
        (stop_datetime_datetime - start_datetime_datetime).seconds / number_of_data_points, 3)
    return time_step_from_file_summary


def generate_time_steps_from_tdm_file(base_dir, file_name, number_of_data_points):
    with open(base_dir + file_name) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    with open(base_dir + "{0}.json".format(file_name), "w") as json_file:
        json.dump(data_dict, json_file)
    with open(base_dir + "{0}.json".format(file_name), "r") as json_file:
        data = json.load(json_file)
    tdm_channel_list = data['usi:tdm']['usi:data']['tdm_channel']
    relative_time_dict = [td for td in tdm_channel_list if td['name'] == 'Relative Time'][0]
    absolute_time_dict = [td for td in tdm_channel_list if td['name'] == 'Absolute Time'][0]
    relative_time_minimum = float(relative_time_dict['minimum'])
    relative_time_maximum = float(relative_time_dict['maximum'])
    time_steps = np.linspace(relative_time_minimum, relative_time_maximum, num=number_of_data_points).round(3)
    return time_steps


