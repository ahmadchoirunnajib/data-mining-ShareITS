--DESKTOP-VGNG6LG

use MiningShareITS

--Jumlah Matakuliah di setiap Jurusan
SELECT Jurusan, count(distinct Matakuliah) as Jumlah from MatakuliahdanNamaDosen group by Jurusan order by Jumlah

--Jumlah Jurusan dan Matakuliah Yang Belum Pernah di Akses oleh Dosen
select a.Jurusan, count(a.Matakuliah) as Jumlah from  
	(SELECT Fakultas, Matakuliah, Jurusan from MatakuliahdanNamaDosen
	EXCEPT
	SELECT Fakultas, Matakuliah, Jurusan from MatakuliahITSNamaDosenAksesMKTerakhir) a group by a.Jurusan order by Jumlah desc

--Jumlah Jurusan dan Matakuliah Yang Sudah Pernah di Akses oleh Dosen
select a.Jurusan, count(a.Matakuliah) as Jumlah from  
	(SELECT Fakultas, Matakuliah, Jurusan from MatakuliahdanNamaDosen
	INTERSECT
	SELECT Fakultas, Matakuliah, Jurusan from MatakuliahITSNamaDosenAksesMKTerakhir) a group by a.Jurusan order by Jumlah desc

--Jumlah Jurusan dan Matakuliah Yang Sudah Pernah di Akses oleh Mahasiswa
select a.Jurusan, count(a.Matakuliah) as Jumlah from  
	(SELECT Fakultas, Matakuliah, Jurusan from MatakuliahdanNamaDosen
	INTERSECT
	SELECT Fakultas, Matakuliah, Jurusan from MatakuliahITSNamaDosenAksesMKTerakhir) a group by a.Jurusan order by Jumlah desc

--Jumlah Jurusan dan Matakuliah Yang Belum Pernah di Akses oleh Mahasiswa
select a.Jurusan, count(a.Matakuliah) as Jumlah  from  (SELECT Fakultas, Matakuliah, Jurusan from MatakuliahdanNamaDosen
EXCEPT
SELECT Fakultas, Matakuliah, Jurusan from MatakuliahITSNamaMahasiswaAksesMKTerakhir) a group by a.Jurusan order by Jumlah desc


--Jumlah Jurusan dan Matkul Yang Diambil Mahasiswa Akan Tetapi Belum Pernah di Akses oleh Mahasiswa
select a.Jurusan, count(a.Matakuliah) as Jumlah  from  (SELECT Fakultas, Matakuliah, Jurusan from MatakuliahITSNamaMahasiswa
EXCEPT
SELECT Fakultas, Matakuliah, Jurusan from MatakuliahITSNamaMahasiswaAksesMKTerakhir) a group by a.Jurusan order by Jumlah desc
