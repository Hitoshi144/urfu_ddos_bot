def get_marks(marks_str: str):
    marks = []
    checkpoint = 0
    for i in range(len(marks_str) - 1):
        if marks_str[i].isdigit() and not marks_str[i+1].isdigit():
            marks.append(marks_str[checkpoint : i+1].strip())
            checkpoint = i+1
    return marks

SUBJECTS = {
    '1': '37.05.01 Клиническая психология',
    '2': '38.03.02 Менеджмент',
    '3': '38.03.01 Экономика',
    '4': '05.03.06 Экология и природопользование'
}