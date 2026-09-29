# 📈 Week 5 Progress Report & AI Disclosure

## ⭐ Key Accomplishments
- Finished Tutorial 5 where I:
    - Implemented a toast notification feature using JS
    - Refactored showing experiences, the experience API, filtering, and adding experiences to use AJAX
    - Protected the experience modal form from XSS
- Finished Tugas Individu 5 where I:
    - Refactored showing skills, the skills API, filtering, and adding skills to use AJAX
    - Added a mock debouncing (jadi karena saya filter berdasarkan category melalui pill bukan suatu text input, saya opt untuk menambahkan suatu mock delay yang merefleksikan debouncing pada umumnya untuk memenuhi spesifikasi tugas) for filtering skills
    - Protected the skill modal form from XSS utilizing escapeHtml and strip_tags
    - Refactored the edit experience process to utilize the existing modal form with AJAX (fitur extra for 4.00 grading)

## ✅ Pertanyaan Reflektif: 
**Tugas Individu 5:**
1. Debouncing adalah suatu teknik untuk delay pengeksekusian suatu fungsi, di case ini untuk mendelay search filter setiap kali pengetikan, agar request ke server tidak dikirim setiap kali ada character baru yang diketik, melainkan ketika user sudah selesai mengetik search parameternya. Teknik ini tentu saja dapat mengurangi load server yang harus memproses request yang lebih dikit melalui teknik debouncing ini.
2. Fungsi await ketika menggunakan fetch() digunakan agar fetch tersebut berjalan asinkronus. Ketika menggunakan await, fetch akan mengembalikan suatu promise yang akan direplace oleh actual data yang diinginkan, sehingga kode di bawahnya berjalan dengan benar dan melakukan parsing terhadap data yang memang sudah direturn oleh server. Jika tidak menggunakan await, baris setelah fetch() yang mengexpect suatu data atau object akan langsung jalan padahal datanya belum direturn.
3. XSS adalah jenis attack dimana attacker memasukkan script berbahaya (biasanya Javascript) ke dalam HTML web yang dapat dieksekusi ketika user lain membuka halaman tersebut. Data yang ditampilkan oleh AJAX/JS lebih rentan karena tidak memiliki filter atau proteksi bawaan seperti di template Django alias tidak ada sanitasi otomatis sehingga harus me-utilize teknik seperti escapeHtml() atau sanitasi tag HTML secara manual yang sudah diimplementasikan pada week ini.

## 🤖 AI Disclosure
**Tools used** : Gemini  

**How it was Used / Main Guidelines:**
- Saat mengerjakan Tutorial 5, saya banyak menggunakan AI untuk menanya pertanyaan terkait steps yang dilakukan, serta untuk personalize changes/refactors yang dispesifikasikan saat tutorial agar sesuai dengan codebase pribadi saya.
- Saat mengerjakan Tugas Individu 5, saya banyak menggunakan AI untuk banyak menyesuaikan changes yang harus saya buat mengikuti tutorial untuk bagian skills. Tentu saja karena terdapat field dan bentuk HTML yang berbeda, syntax untuk building element HTMLnya juga berbeda sehingga saya extensively menggunakan AI untuk process ini. Jujur saya juga cukup overwhelmed dengan banyaknya syntax yang baru sehingga saya banyak menanyakan terhadap AI atau langsung meminta kode (dengan catatan saya juga bertanya-tanya untuk hopefully bisa lebih mengerti). Saya juga utilize AI pada implementasi fitur tambahan karena saya cukup sesat apa yang harus dirubah ketika mengimplement javascriptnya.

**Chat History Links** :  
[Chat for Tutorial 5](https://drive.google.com/file/d/17pM7BDOitAwuM-UXUdXnLQBYY89VaLFs/view?usp=sharing) \
[Chat for Tugas 5](https://drive.google.com/file/d/1bpdQSWMMM8DuIK3g5rIdugpjP0w9c4nJ/view?usp=sharing)

FYI untuk Asdos kayaknya saya kedepannya bakal export ke PDF untuk chat AInya, gatau kenapa pas mau sharing linknya setiap saya buka di incognito error gitu.


**AI Limitations and Takeaways:**  
- Pada minggu ini, saya banyak mengalami limitasi karena again seperti minggu sebelumnya, saya hanya menggunakan chat-based AI bukan agent, sehingga setiap kali saya ingin bertanya melewati prompting saay harus upload ulang semua file yang bersambungan. Hal ini tentu saja memperlambat workflow saya, namun di sisi lain juga membantu saya memastikan pemahaman saya terkait hubungan antara file yang memang sedang diimplementasikan. Saya cukup banyak langsung lempar ke AI pada minggu ini karena menurut saya JavaScript ini banyak banget boilerplatenya yang belum saya sepenuhnya paham. Mungkin kedepannya saya bisa terus berlatih especially untuk quiz minggu depan.