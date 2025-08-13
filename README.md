# <div align="center">My rating URFU</div>

<div align="center">
<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/aiogram">
</div>

## :scroll: A brief history
**The name of the repository is a** <s>joke!</s>

This is a Telegram bot that displays competition lists. 
The thing is, this university publishes the lists for each field quite late, and the only lists where you can see the results of your entrance exams are mixed, meaning you can't find out where you stand. 
I created this bot for my girlfriend, and later for her friend, so I had to make a multi-user system. Initially, it was supposed to be a parser based on beautifulSoup, but due to the peculiarities of the site with those mixed competitive lists, nothing worked out. 
But then, after analyzing the site's network traffic, I found a GET request that is sent to retrieve data, AND THEN I noticed that the site's backend does not have a CORS policy configured)) And the data is retrieved directly from the university's backend (seriously, how stupid is that?). 

## ⚙️ How it works

1. **Data update**

* If the data in PostgreSQL is more than 1 hour old, the bot starts collecting current data.
* Requests are executed in multithreaded mode.
   * The backend returns a maximum of 100 applicants per request, so the bot makes up to 50 requests (≈ 5,000 applicants per cycle).

2. **Data processing**
   Each applicant is added to the database only if:

* they have submitted their consent to admission (original certificate),
* they are applying for a state-funded place,
* they are participating in one of the areas specified in `CODES`.
> if (subject["speciality"].split()[0] in CODES) and (subject["edu_doc_original"] == True) and (subject["compensation"] == "Бюджетная основа") 

3. **Sorting**
   Data is sorted:

* first by priority (in ascending order),
* within priority — by total score (in descending order).

4. **User location search**
   The user enters their `regid`, the bot finds it in the list and displays the current place.

5. **Additional function**
   You can download the complete table for each direction for independent analysis. The table is already sorted according to the specified rules.

<details>
<summary><b> Applicant data structure</b></summary>

```
 "regnum": 3560363,
      "applications": [
        {
          "total_mark": 230,
          "edu_doc_original": false,
          "achievs": 0,
          "status_epgu": "",
          "competition": "Основные места в рамках КЦП",
          "program": "Информационно-аналитические системы безопасности",
          "priority": 1,
          "speciality": "10.05.04 Информационно-аналитические системы безопасности",
          "is_without_tests": false,
          "familirization": "Очная",
          "avgm": 0,
          "institute": "ИРИТ-РТФ",
          "compensation": "Бюджетная основа",
          "status": "Участвует в конкурсе",
          "marks": {
            "Математика": {
              "mark": 74,
              "case": "ЕГЭ"
            },
            "Физика": {
              "mark": 73,
              "case": "ЕГЭ"
            },
            "Русский язык": {
              "mark": 83,
              "case": "ЕГЭ"
            }
          }
        },
        {
          "total_mark": 230,
          "edu_doc_original": false,
          "achievs": 0,
          "status_epgu": "",
"competition": "Основные места в рамках КЦП",
          "program": "Информационная безопасность телекоммуникационных систем",
          "priority": 2,
          "speciality": "10.05.02 Информационная безопасность телекоммуникационных систем",
          "is_without_tests": false,
          "familirization": "Очная",
          "avgm": 0,
          "institute": "ИРИТ-РТФ",
          "compensation": "Бюджетная основа",
          "status": "Участвует в конкурсе",
          "marks": {
            "Математика": {
              "mark": 74,
              "case": "ЕГЭ"
            },
            "Физика": {
              "mark": 73,
              "case": "ЕГЭ"
            },
            "Русский язык": {
              "mark": 83,
              "case": "ЕГЭ"
            }
          }
        },
        {
          "total_mark": 230,
          "edu_doc_original": false,
          "achievs": 0,
          "status_epgu": "",
          "competition": "Основные места в рамках КЦП",
          "program": "Математические методы защиты информации",
          "priority": 3,
          "speciality": "10.05.01 Компьютерная безопасность",
          "is_without_tests": false,
          "familirization": "Очная",
          "avgm": 0,
          "institute": "ИЕНиМ",
          "compensation": "Бюджетная основа",
          "status": "Участвует в конкурсе",
          "marks": {
            "Математика": {
              "mark": 74,
              "case": "ЕГЭ"
            },
            "Физика": {
              "mark": 73,
              "case": "ЕГЭ"
            },
            "Русский язык": {
              "mark": 83,
              "case": "ЕГЭ"
            }
          }
        },
        {
          "total_mark": 230,
          "edu_doc_original": false,
          "achievs": 0,
          "status_epgu": "",
          "competition": "Основные места в рамках КЦП",
          "program": "Безопасность компьютерных систем",
          "priority": 4,
          "speciality": "10.03.01 Информационная безопасность",
          "is_without_tests": false,
          "familirization": "Очная",
          "avgm": 0,
          "institute": "ИРИТ-РТФ",
          "compensation": "Бюджетная основа",
          "status": "Участвует в конкурсе",
          "marks": {
            "Математика": {
              "mark": 74,
              "case": "ЕГЭ"
            },
            "Физика": {
              "mark": 73,
              "case": "ЕГЭ"
            },
            "Русский язык": {
              "mark": 83,
              "case": "ЕГЭ"
            }
          }
        },
        {
          "total_mark": 230,
          "edu_doc_original": false,
          "achievs": 0,
          "status_epgu": "",
          "competition": "Основные места в рамках КЦП",
          "program": "Строительство зданий, сооружений и развитие территорий",
          "priority": 5,
          "speciality": "08.03.01 Строительство",
          "is_without_tests": false,
          "familirization": "Очная",
          "avgm": 0,
          "institute": "ИСА",
          "compensation": "Бюджетная основа",
          "status": "Участвует в конкурсе",
          "marks": {
            "Математика": {
              "mark": 74,
              "case": "ЕГЭ"
            },
            "Физика": {
              "mark": 73,
              "case": "ЕГЭ"
            },
            "Русский язык": {
              "mark": 83,
              "case": "ЕГЭ"
            }
          }
        }
      ]
    },
```
</details>

---

## 🚀 Installation and launch

### 1. Clone the repository

```bash
git clone https://github.com/Hitoshi144/urfu_ddos_bot.git
cd urfu_ddos_bot
```

---

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS (Bash/Zsh):**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Set dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Install [Docker](https://www.docker.com/)

---

### 5. Create a PostgreSQL database in Docker

```bash
docker run --name my-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=mydb -p 5432:5432 -d postgres
```

---

### 6. Create a Telegram bot

1. Write to [@BotFather](https://t.me/BotFather)
2. Use the command `/newbot` and follow the instructions
3. Copy the **token** for connection

---

### 7. Create a `.env` file in the project folder

```
TOKEN="your_bot_token"
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydb
DB_USER=postgres
DB_PASSWORD=postgres
```
> You can use your settings to create a database in Docker and for .env.

---

### 8. Start PostgreSQL (if not already running)

```bash
docker start my-postgres
```

---

### 9. Launch the bot

**Windows:**

```powershell
python main.py
```

**Linux / macOS:**

```bash
python3 main.py
```

---

## 🎉 That's it! 

The project is complete and **may not work** at certain times, for example, when there is no student recruitment, as its functionality depends entirely on the university's backend.

---

## License

Distributed under the **MIT** License. See [LICENSE](https://github.com/Hitoshi144/urfu_ddos_bot/blob/master/LICENSE) for more information.
