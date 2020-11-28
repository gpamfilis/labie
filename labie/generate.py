import os

import pandas as pd
import tdm_loader
from matplotlib import pyplot as plt

from labie.utils import generate_time_steps_from_tdm_file, get_time_step_from_summary_file


def generate_mz_graphs(base_dir, file_name_tdm, file_name_tdx, file_summary_name, mz_label, output_dir=None):
    if output_dir is None:
        output_dir = base_dir

    flags = []
    for fi in [file_name_tdm, file_name_tdx, file_summary_name]:
        if os.path.exists(os.path.join(base_dir, fi)):
            flags.append(True)
        else:
            flags.append(False)
    if all([f for f in flags if f is True]):
        print('All Files Are There')
        data_file = tdm_loader.OpenFile(base_dir + file_name_tdm)

        for channel_group in range(1, data_file.no_channel_groups() + 1):
            # channel_group = 2
            if mz_label is None:
                labels = list(data_file.channel_dict(channel_group).keys())
                for label in labels:
                    print(label)
                    if 'm/z' not in label:
                        continue
                    generate_single_mz_graph(data_file=data_file, channel_group=channel_group, base_dir=base_dir,
                                             output_dir=output_dir, file_name_tdm=file_name_tdm,
                                             file_summary_name=file_summary_name, mz_label=label)
            else:
                if 'm/z' in mz_label:
                    generate_single_mz_graph(data_file=data_file, channel_group=channel_group, base_dir=base_dir,
                                             file_summary_name=file_summary_name, mz_label=mz_label)
                else:
                    print('m/z not in label !!!')
        return True
    else:
        # todo check flags and say what is missing.
        print('Missing one of three files')
        return False


def generate_single_mz_graph(data_file, channel_group, mz_label, base_dir, output_dir, file_name_tdm,
                             file_summary_name):
    m_z_data = data_file.channel_dict(channel_group)[mz_label]
    os.makedirs(
        output_dir + 'labie_results/{0}/channel_group_{1}'.format(file_name_tdm.split('.')[0],
                                                                  channel_group),
        exist_ok=True)

    number_of_data_points = m_z_data.shape[0]

    time_step_from_summary_file = get_time_step_from_summary_file(base_dir + file_summary_name,
                                                                  number_of_data_points)

    time_steps = generate_time_steps_from_tdm_file(base_dir, file_name_tdm, number_of_data_points)

    index = pd.Index(time_steps, name='Relative Time')
    data_mz = pd.DataFrame(m_z_data, index=index, columns=[mz_label])

    for column in data_mz.columns:
        # print(column)
        data_mz[column].plot()
        plt.ylabel(column)
        plt.xticks(rotation=70)
        plt.tight_layout()
        plt.savefig(
            output_dir + 'labie_results/{0}/channel_group_{1}/{2}.svg'.format(file_name_tdm.split('.')[0],
                                                                              channel_group,
                                                                              column.replace('/', '_')),
            format='svg',
            dpi=1200)
        plt.close()


if __name__ == '__main__':
    pass
