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

## 🤖 AI Disclosure
**Tools used** : Gemini  

**How it was Used :**
- Saat mengerjakan Tutorial 0, saya menggunakan Gemini untuk menjelaskan berbagai steps ketika melakukan set up untuk project portofolio ini karena saya kurang familiar dengan menggunakan Django, membuat file .env, tujuan membuat file seperti itu, dsb. Saya juga menggunakan AI untuk membantu saya dalam outlining apa yang harus masuk ke dalam dokumentasi dan bagaimana melakukan set-up dokumentasi yang lengkap. Saya memutuskan untuk melakukan hal ini dikarenakan terdapat rubrik terkait dokumentasi dan saya juga ingin membangun habit dan belajar cara bagaimana membuat dokumentasi yang professional.
- Saat mengerjakan Tutorial 1, saya menggunakan Gemini hanya untuk menjelaskan berbagai steps ketika melakukan set up file dan folder Django, serta untuk menjelaskan syntax dan struktur file HTML dan CSS.

**Chat History Links** :  
[Chat for Tutorial 0](https://gemini.google.com/share/d/1I9uXUnEVEyTI4dFoSONo7znqeuElRJS5?usp=sharing)  
[Chat for Tutorial 1](https://gemini.google.com/share/d/1DRl7wvHUVw79v3YAcGR9mzvusq2efYDE?usp=sharing)

**Main Guidelines When Using AI:**   
Dalam menggunakan AI pada minggu ini, saya tidak pernah melakukan asal copy paste sama sekali (copy paste pun jarang kecuali saat melengkapi README.md,requirements atau menggunakan command yang diberi oleh AI) dan saya selalu berusaha untuk menggali informasi yang diberikan oleh AI tsb. (saya cukup percaya bahwa hal ini terefleksikan di history chat saya).

**AI Limitations and Takeaways:**  
- Ketika menggunakan AI untuk menjelaskan bagaimana cara membuat dokumentasi set-up dan installation yang baik, salah satu command yang saya run yakni `pip freeze` me-replace file `requirements.txt` yang sudah diberikan di tutorial dengan file baru dengan package-package yang telah terinstall di virtual environment saya. Awalnya, saya mengira bahwa hal ini aman saja. Namun, ketika saya mencoba deploy ke PWS di akhir tutorial 1, servernya menghadapi saat mencoba download requirements yang diperbarui tersebut dikarenakan `pip`-nya belum updated, sehingga project tidak bisa di build. Hal tersebut menyebabkan saya butuh waktu yang cukup lama untuk troubleshoot karena harus membaca logs di PWS terlebih dahulu. Mungkin ini akan menjadi pelajaran kedepan bagi saya untuk mengevaluasi konsekuensi menjalankan suatu command yang telah diberikan oleh AI.