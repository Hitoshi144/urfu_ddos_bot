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
