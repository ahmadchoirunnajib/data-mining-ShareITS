import pandas as pd
import dateparser as dp
import pyodbc
from string import digits
files = ['1SemuaCourse.csv', '2MatakuliahPublik.csv', '3Chat.csv', '4MatakuliahITS.csv',
         '5MatakuliahdanNamaDosen.csv', '6MatakuliahITSNamaMahasiswa.csv',
         '7MatakuliahITSNamaDosenAksesMKTerakhir.csv', '8MatakuliahITSJumlahMahasiswa.csv',
         '9MatakuliahHidden.csv', '10MatakuliahITSNamaMahasiswaAksesMKTerakhir.csv',
         '11Useryanglogindalamsetahunterakhir.csv', '12Useryangpernahlogin.csv']

tables = ['SemuaCourse', 'MatakuliahPublik', 'Chat', 'MatakuliahITS',
          'MatakuliahdanNamaDosen', 'MatakuliahITSNamaMahasiswa',
          'MatakuliahITSNamaDosenAksesMKTerakhir', 'MatakuliahITSJumlahMahasiswa',
          'MatakuliahHidden', 'MatakuliahITSNamaMahasiswaAksesMKTerakhir',
          'Useryanglogindalamsetahunterakhir', 'Useryangpernahlogin']


def cleaning_csv(string):
    df = pd.read_csv("dataset/" + string, sep="|", error_bad_lines=False, encoding='cp1252')
    df = df.set_index('No')
    if 'Lastaccess' in df.columns:
        df['lastaccessdatetime'] = df.apply(lambda row: dp.parse(row.Lastaccess), axis=1)
    df.to_csv('convert/convert_' + string, sep="|")


def create_table(string):
    df = pd.read_csv("convert/convert_" + string, sep="|", error_bad_lines=False, encoding='cp1252')
    list_column = list(df.columns.values)
    print(type(list_column))
    query_datatype = ''
    for column in list_column:
        if 'No' == column.replace("|", ""):
            q = 'No int'
        elif 'lastaccessdatetime' == column.replace("|", ""):
            q = 'lastaccessdatetime datetime'
        else:
            q = str(column).replace(" ", "").replace("|", "") + " varchar(255)"
        query_datatype = query_datatype + str(q) + ", "
    remove_digits = str.maketrans('', '', digits)
    table_name = string.translate(remove_digits)
    table_name = table_name[:-4]
    query = "CREATE TABLE " + table_name + " (" + query_datatype[:-2] + ")"
    bulkinsertquery = "BULK INSERT " + table_name + " FROM \'G:\Google Drive\S2\Semester 1\Manajemen Data dan Informasi\FP\ProjectPython\convert\convert_" + string + "\' WITH ( FIRSTROW = 2, FIELDTERMINATOR = \'|\', ROWTERMINATOR = \'\\n\', MAXERRORS = 100000 )"
    print("executing query = " + query)
    print("executing query = " + bulkinsertquery)
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 13 for SQL Server};SERVER=DESKTOP-VGNG6LG;DATABASE=MiningShareITS;Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    cursor.execute("use MiningShareITS;")
    cursor.execute(query)
    cursor.execute(bulkinsertquery)
    cnxn.commit()
    cnxn.close()


def datasummaries(string):
    df = pd.read_csv("convert/convert_" + string, sep="|", error_bad_lines=False, encoding='cp1252')
    print(df.describe())

#for item in files:
    #cleaning_csv(item)
    #create_table(item)