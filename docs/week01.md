# 📈 Week 1 Progress Report & AI Disclosure

## ⭐ Key Accomplishments
- Finished Tutorial 0 where I: 
    - Initialized the GitHub repository
    - Created an isolated Python env for installing project dependencies
    - Configured local settings and ran default database migrations
    - Launched local development server to test if the set up was done correctly through 'localhost:8000'
- Finished Tutorial 1 where I: 
    - Set up the Django project files (views, URL, template and static folders)
    - Initialized landing page (HTML and CSS file) 
    - Deployed my website to PWS 
- Finished Individual Assignment 1 where I:
    - Added a new section regarding Education below the About Me section
    - Added a cascading fading in animation that plays in the Education section (part of extra UI/UX elements for extra feature grade in rubric)

## ✅ Pertanyaan Reflektif: 
**Tugas Individu 1:**
1. Saat saya merancang struktur HTML, saya menggunakan elemen semantik HTML5 seperti `<section>` (menggantikan div) untuk menandakan bahwa itu suatu section terpisah pada website (contoh antara About Me dan Education dipisah menjadi 2 section). Saya juga menggunakan `<article>` untuk memisahkan suatu bagian/block of text dengan yang lain. Elemen tersebut membantu saya dalam membuat static web karena bantu memberi contextual clues saat developing terhadap isi bagian-bagian tersebut, serta membantu dalam readability dan SEO optimization.
2. Saat mengatur CSS agar tetap responsive, saya tidak terlalu mengalami tantangan dalam menyesuaikan tata letak dari desktop ke mobile. Namun saya memang lumayan bingung terkait tipe tata letak (flex, flexbox, grid) yang harus saya gunakan dalam membuat setiap bagian website, terutama karena saya menggunakan ide untuk membuat suatu timeline dimana letak setiap content berpindah tempat dari kiri ke kanan secara alternating. Untuk hal ini, saya menggunakan AI untuk membantu dalam menyesuaikan hal tersebut.
3. Saya tidak terlalu mengalami batasan saat mencoba menyajikan informasi pada portofolio, karena saya hanya menambahkan suatu education section yang bersifatnya static, semua sudah pre-loaded. Mungkin kedepannya, jika saya ingin membuat suatu section baru seperti Projects atau Experience, dimana saya tetap terus dapat menambahkan konten baru ke web, saya akan mengalami batasan dimana saya harus terus mengupdate ulang manual HTML dan CSS filesnya dimana hal ini akan menghabiskan banyak waktu dan tenaga. Hal ini adalah mengapa kita menggunakan Django, dimana kita bisa dapat membangun suatu HTML website dynamically menggunakan template file dan data yang kita upload untuk mengisi template tersebut.

## 🤖 AI Disclosure
**Tools used** : Gemini  

**How it was Used :**
- Saat mengerjakan Tutorial 0, saya menggunakan Gemini untuk menjelaskan berbagai steps ketika melakukan set up untuk project portofolio ini karena saya kurang familiar dengan menggunakan Django, membuat file .env, tujuan membuat file seperti itu, dsb. Saya juga menggunakan AI untuk membantu saya dalam outlining apa yang harus masuk ke dalam dokumentasi dan bagaimana melakukan set-up dokumentasi yang lengkap. Saya memutuskan untuk melakukan hal ini dikarenakan terdapat rubrik terkait dokumentasi dan saya juga ingin membangun habit dan belajar cara bagaimana membuat dokumentasi yang professional.
- Saat mengerjakan Tutorial 1, saya menggunakan Gemini hanya untuk menjelaskan berbagai steps ketika melakukan set up file dan folder Django, serta untuk menjelaskan syntax dan struktur file HTML dan CSS.
- Saat mengerjakan Tugas Individu 1, saya menggunakan Gemini untuk menjelaskan ulang struktur HTML dan CSS styling dari keseluruhan website. Lalu, karena saya memang kurang familiar dengan syntax CSS dan bagaimana styling yang baik, saya banyak melemparkan pertanyaan ke Gemini bagaimana mengimplementasi suatu fitur atau perubahan pada website untuk melihat kodenya. Disini saya memang banyak melakukan copy paste, namun saya tetap berprinsip dengan tidak meminta Gemini untuk mengenerate keseluruhan website (one-shot) pada 1 prompt melainkan saya tetap melakukannya bertahap dan per fitur, dengan mengibaratkan saya melakukan codingnya secara terstruktur, dan menggunakan Gemini untuk syntaxnya. Saya juga mengandalkan Gemini untuk membantu saya mengimplementasi feature animasi yang saya inginkan dengan menggunakan potongan kode JavaScript yang singkat karena saya belum pernah menggunakannya.

**Chat History Links** :  
[Chat for Tutorial 0](https://gemini.google.com/share/d/1I9uXUnEVEyTI4dFoSONo7znqeuElRJS5?usp=sharing)  
[Chat for Tutorial 1](https://gemini.google.com/share/d/1DRl7wvHUVw79v3YAcGR9mzvusq2efYDE?usp=sharing)
[Chat for Tugas 1](https://gemini.google.com/share/d/1HAvzyUoTatQbe3jNmsK9CuI0jTHZuWh8?usp=sharing) 

**Main Guidelines When Using AI:**   
Dalam menggunakan AI pada Tutorial 0 & 1, saya tidak pernah melakukan asal copy paste sama sekali (copy paste pun jarang kecuali saat melengkapi README.md,requirements atau menggunakan command yang diberi oleh AI) dan saya selalu berusaha untuk menggali informasi yang diberikan oleh AI tsb. (saya cukup percaya bahwa hal ini terefleksikan di history chat saya).
Dalam menggunakan AI pada Tugas Individu 1, saya banyak melakukan copy paste karena saya merasa kurang hafal dengan syntax terutama CSS. Namun seperti saya sebut di bagian atas, saya tidak melakukan copy paste one-shot, dan tetap berusaha untuk menggunakan AI hanya sebagai tools untuk membantu saya mengerjakan dan membangun websitenya step-by-step. 

**AI Limitations and Takeaways:**  
- Ketika menggunakan AI untuk menjelaskan bagaimana cara membuat dokumentasi set-up dan installation yang baik, salah satu command yang saya run yakni `pip freeze` me-replace file `requirements.txt` yang sudah diberikan di tutorial dengan file baru dengan package-package yang telah terinstall di virtual environment saya. Awalnya, saya mengira bahwa hal ini aman saja. Namun, ketika saya mencoba deploy ke PWS di akhir tutorial 1, servernya menghadapi saat mencoba download requirements yang diperbarui tersebut dikarenakan `pip`-nya belum updated, sehingga project tidak bisa di build. Hal tersebut menyebabkan saya butuh waktu yang cukup lama untuk troubleshoot karena harus membaca logs di PWS terlebih dahulu. Mungkin ini akan menjadi pelajaran kedepan bagi saya untuk mengevaluasi konsekuensi menjalankan suatu command yang telah diberikan oleh AI.