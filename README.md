

# **Streamlit Setup Instructions (Windows, macOS, WSL)**
---

# **1. Install Python**

### **Windows**

* Download from: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
* When installing, **check “Add Python to PATH”**
* Finish installation

### **macOS**

* Install Python using **Homebrew**:

  ```sh
  brew install python
  ```

  or download from:
  [https://www.python.org/downloads/mac-osx/](https://www.python.org/downloads/mac-osx/)

### **WSL (Ubuntu)**

* Update and install Python:

  ```sh
  sudo apt update
  sudo apt install python3 python3-venv python3-pip -y
  ```

---

# **2. Create a Virtual Environment**

### Windows (PowerShell or CMD)

```sh
python -m venv venv
venv\Scripts\activate
```

### macOS

```sh
python3 -m venv venv
source venv/bin/activate
```

### WSL (Ubuntu)

```sh
python3 -m venv venv
source venv/bin/activate
```

---

# **3. Install Streamlit**

```sh
pip install streamlit
```

---

# **4. Run Your Streamlit App**

```sh
streamlit run app.py
```

---

# **(Optional) Running the AI Features**

To enable AI functionality like OpenAI:

---

# **Enable AI Features**

1. Create a `.env` file in your project root (if you haven’t already):

```
OPENAI_API_KEY=your_key_here
```
---

