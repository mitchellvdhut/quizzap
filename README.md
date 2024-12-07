# 🚀 Quizzap

🎉 A fun and free Kahoot clone, built just for the thrill of it!  
Created and maintained by [Mitchell](https://github.com/mitchellvdhut) and [Tijmen](https://github.com/troshujin).  

---

## 🧐 About

Quizzap lets you manage quizzes, host quiz sessions, and have players join in for some epic trivia battles. Why pay for fun when you can have it for free? 😏  
And yes, we even added an **Anarchy mode** for the rebels out there who really despise Authentication. 🔥

---

## ✨ Features

- 📝 **Create and manage your quizzes.**
- 🎮 **Host quiz sessions and invite participants.**
- 📱 **Mobile-friendly for gaming on the go.**
- 🔒 **Secure authentication** (if you're into that sort of thing).
- 🚫 **Anarchy Mode**: Skip authentication and embrace chaos.
- 🐳 **Dockerized for easy deployment.**
- 🎛️ **Custom WebSocket Manager** for real-time action.

---

## 🛠️ How to Run Quizzap

Follow these steps to set up Quizzap locally. 🚀  

### **Backend Setup**  

First, make sure to setup the environment variables:

1. Create a `.env` file in the `backend` folder.
2. Copy over all values from `env.example`.
3. Change them however you see fit.

Run the backend locally with HTTPS:  

1. **Generate Certificates**  
  Use this command (requires GIT installed):  
  *Used in a Bash terminal.*
  ```bash
  "C:\Program Files\Git\usr\bin\openssl.exe" req -x509 -newkey rsa:4096 -keyout nginx/certs/nginx.key -out nginx/certs/nginx.crt -days 365 -nodes  
  ```

2. **Start the Backend**  
  Spin it up using Docker:  
  ```cmd
  docker compose up --build  
  ```

---

### **Frontend Setup**  

Currently, the frontend isn't Dockerized. You'll need **Node.js** installed.  

1. Navigate to the `frontend` folder:  
  ```cmd
  cd frontend  
  ```

2. Install dependencies:
  ```cmd
  npm i  
  ```

3. Start the development server:
  ```cmd
  npm run
  ``` 

---

## 🎯 Usage  

- **Backend API Docs**: [https://localhost/api/latest/docs](https://localhost/api/latest/docs)  
- **Quiz Sessions**: [https://localhost/](https://localhost/)  
- **Frontend App**: [http://localhost:5173/](http://localhost:5173/)  
- **phpMyAdmin**: [http://localhost:8080/](http://localhost:8080/)  

---

## ⚙️ Technologies  

### 🖥️ **Backend**  
- 🐍 **Python (FastAPI)**: Robust and modern backend framework.  
- ⚡ **WebSockets**: For real-time updates.  
- 🧩 **nginx**: HTTPS reverse proxy.  
- 🐋 **Docker**: Containerization for easy deployment.  
- 🛢️ **MySQL**: Reliable database solution.  
- 🛠️ **phpMyAdmin**: Manage the database effortlessly.  

### 🌐 **Frontend**  
@Mitchell, your expertise is needed! But so far, here's what we've got:  
- 🟢 **Node.js**: JavaScript runtime.  
- 🚀 **Vite**: Lightning-fast development tool.  
- 🎨 **Vue 3**: Reactive frontend framework.  
- 🎨 **SCSS**: Enhanced CSS for styling.  

---

## 🤝 Contribute  

Want to make Quizzap even better? Awesome! Here's how you can help:  

1. Fork the repository.  
2. Create a feature branch:  
  ```cmd
  git checkout -b feature-name
  ```

3. Commit your changes:  
  ```cmd
  git commit -m "Add your message here" 
  ``` 

4. Push the branch:  
  ```cmd
  git push origin feature-name
  ```

5. Open a Pull Request.

---

## 📜 License  

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

🚀 **Ready to start quizzing? Let's go!**
