# 🚀 Flask Portfolio with Admin Dashboard & Database

Maine ye apna personal portfolio banaya hai jo sirf ek static page nahi hai, balki ek full-stack web application hai. Isme maine **Bootstrap** ka use karke ek responsive frontend banaya hai aur **Flask** se backend handle kiya hai.

Sabse khaas baat ye hai ki isme ek **Admin Panel** hai jahan se main saare contact messages ko manage kar sakta hoon jo database mein save hote hain.

## 🔥 Key Features

*   **Responsive UI:** Bootstrap ka use kiya hai taaki website mobile aur desktop dono par mast dikhe.
*   **Dynamic Content:** Saare projects, skills, aur awards `Project_Config.json` se load hote hain, toh code touch kiye bina content change ho jata hai.
*   **Message System (Database):** User jo bhi contact form bharte hain, wo **SQLite** database (via SQLAlchemy) mein save ho jata hai.
*   **Secure Admin Panel:** Ek hidden `/login` route hai jahan se main password daal kar saare messages aur site ka data dekh sakta hoon.
*   **Environment Safety:** Database URI aur passwords ke liye `.env` file ka use kiya hai.

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Database:** SQLite & SQLAlchemy
- **Data Management:** JSON
- **Environment:** python-dotenv

## ⚙️ Setup & Installation

1.  **Repo Clone Karein:**
    ```bash
    git clone github.com
    cd portfolio-flask
    ```

2.  **Required Libraries Install Karein:**
    ```bash
    pip install flask flask_sqlalchemy python-dotenv
    ```

3.  **Environment Variables (`.env`) Setup Karein:**
    Apni details ke saath ek `.env` file banayein:
    ```env
    SECRET_KEY=aapka_secret_key
    ADMIN_PASSWORD=admin123
    SOCIAL_GITHUB=github.com
    MY_PERSONAL_EMAIL=aapkaemail@gmail.com
    ```

4.  **Website Launch Karein:**
    ```bash
    python main.py
    ```

## 📂 Project Structure

- `main.py`: Flask ka core backend aur routes.
- `messages.db`: Jahan user ke saare messages save hote hain (auto-created).
- `Project_Config.json`: Isme mere saare projects aur skills ka data hai.
- `templates/`: Mere HTML files (Index, Admin, Login).
- `static/`: CSS, JS aur Images.

## 🔐 Admin Access
Agar aapko messages dekhne hain, toh browser mein `/login` par jayein aur apna password enter karein jo `.env` mein set kiya hai. Login ke baad aap `/admin` dashboard par saare records dekh payenge.

---
**Made with ❤️ by [Piyush Kalbande](github.com)** 
*Mera portfolio meri coding journey ka ek chhota sa hissa hai.*
