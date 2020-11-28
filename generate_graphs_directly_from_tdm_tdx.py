import seaborn as sns
from labie.generate import generate_mz_graphs

sns.set_theme()


if __name__ == '__main__':
    base_dir = '/home/kasper/Dropbox/George Maria/PTRMS 24-26NOV2020/'
    # base_dir = './'
    file_name_tdm = '26nov2020.tdm'
    file_name_tdx = '26nov2020.tdx'
    file_summary_name = '26nov2020_Summary.txt'
    mz_label = 'm/z 95.00 ch29'

    generate_mz_graphs(base_dir, file_name_tdm, file_name_tdx, file_summary_name, mz_label)
