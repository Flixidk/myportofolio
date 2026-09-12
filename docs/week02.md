# 📈 Week 2 Progress Report & AI Disclosure

## ⭐ Key Accomplishments
- Finished Tutorial 2 where I:
    - Created a Django application
    - Implemented the MVT pipeline for my web page
    - Created a dynamic "Experience" page that fetches data from a database
    - Configured the URL routing for the website
    - Made unit tests
- Finished Tugas Individu 2 where I:
    - Created a new model in the main application called Skill
    - Made a skill page for the portofolio website and integrated teh MVT pipeline to fetch dynamic data from the database to serve within the `experience.html` template
    - Configured the URL routing for the new skill page
    - Added an extra filtering feature for the skills page that takes in user inputs through filter buttons on the web page and dynamically serves filtered data using the MVT pipeline (Extra Feature for 4.0 grading)
    - Created and updated unit tests until 100% coverage for business logic files (`views.py`, `models.py`)

## ✅ Pertanyaan Reflektif: 
**Tugas Individu 2:**
1. Ketika pengguna membuka halaman portofolio baru, browser pengguna mengirim HTTP request yang akan diproses oleh file `urls.py` pada project yang akan memforward request tersebut ke `urls.py` tingkat aplikasi yang sesuai. File `urls.py` di tingkat aplikasi yang memproses HTTP request tersebut dan menghubungkan ke suatu function di `views.py` yang akan melakukan pemrosesan untuk mendapatkan halaman portofolio yang sesuai (dengan template dan data yang sesuai). Views akan memanggil `models.py` untuk mengambil data dari database, dan mengumpulkan data tersebut dalam suatu context untuk diisi kepada template file yakni HTML pages yang sudah dibuat menggunakan function render(). Isi HTML tersebut berupa data dinamis sesuai data yang diteruskan oleh views dari database sehingga tidak langsung hardcoded di dalam HTMLnya. Lalu pada akhirnya setelah semua proses tersebut terjadi Django akan mengirim HTTP response ke browser pengguna yang berisi template (HTML and CSS) yang sudah terisi.
2. Menyimpan data langsung di dalam portofilio sebaiknya disimpan dalam model dan tidak langsung di hardcode di dalam template karena maintenance atau pemeliharaan data (baik yang baru maupun yang sudah ada) dapat dilakukan dengan mudah. Daripada kita susah payah mengubah HTML filenya ketika setiap kali kita ingin mengubah atau menambahkan data, kita cukup perlu menambahkan entry baru di database melalui Django Admin dashboard sehingga template akan otomatis merender data tersebut kita website di access.
3. Perbedaan fungsi `makemigrations` dan `migrate` pada Django adalah bahwa `makemigrations` hanya menyiapkan/mencatat blueprint untuk perubahan yang akan diterapkan pada database. Blueprint ini kemudian disimpan dalam folder migrations. Di sisi lain, fungsi `migrate` akan menerapkan blueprint perubahan yang sudah disimpan tersebut ke actual databasenya (mengeksekusi perintah SQL pada database).

## 🤖 AI Disclosure
**Tools used** : Gemini  

**How it was Used / Main Guidelines:**
- Saat mengerjakan Tutorial 2, saya menggunakan Gemini untuk menjelaskan berbagai steps ketika melakukan set up untuk menerapakan MVT pipeline pada Django karena belum terlalu paham. Saya banyak menanyakan terkait command/kode yang terdapat pada tutorial dan minta Gemini untuk menjelaskan, serta menanyakan berbagai follow-up questions untuk mendalami pemahaman saya. Saya tidak terlalu banyak meminta kode dari Gemini yang saya integrasikan ke dalam codebase saya karena mainly mengikuti steps yang terdapat pada tutorial.
- Saat mengerjakan Tugas Individu 2, saya banyak menggunakan Gemini mainly pada mengimplementasikan design/layout HTML dan CSS pada page experience dan skills. Disini saya memang banyak melakukan copy paste dan mengarahkan Gemini untuk mengubah kodenya sesuai request saya, karena saya ingin mengerahkan fokus saya pada tugas individu ini terkait bagaimana saya memang mengimplementasikan MVT Django. Namun, ketika mengimplementasikan MVT, membuat model baru, saya tidak terlalu copy-paste namun banyak menanyakan follow-up questions ke Gemini terkait syntax/kode apa yang sebaiknya diketik karena saya menggunakan baseline dari Tutorial 2 sebagai contoh. Saya juga menanyakan ide ke Gemini terkait ide tambahan untuk filtering skills berdasarkan category yang akhirnya saya implementasikan dalam web saya. Walaupun saya banyak mengandalkan Gemini pada tugas ini (especially untuk implementasi CSS), saya tetap melakukan rekap dan berusaha untuk memahami seluruh kode yang telah saya implementasikan, dan saya cukup percaya diri sudah mengerti bagaimana MVT pada Django digunakan.

**Chat History Links** :  
[Chat for Tutorial 2](https://gemini.google.com/share/d/1dB_16qZya3zplEA5BiDgSB9PfrJFFWAg?usp=sharing)
[Chat for Tugas 2](https://gemini.google.com/share/d/19bnQsGvDLOdR2w17SdUSCqBkDbeR96xT?usp=sharing)


**AI Limitations and Takeaways:**  
- Saya tidak terlalu mengalami banyak limitations ketika menggunakan AI pada minggu ini, mungkin salah satu batasannya adalah karena saya menggunakan web-chat based AI dibanding agent, saya mengalami kesusahan untuk menyesuaikan context kode yang saya inginkan dengan apa yang dioutput karena Gemini tidak memiliki akses untuk membaca keseluruhan codebase saya. Hal tersebut menyebabkan berbagai overlap/duplicate/redundant code yang ujungnya harus saya refactor. Namun, menurut saya hal tersebut merupakan suatu plus karena memaksakan saya untuk truly understand codebase yang sudah saya buat dan mengidentifikasi berbagai problem yang terdapat pada codebase saya.