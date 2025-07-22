def get_marks(marks_str: str):
    marks = []
    checkpoint = 0
    for i in range(len(marks_str) - 1):
        if marks_str[i].isdigit() and not marks_str[i+1].isdigit():
            marks.append(marks_str[checkpoint : i+1].strip())
            checkpoint = i+1
    return marks

def get_regid(userId: int):
    regid = ''

    with open('regids.txt', 'r') as file:
        regids = file.readlines()

        for id in regids:
            if id.split(':')[0] == str(userId):
                regid = id.split(':')[1]
    
    return regid

def write_regid(userId: int, regId: str):
    with open('regids.txt', 'a') as file:
            file.write(f'{userId}:{regId}\n')

def change_regid(userId: int, regId: str):
    with open('regids.txt', 'r') as file:
        data = file.readlines()

    with open('regids.txt', 'w') as file:
        for i, cur in enumerate(data):
            if cur.split(':')[0] == str(userId):
                data[i] = f'{userId}:{regId}\n'
            
            file.write(data[i])

SUBJECTS = {
    '1': '37.05.01 Клиническая психология',
    '2': '38.03.02 Менеджмент',
    '3': '38.03.01 Экономика',
    '4': '05.03.06 Экология и природопользование',
    '5': '37.05.02 Психология служебной деятельности',
    '6': '43.03.01 Сервис (УГИ)',
    '7': '43.03.01 Сервис (Спортик)'
}