# 📈 Week 10 Progress Report & AI Disclosure

## ⭐ Key Accomplishments
- Finished Tutorial 7 where I:
    - Implemented a Django Rest Framework API for my Experiences model to replace the old AJAX endpoints
    - Revised unit tests and reimplemented editor permissions using the DRF API
- Finished Tugas 6 where I:
    - Implemented a Django Rest Framework API for my Skill model to replace the old AJAX endpoints
    - Implemented an edit skill feature to accommodate PATCH requests for the DRF API
    - Built unit tests for the newly implemented API and also grew coverage to 100% by making unit tests for previous week's features.

## ✅ Pertanyaan Reflektif: 
**Tugas Individu 6:**
1. REST merupakan suatu arsitektur untuk software (dalam kasus ini web portofolio saya) yang mendefinisikan berbagai constraint seperti stateless communication, uniform interface, serta penggunaan HTTP methods yang standar (GET, POST, PUT, PATCH, DELETE) untuk mengubah data. Mengembalikan JSON saja belum cukup dikarenakan belum menerapkan prinsip REST secara penuh, karena hanya mengembalikan datanya saja, belum ada untuk update, post, ataupun delete data melalui API json yang sebelumnya saya buat. PUT digunakan untuk mereplace data keseluruhan suatu objek, jika ada field yang kosong maka data di field tsb. akan dihapus/reset ke default. PUT baik digunakan pada fitur seperti memperbarui keseluruhan profile pengguna di suatu media sosial. PATCH digunakan untuk partial updates untuk beberapa field dan baik digunakan pada fitur seperti mengubah username saja ataupun mengubah profile picture.
2. Serializer pada DRF berperan untuk mengubah objek kompleks seperti Model Django menjadi dictionary yang dapat dirender otomatis ke dalam format JSON (serialization) ataupun sebaliknya (deserialization). Keunggulan menggunakan ini dibanding membangun JsonResponse secara manual adalah teradapat automatic validation, built-in methods dan error-handling yang sudah built-in dan tidak perlu diimplement berkali-kali pada object/endpoint yang berbeda.
3. Authentication adalah proses untuk mengenali dan verifikasi identitas user, sedangkan authorization adalah proses menentukan bahwa suatu user memiliki akses untuk melakukan tindakan tertentu. Jika kita hanya mengandalkan menyembunyikan tombol pada fronend, suatu user dapat mengirim request ke API kita secara langsung melalui console atau tools seperti Curl dan membypass hal tersebut.
4. Ketika menggunakan SessionAuthentication, Django masih menggunakan session dan cookie bawaan Django melalui sessionid yang dikirim oleh browser sebagai cookie tiap request. Hal tersebut membuat website rentan terhadap CSRF yang sudah dibahas pada minggu sebelumnya, sehingga token CSRF tersebut diperlukan pada setiap request untuk memastikan bahwa request berasal dari site original. force_authenticate juga tidak cukup bahwa perlindungan CSRF berjalan karena hal tersebut hanya digunakan pada unit test dan berjalan melalui melakukan mocking yang melewati middleware authentication maupun pemeriksaan token CSRF biasa yang biasanya dialami oleh browser kita pada umumnya.

## 🤖 AI Disclosure
**Tools used** : Claude, Codex  

**How it was Used / Main Guidelines:**
- Saat mengerjakan Tutorial 7, saya menggunakan Claude untuk menyesuaikan kode yang ada di tutorial untuk menggunakan model saya yakni Experience, dikarenakan kode di tutorial memang sudah baked-in sesuai pengerjaan tutorial sebelumnya. 
- Saat mengerjakan Tugas 6, saya menggunakan Codex untuk memastikan bahwa serializer dan URL yang saya buat untuk DRF API skill tidak ada bug, dan saya memanfaatkan Codex untuk membantu menyesuaikan rerouting endpoint pada skill.HTML untuk menggunakan API baru, serta untuk mengimplementasi edit skill feature seperti di page experience. Saya juga menyerahkan seluruh pembuatan unit testing kepada Codex, baik maupun untuk API ataupun untuk melengkapi coverage.

**Chat History Links** :  
[Chat for Tutorial 7](https://claude.ai/share/89327fdb-5f2a-4286-964d-ad2bb7cc05d8) \
[Chat for Tugas 6](https://chatgpt.com/s/cx_6ae9d1ca0c4c8191bb899de59b007204)



**AI Limitations and Takeaways:**  
- Pada minggu ini, saya mengalami limitasi terkait testing terkait fungsionalitas APInya karena AI tidak bisa melakukan testing secara langsung terkait browsable endpoint yang saya build, sehingga saya banyak melakukan manual testing over and over again ketika mengimplementasi suatu change yang minor terhadap API saya agar permissions and authentication dapat masih berjalan.