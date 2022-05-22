# Hotel Recommendation

## Install requirements

Untuk menjalankan fungsionalitas dari script di sini, maka cukup jalanan perintah berikut

```
pip install -r requirements.txt
```


## File structure

Berikut ini merupakan struktur file yang ada pada proyek ini
```
.
├── app/
│   ├── controllers/
│   │   └── data_management.py
│   ├── libraries/
│   │   ├── data.py
│   │   └── recommender.py
│   ├── models.py
│   └── register.py
├── data
├── bootstrap/
│   ├── static/
│   │   ├── assets
│   │   ├── css
│   │   ├── js
│   │   └── vendor
│   ├── templates
│   ├── app.py
│   └── extensions.py
├── run.py
├── config.py
├── requirements.txt
├── Procfile
├── .env
├── .gitignore
└── README.md
```

Terdapat sejumlah folder utama yang mana terletak di root path sebagaimana ditunjukkan pada bagan di atas. Folder tersebut antara lain
1. app: digunakan untuk komputasi dan management routing (controller) dari proyek
2. data: digunakan untuk menyimpan data-data yang diperlukan
3. bootrstrap: diguankan untuk management tampilan sekaligus menjadi penghubung dengan controller (yg ditunjukkan pada file app.py dan extensions.py)

Pada folder app terdapat beberapa subfolder dan file di antaranya adalah
1. controllers: management routing di proyek
2. libraries: management fungsi komputasi yang ada di proyek
3. models.py: file yang digunakan untuk mengatur skema database
4. register.py: file yang digunakan untuk memastikan routing yang dibuat di controllers terhubung dengan main aplikasi

Selain itu pada root path juga terdapat beberapa file penting, di antaranya
1. run.py: base script untuk menjalankan proyek
2. config.py: configurasi umum dan management env variabel yg digunakan di proyek
4. Procfile: konfigurasi untuk menjalankan aplikasi di heroku
5. .gitignore: daftar file yang di-hide atau diikutsertakan dalam pengelolaan git
6. .env: digunakan untuk mendefinisikan variabel global


## Setup .env

Untuk menjalankan program ini pastikan menambahkan/mengkonfigurasi file `.env` yang berisi:
- USER=<username>
- PASSWORD=<pasword>
- DATABASE=<database>
- SECRET_KEY=<secret key>
- WTF_CSRF_SECRET_KEY=<csrf secret key>

Program ini menggunakan database `mongodb` dan .env file di atas digunakan untuk menjalankan database tersebut.

Selanjutya script rekomendasi ada di app -> libraries -> recommender.py .

Apabila tidak mau terlalu ribet maka pada `.env` cukup ditambahkan 
- HOST=<urlmongo>

kemudian pada config.py tinggal dirubah jadi

```{python}
import os 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    HOST = str(os.environ.get('HOST'))
    MONGODB_SETTINGS = { 'host': HOST }
    SECRET_KEY = str(os.environ.get('SECRET_KEY'))
    WTF_CSRF_SECRET_KEY = str(os.environ.get('WTF_CSRF_SECRET_KEY'))

```

## Clone ke repo baru

1. Update remote url -> git remote set-url origin <repo url or ssh>
2. Jalankan -> git status
3. Apabila ada yang belum ter-commit maka jalankan -> `git add .` . Selanjutnya `git commit -m <pesannya apa>`.
4. Jalankan -> git pull origin <nama repo>
5. Jalankan -> git push origin <nama repo>

## Heroku Deployment
1. heroku login
2. jalankan -> `git checkout master`, apabila belum ada branch master maka buat terlebih dahulu dengan menjalankan -> `git checkout -b master`
2. jalankan -> `git push heroku master`
