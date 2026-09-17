# 📈 Week 3 Progress Report & AI Disclosure

## ⭐ Key Accomplishments
- Finished Tutorial 3 where I:
    - Implemented a skeleton for my web app
    - Implemented forms to create and delete data regarding Experience into my database
    - Implemented fetching and delivering Experience data using JSON
- Finished Tugas Individu 3 where I:
    - Implemented additional forms to create and delete skills, and update data for my experiences
    - Implemented fetching and delivering Skill data using JSON
    - Implemented an extra feature (for 4.0 grading) where a toast message notification would appear after doing a CRUD transaction
    - Implemented unit tests for added view functions

## ✅ Pertanyaan Reflektif: 
**Tugas Individu 3:**
1. Kita menggunakan ModelForm pada Django karena jauh lebih efisien dibanding membuat form manual di HTML. Django akan otomatis membuat form sesuai tipe data yang terdapat pada models kita sesuai yang kita spesifikasikan. Django juga melakukan validasi data secara otomatis di backendnya. Salah satu alasan lainnya adalah masalah keamanan dimana kita diwajibkan menambahkan {% csrf_token %} yang mencegah Cross Site Request Forgery dimana suatu attacker dapat menggunakan cookie/authentication kita untuk mengirimkan request palsu langsung ke backend.
2. JSON lebih suka dibanding XML karena lebih lightweight, lebih mudah di parse, cocok dengan OOP, dan lebih human readable karena sudah tersedia sebagai key-value pairs.
3. Ketika kita menggunakan views untuk mengembalikan data portofolio dalam bentuk JSON, views tersebut akan mengakses data objects yang terdapat di database yang kemudian akan direturn kepada client yang membuat request tersebut. Namun, sebelum mengembalikannya, kita harus melakukan serialization karena objek di Django tidak bisa langsung direpresent sebagai suatu file JSON, sehingga harus dilakukan suatu proses translasi yang menyusun objek tersebut menjadi suatu key-value pair.

## 🤖 AI Disclosure
**Tools used** : Gemini  

**How it was Used / Main Guidelines:**
- Saat mengerjakan Tutorial 3, saya banyak menanyakan AI terkait steps yang dilakukan pada tutorial. Saya juga banyak menggunakan AI untuk menyesuaikan CSS atau pembuatan ModelForms yang saya buat dengan fitur yang diminta pada tutorial dikarenakan tutorial mengerjakan page terkait Projects, sedangkan saya mengubah page Experiences saya sehingga banyak styling/layout yang harus disesuaikan.
- Saat mengerjakan Tugas Individu 3, jujur saja saya banyak vibecoding, especially di bagian CSS, additional feature (toast messages) dan unit tests (all generated) karena jujur lagi banyak banget deadline dan saya lagi mencoba untuk get on top of things. Hal ini menyebabkan saya melakukan banyak copy-pasting dan troubleshooting terkait output yang dikirim oleh AI. Sebenernya overall saya lebih banyak mengikuti steps yang sudah diterapkan di tutorial, hanya saya menggunakan AI untuk menyesuaikan untuk fitur yang saya ingin bedakan (button layouts, CSS styling, dsb.).

**Chat History Links** :  
[Chat for Tutorial 3](https://gemini.google.com/share/d/1lcT86vmelHEze1oOgXDISTpKYeyEvbXp?usp=sharing) \
[Chat for Tugas 3](https://gemini.google.com/share/d/1-Mkd721BtCx0XXiQ8gR6KS3Hso3xL8m-?usp=sharing)


**AI Limitations and Takeaways:**  
- Saya tidak terlalu mengalami banyak limitations ketika menggunakan AI pada minggu ini, mungkin salah satu batasannya adalah (persis sama dengan minggu lalu) karena saya menggunakan web-chat based AI dibanding agent, saya mengalami kesusahan untuk menyesuaikan context kode yang saya inginkan dengan apa yang dioutput karena Gemini tidak memiliki akses untuk membaca keseluruhan codebase saya. Hal tersebut menyebabkan berbagai overlap/duplicate/redundant code yang ujungnya harus saya refactor. Namun, menurut saya hal tersebut merupakan suatu plus karena memaksakan saya untuk truly understand codebase yang sudah saya buat dan mengidentifikasi berbagai problem yang terdapat pada codebase saya.