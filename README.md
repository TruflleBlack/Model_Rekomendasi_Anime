# Model Rekomendasi Anime
## Project Overview
Di situasi pandemi COVID-19 ini membuat peminat anime justru meningkat dikarenakan anjuran pemerintah untuk work from home membuat masyarakat seringkali dilanda kebosanan. Banyak dari mereka yang mengisi waktu luang mereka di rumah dengan bermain smartphone, memasak, rebahan, ataupun menonton film yang mereka suka seperti menonton anime. Bagi mereka yang menonton anime bisa dibilang sebagai penghibur yang tidak pernah membosankan di saat kegiatan dalam rumah. Dilansir dari Kompas, pengguna baru Netflix bertambah 15,8 juta selama pandemic COVID-19. Netflix sendiri adalah layanan streaming dengan menyediakan banyak film dan serial, termasuk anime juga. Beberapa studio animasi Jepang juga sudah ada yang bekerjasama dengan Netflix seperti NAZ-Anime & Company Studio, Science SARU, dan MAPPA. Oleh karena itu, masyarakat tidak perlu lagi datang ke bioskop untuk melihat film anime. Masyarakat menjadi lebih mudah untuk mengakses anime di mana saja dan kapan saja.[[1](https://www.jef.or.jp/journal/pdf/234th_Special_Article_01.pdf)]

Sistem rekomendasi telah menjadi populer dalam beberapa tahun terakhir untuk mengatasi masalah kelebihan informasi dengan menyarankan produk yang paling relevan kepada pengguna dari sejumlah besar data. Penonton saat ini cenderung mengakses secara *online*, yang jelas menimbulakn masalah pertumbuhan data yang terlalu cepat di internet yang menyebabkan terlalu banyak informasi. Hal ini dapat mempersulit seseorang untuk mendapatkan informasi judul anime dengan cepat saat mereka membutuhkannya. Untuk itu, diperlukan sistem rekomendasi yang membantu seseorang menemukan informasi tentang judul anime yang bagus untuk ditonton di waktu senggang.
## Business Understanding
Berdasarkan latar belakang diatas, berikut ini rumusan masalah yang dapat diselesaikan pada proyek ini:
### Problem Statements
Bagaimana membangun sistem rekomendasi anime yang menggunakan metode content-based filtering dan memudahkan pengguna untuk mendapatkan rekomendasi?
### Goals
Untuk mempermudah penonton dalam menemukan judul anime yang direkomendasikan berdasarkan rating.
### Solution Statement
Membuat model sistem rekomendasi untuk memberikan beberapa rekomendasi anime dengan menggunakan pendekatan content based filtering.
- Content Based Filtering
Sistem rekomendasi berbasis konten (content-based filtering) adalah merekomendasikan item yang mirip dengan item yang disukai pengguna di masa lalu. Content-based filtering mempelajari profil minat pengguna baru berdasarkan data dari objek yang telah dinilai pengguna. Algoritma ini bekerja dengan menyarankan item serupa yang pernah disukai di masa lalu atau sedang dilihat di masa kini kepada pengguna. Semakin banyak informasi yang diberikan pengguna, semakin baik akurasi sistem rekomendasi. [[2](https://www.dicoding.com/academies/319/tutorials/17116)]

## Data Understanding
### Exploratory Data Analysis
Dataset yang digunakan penulis bersumber dari platform penyedia dataset yaitu Kaggle. Dataset yang digunakan berfokus tentang Rekomendasi anime ditahun 2020. Dataset ini berisi informasi tentang 16.621 anime, 175.731 rekomendasi dan preferensi dari 74.129 pengguna. Berikut dataset penulis gunakan :
**Jenis**|**Keterangan**|
:-----:|:-----:
Sumber| [Kaggle dataset : Anime-Planet Recommendation Database](https://www.kaggle.com/datasets/hernan4444/animeplanet-recommendation-database-2020?select=anime.csv)|
Lisensi | CC0: Public Domain
Jenis dan Ukuran Berkas | CSV(113 MB)
Jumlah Dataset csv | 5 dataset csv

Berikut 5 dataset yang terdapat di dalam dataset Anime-Planet Recommendation
1. ```animelist.csv``` memiliki daftar semua anime yang didaftarkan oleh pengguna dengan skor masing-masing, status menonton, dan jumlah episode yang ditonton. Dataset ini berisi 20 Juta baris, 16.745 anime berbeda dan 74.129 pengguna berbeda. File memiliki kolom berikut:
- user_id: id pengguna yang dibuat secara acak yang tidak dapat diidentifikasi.
- anime_id: ID anime-planet dari anime. (misalnya 1).
- skor: skor antara 1 sampai 5 yang diberikan oleh pengguna dalam skala 0,5. 0 jika pengguna tidak menetapkan skor. (misalnya 3.5)
- watching_status: ID negara dari anime ini di daftar anime pengguna ini. (misalnya 2)
- watch_episodes: jumlah episode yang ditonton oleh pengguna. (misalnya 24)

2. ```watching_status.csv``` menjelaskan setiap kemungkinan status kolom: "watching_status" di ```animelist.csv```

3. ```rating_complete.csv``` adalah himpunan bagian dari animelist.csv. Dataset ini hanya mempertimbangkan anime yang telah ditonton sepenuhnya oleh pengguna (watching_status==1) dan memberinya skor ( score!=0). Dataset ini berisi 8 Juta peringkat yang diterapkan ke 15.681 anime oleh 68.199 pengguna. File ini memiliki kolom berikut:
- user_id: id pengguna yang dibuat secara acak yang tidak dapat diidentifikasi.
- anime_id: ID anime-planet dari anime. (misalnya 1).
- rating: rating yang telah ditetapkan pengguna ini.

4. ```anime_recommendations.csv``` memiliki daftar semua anime yang direkomendasikan diberikan satu anime. 
- Anime: ID Planet Anime dari anime. (misalnya 1).
- Recommendation: Anime Planet ID dari anime yang direkomendasikan. (misalnya 1).
- Agree Votes: jumlah pengguna yang setuju dengan rekomendasi.

5. ```anime.csv``` berisi informasi umum setiap anime (16.621 anime berbeda) seperti Tag, jenis, studio, sinopsis, dll. File ini memiliki kolom berikut:
Anime-PlanetID: ID Planet Anime dari anime. (misalnya 1).
Nama: nama lengkap anime. (misalnya FLCL)
Nama Alternatif: cara lain untuk memanggil anime. (misalnya Furi Kuri)
Rating Score: skor rata-rata anime yang diberikan dari semua pengguna di database Anime Planet. (mis. 8.78)
Number Votes: jumlah pengguna yang memberikan skor pada anime. (misalnya 1241)
Tag: daftar tag yang dipisahkan koma untuk anime ini. (misalnya Komedi, Mecha, Sci Fi, Luar Angkasa, Karya Asli)
Peringatan Konten: daftar tag peringatan konten yang dipisahkan koma. (misalnya Kekerasan Eksplisit, Tema Dewasa, Ketelanjangan)
Jenis: TV, film, OVA, dll. (misalnya TV).
Episode: jumlah bab. (misalnya 26)
Selesai: Benar jika anime selesai ketika saya melakukan pengikisan data. Salah adalah anime yang sedang berlangsung pada saat itu.
Durasi: durasi anime dalam menit (mis. 60)
StartYear: tahun ketika anime memulai transmisi. (misalnya 2016)
EndYear: tahun ketika anime menyelesaikan transmisi. (misalnya 2017)
Musim: musim dan tahun rilis (mis. Musim Gugur 2000)
Studios: daftar studio yang dipisahkan koma (misalnya Sunrise)
Sinopsis: sinopsis anime
Url : url menuju halaman utama anime di Anime Planet 

Dari 5 datase diatas, penulis menggunakan variabel anime dan ratin yangg akan digunakan pada model rekomendasi ini.
- Melakukan analisis dataset, penulis melakukan perubahan nama header 'Anime-PlanetID' menjadi 'anime_id' pada variabel anime.csv, 
- Melakukan overview dataframe dari 5 dataset. Overview datafraem bertujuan melihat mean,median,min,max dan lain lain untuk tipe data yang numerik.
- Melakukan visualisasi dataset rating dan anime, berikut penjelasan tentang visualisasi 2 variabel tersebut :
**Visualisasi variabel dataset Rating**
![Gambar 1](https://i.postimg.cc/MHh3H7n4/newplot.png)
Pada visualisasi rating diatas bisa dilihat bahwa rating anime paling tinggi berada di rating 5 sejumlah 22.6% dan paling rendah di sekitaran rating 0.5 yang berjumah 1%.
**Visualisasi variabel dataset Anime**
![Gambar 2](https://i.postimg.cc/05TbPztJ/newplot-1.png)
Pada visualisasi variabel anime diatas menghitung distribusi anime pertahunnya, dan distribusi paling tinggi berada di tahun 2017.

## Data Preparation
### Data Preprocessing

Sebelum melakukan data processing, disini penulis melakukan data preprocessimg terlebih dahulu. Diantaranya seperti berikut :
- Menggabungkan seluruh data pada kategori anime_id yang terdiri dari beberapa variabel yaitu variabel anime, anime list, anime recomen dan rating
- Menggabungkan seluruh data pada kategori user yang terdiri dari variabel anime list dan rating
- Mengetahui jumlah rating
- Menggabungkan Data dengan Fitur Nama Anime dengan menggunakan perintah ```groupby```
- Menggabungkan Data dengan dataframe anime dengan menggunakan perintah ```pd.merge```

### Data Preparation

Untuk persiapan data, penulis menggunakan beberapa teknik yang diperlukan dalam tahap persiapan data. Sebagai berikut:
- Mengatasi missing value dengan menyeleksi data apakah data tersebut ada yang kosong atau tidak dengan menggunakan ```.isnull().sum()```. Dan melakukan ```Dropna``` untuk membuang seluruh row yang memiliki NaN values.
- ```drop_duplicates``` Drop dulicates digunakan dalam proses data preparation untuk membuang data - data yang terduplikasi.
- ```.tolist()``` untuk menkonversi data menjadi list
- Membuat dictionary untuk membuat dictionary dari data yang ada.
- Menggunakan TfidfVectorizer untuk melakukan pembobotan.

## Modeling 
Setelah melakukan processing dataset, langkah selanjutnya adalah memodelkan data. Model yang akan digunakan proyek kali ini yaitu menggunakan pendekatan content based filtering menggunakan TfidfVectorizer.
### Content Based Filtering
Dalam pembuatannya, content based filtering menggunakan konsep perhitungan vectoru, TF-IDF, dan Cosine Similarity yang intinya dikonversikan dari data/teks menjadi berbentuk vector.

**TF-IDF** adalah singkatan dari Term Frequency-Inverse Document Frequency memiliki fungsi untuk mengukur pentingnya sebuah kata relatif terhadap kata lain dalam sebuah dokumen. Umumnya dalam perhitungan ini menghitung skor untuk setiap kata untuk menunjukkan pentingnya dalam dokumen dan corpus. Metode ini umumnya digunakan dalam pencarian informasi dan text mining. 
Ditahap ini kita akan membangun sistem rekomendasi sederhana berdasarkan genre anime 

**Cosine Similarity** setelah kita telah berhasil mengidentifikasi korelasi antara judul anime dengan genrenya. Sekarang, kita akan menghitung derajat kesamaan (similarity degree) antar Judul anime dengan teknik cosine similarity. Di sini, kita menggunakan fungsi cosine_similarity.

2 metode diatas memiliki kelebihan dan kekurangan. 
- Kelebihan
Tidak memerlukan data apapun terhadap pengguna
Dapat merekomendasikan item khusus
- Kekurangan
Membutuhkan banyak pengetahuan suatu domain
Membuat rekomendasi berdasarkan minat pengguna yang ada saja

**Recommendation Result**
Untuk mendapatkan rekomendasi, kita menggunakan judul anime yang berjudul "Naruto " dengan genre "Action, Drama, Shounen, Japanese Mythology,...". Jika sistem rekomendasi berjalan dengan baik, maka kita akan mendapatkan hasil judul anime dengan genre yang sama yaitu "Action, Drama, Shounen, Japanese Mythology,...". Hasil rekomendasi di bawah sudah diurutkan dari rating terbesar.
|                  anime_title                 |                       genre                       |  type | episode | ratings |
|:--------------------------------------------:|:-------------------------------------------------:|:-----:|:-------:|:-------:|
|         Naruto: Narutimate Hero 3 OVA        |      Action, Shounen, Ninja, Based on a Manga     |  OVA  |    1    |   5.0   |
|  Naruto Shippuden OVA: Sage Naruto vs Sasuke | Action, Shounen, Ninja, Rivalries, Shorts, Bas... |  OVA  |    1    |   4.0   |
| Naruto Movie 2: Legend of the Stone of Gelel |      Action, Shounen, Ninja, Based on a Manga     | Movie |    1    |   3.0   |
|              The Dagger of Kamui             |         Action, Adventure, Ninja, Revenge         | Movie |    1    |   2.5   |
|  Naruto Shippuden Movie 3: The Will of Fire  |      Action, Shounen, Ninja, Based on a Manga     | Movie |    1    |   1.5   |

Dari hasil di atas dapat dilihat bahwa anime yang bergenre antar Action, Drama, Shounen, Japanese Mythology,... menjadi yang direkomendasikan oleh sistem. Hal ini didasarkan pada kesukaan penonton atau pengguna pada masa lalu.

## Evaluation
Untuk mengevaluasi sistem rekomendasi menggunakan pendekatan pemfilteran berbasis konten, kita dapat menggunakan salah satu metrik, yaitu precision@K. Precision dalah perbandingan antara jumlah true positive (TP) dan jumlah data yang diprediksi positif. Atau Anda dapat menulisnya secara matematis seperti ini :

- precision = TP / (TP + FP)

Keterangan
TP = True Positive atau positif yang sebenarnya 
FP = False Positive atau positif yang salah dari hasil prediksi

Namun, sistem rekomendasi menggunakan True positive atau False Positive melainkan rating yang diberikan pada judul anime untuk menentukan genre yang direkomendasikan relevan atau tidak. Dengan rumus sebagai berikut :

precision@K = (# of recommended item that relevan) / (# of recommended item)

Relevan : Rating > 2.5 Tidak relevan : Rating < 2.5

Angka 2,5 bersifat arbitrer dan nilai-nilai di atas dianggap cocok. Ada banyak cara untuk memilih nilai ini, tetapi untuk proyek ini penulis menggunakan 2.5 sebagai ambang batas. Dengan kata lain, judul anime dengan peringkat di atas 2.5 dianggap relevan, dan judul anime di bawahnya dianggap tidak relevan.

Pertama, pilih nilai K 5.0 (sesuai dengan rekomendasi keseluruhan).
Kemudian tentukan ambang relevansi 2,5. Selanjutnya, filter semua judul anime yang direkomendasikan berdasarkan ambang batas. Terakhir, hitung presisi@K menggunakan rumus di atas. Hasil rekomendasi yang dihasilkan menghasilkan akurasi sebagai berikut::

precision@10 = 2.5 / 5 precision@10 = 60%

Karena ada 5 anime dengan peringkat di atas ambang batas dan di bawah ambang batas 4, penulis mendapatkan akurasi 60% dari model sistem rekomendasi penulis menggunakan pendekatan Content Based Filtering.
