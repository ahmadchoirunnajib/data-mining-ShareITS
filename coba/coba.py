import pandas as pd
import dateparser as dp

files = ['1SemuaCourse.csv', '2MatakuliahPublik.csv', '3Chat.csv', '4MatakuliahITS.csv',
         '5MatakuliahdanNamaDosen.csv', '6MatakuliahITSNamaMahasiswa.csv',
         '7MatakuliahITSNamaDosenAksesMKTerakhir.csv', '8MatakuliahITSJumlahMahasiswa.csv',
         '9MatakuliahHidden.csv', '10MatakuliahITSNamaMahasiswaAksesMKTerakhir.csv',
         '11Useryanglogindalamsetahunterakhir.csv', '12Useryangpernahlogin.csv']


def cleaning_csv(string):
    df = pd.read_csv("dataset/" + string, sep="|", error_bad_lines=False, encoding='cp1252')
    df = df.set_index('No')
    if 'Lastaccess' in df.columns:
        df['lastaccessdatetime'] = df.apply(lambda row: dp.parse(row.Lastaccess), axis=1)
    df.to_csv('convert/convert_' + string)


def create_table(string):
    df = pd.read_csv("convert/convert_" + string, sep="|", error_bad_lines=False, encoding='cp1252')
    df = df.set_index('No')


for item in files:
    cleaning_csv(item)
