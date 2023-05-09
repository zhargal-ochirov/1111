import json
import operator
from sklearn import svm


def get_frequency():
    with open(
            r'Z:\pythonProject\Вкр\vkr\media\documents\letterFrequency.json',
            encoding='utf-8-sig') as f:
        frequency = json.load(f)
    frequency.sort(key=operator.itemgetter('key'))
    return frequency


def patterns(patterns):
    # шаблоны пользователей и ожидаемые значения
    patterns_users = []
    expected_values = []
    for i in patterns:
        patterns_users.append(i['login'])
        expected_values.append(i['expectedValues'])
    return patterns_users, expected_values, patterns


def sessions(sessions):
    # пользователи и значения
    session_users = []
    session_letters = []
    for i in sessions:
        session_users.append(i['Login'])
        session_letters.append(i['Letters'])
    return session_users, session_letters


def Eucliadian_dist(expected_values, session_letters, n_session, patterns_users):
    result = []
    for i in expected_values:
        dist_eucliadian = 0
        for j in range(len(i)):
            if i[j]['Key'] == session_letters[n_session][j]['Key']:
                dist_eucliadian += pow(float(i[j]['Value']) - session_letters[n_session][j]['Value'], 2)
                k = pow(dist_eucliadian, 0.5)
        result.append(k)
    dict_result = dict(zip(patterns_users, result))
    dict_result_sort = (dict(sorted(dict_result.items(), key=lambda x: x[1])))
    result = (next(iter(dict_result_sort)))
    return result


def Eucliadian_freq_dist(expected_values, session_letters, n_session, frequency, patterns_users):
    result = []
    for i in expected_values:
        dist_eucliadian = 0
        for j in range(len(i)):
            if i[j]['Key'] == session_letters[n_session][j]['Key'] == frequency[j]['key']:
                dist_eucliadian += pow(float(i[j]['Value']) - session_letters[n_session][j]['Value'], 2) * float(frequency[j]['value'])
                k = pow(dist_eucliadian, 0.5)
        result.append(k)
    dict_result = dict(zip(patterns_users, result))
    dict_result_sort = (dict(sorted(dict_result.items(), key=lambda x: x[1])))
    result = (next(iter(dict_result_sort)))
    return result


def Manhattan_dist(expected_values, session_letters, n_session, patterns_users):
    result = []
    for i in expected_values:
        dist_manhattan = 0
        for j in range(len(i)):
            if i[j]['Key'] == session_letters[n_session][j]['Key']:
                dist_manhattan += abs(float(i[j]['Value']) - session_letters[n_session][j]['Value'])
                k = dist_manhattan
        result.append(k)
    dict_result = dict(zip(patterns_users, result))
    dict_result_sort = (dict(sorted(dict_result.items(), key=lambda x: x[1])))
    result = (next(iter(dict_result_sort)))
    return result


def Manhattan_freq_dist(expected_values, session_letters, n_session, frequency, patterns_users):
    result = []
    for i in expected_values:
        dist_manhattan_freq = 0
        for j in range(len(i)):
            if i[j]['Key'] == session_letters[n_session][j]['Key'] == frequency[j]['key']:
                dist_manhattan_freq += abs(float(i[j]['Value']) - session_letters[n_session][j]['Value']) * float(frequency[j]['value'])
                k = dist_manhattan_freq
        result.append(k)
    dict_result = dict(zip(patterns_users, result))
    dict_result_sort = (dict(sorted(dict_result.items(), key=lambda x: x[1])))
    result = (next(iter(dict_result_sort)))
    # liquid_user = test1(patterns_users, expected_values, session_users, session_letters, border)
    return result


def SVM(expected_values, patterns_users,session_letters, n_session):
    x = expected_values
    y_train = patterns_users
    session_letters = session_letters[n_session]

    x_train = []
    train = []
    for i in x:
        for j in i:
            k = j.get('Value')
            train.append(k)
        x_train.append(train)
        train = []
    y_pr = []
    for i in session_letters:
        p = i.get('Value')
        y_pr.append(p)

    clf = svm.SVC()
    clf.fit(x_train, y_train)
    result = (clf.predict([y_pr]))

    return result[0]


def select_method(expected_values, session_letters, n_session, frequency, patterns_users,temp, session_users, border):
    if temp == '1':
        rec_user = Eucliadian_dist(expected_values, session_letters, n_session, patterns_users)
        liquid_user, real_user = test1(patterns_users, expected_values, session_users, session_letters, border)
        if rec_user == real_user[n_session]:
            result = rec_user
        else:
            result = "Неопознаный пользователь"

    elif temp == '2':
        rec_user = Manhattan_dist(expected_values, session_letters, n_session, patterns_users)
        liquid_user, real_user = test1(patterns_users, expected_values, session_users, session_letters, border)
        if rec_user == real_user[n_session]:
            result = rec_user
        else:
            result = "Неопознаный пользователь"
    elif temp == '3':
        rec_user = Eucliadian_freq_dist(expected_values, session_letters, n_session, frequency, patterns_users)
        liquid_user, real_user = test1(patterns_users, expected_values, session_users, session_letters, border)
        if rec_user == real_user[n_session]:
            result = rec_user
        else:
            result = "Неопознаный пользователь"
    elif temp == '4':
        rec_user = Manhattan_freq_dist(expected_values, session_letters, n_session, frequency, patterns_users)
        liquid_user, real_user = test1(patterns_users, expected_values, session_users, session_letters, border)
        if rec_user == real_user[n_session]:
            result = rec_user
        else:
            result = "Неопознаный пользователь"
    elif temp == '5':
        rec_user = SVM(expected_values, patterns_users,session_letters, n_session)
        liquid_user, real_user = test1(patterns_users, expected_values, session_users, session_letters, border)
        if rec_user == real_user[n_session]:
            result = rec_user
        else:
            result = "Неопознаный пользователь" + rec_user
    return result


def test1(patterns_users, expected_values, session_users, session_letters, border):
    dict_pattern = dict(zip(patterns_users, expected_values))
    dict_session = dict(zip(session_users, session_letters))
    pattern_sum = 0
    session_sum = 0
    real_users = []
    result = []
    for i in patterns_users:
        k = dict_pattern[i]
        for val in k:
            pattern_sum += float(val.get('Value'))
        # print(pattern_sum)
        for j in session_users:
            p = dict_session[j]
            real_users.append(j)
            if i == j:
                for val_s in p:
                    session_sum += float(val_s.get('Value'))
                result.append(abs(session_sum - pattern_sum) < 0.01 * border * pattern_sum)
                # print(session_sum)
                session_sum = 0
        pattern_sum = 0
    return result, real_users


def far_frr(patterns_users, expected_values, session_users, session_letters, border, frequency):
    methods = ("Евклидово расстояние", "Манхэттенское расстояние","Евклидово расстояние + частотность",
               "Манхэттенское расстояние + частотность","Метод опорных векторов")

    border_users, real_users = test1(patterns_users, expected_values, session_users, session_letters, border)


    for i in methods:
        fr = 0  # Ложный отказ в допуске законного пользователя
        fa = 0  # Ложный доступ незаконного пользователя
        ta = 0  # Верный допуск в систему законного пользователя
        tr = 0  # Верный отказ в доступе незаконному пользователю
        if i == "Евклидово расстояние":
            for j in range(len(border_users)):
                recognized_user = Eucliadian_dist(expected_values, session_letters, j, patterns_users)
                if recognized_user == real_users[j] and border_users[j]:
                    ta += 1
                elif recognized_user != real_users[j] and border_users[j]:
                    fa += 1
                elif recognized_user == real_users[j] and not border_users[j]:
                    fr += 1
                else:
                    tr += 1
                far_frr_euc = [i, ta, fa, fr, tr]
        if i == "Манхэттенское расстояние":
            for j in range(len(border_users)):
                recognized_user = Manhattan_dist(expected_values, session_letters, j, patterns_users)
                if recognized_user == real_users[j] and border_users[j]:
                    ta += 1
                elif recognized_user != real_users[j] and border_users[j]:
                    fa += 1
                elif recognized_user == real_users[j] and not border_users[j]:
                    fr += 1
                else:
                    tr += 1
                far_frr_manh = [i, ta, fa, fr, tr]
        if i == "Евклидово расстояние + частотность":
            for j in range(len(border_users)):
                recognized_user = Eucliadian_freq_dist(expected_values, session_letters, j, frequency, patterns_users)
                if recognized_user == real_users[j] and border_users[j]:
                    ta += 1
                elif recognized_user != real_users[j] and border_users[j]:
                    fa += 1
                elif recognized_user == real_users[j] and not border_users[j]:
                    fr += 1
                else:
                    tr += 1
                far_frr_euc_freq = [i, ta, fa, fr, tr]
        if i == "Манхэттенское расстояние + частотность":
            for j in range(len(border_users)):
                recognized_user = Manhattan_freq_dist(expected_values, session_letters, j, frequency, patterns_users)
                if recognized_user == real_users[j] and border_users[j]:
                    ta += 1
                elif recognized_user != real_users[j] and border_users[j]:
                    fa += 1
                elif recognized_user == real_users[j] and not border_users[j]:
                    fr += 1
                else:
                    tr += 1
                far_frr_manh_freq = [i, ta, fa, fr, tr]
        if i == "Метод опорных векторов":
            for j in range(len(border_users)):
                recognized_user = SVM(expected_values, patterns_users,session_letters, j)
                if recognized_user == real_users[j] and border_users[j]:
                    ta += 1
                elif recognized_user != real_users[j] and border_users[j]:
                    fa += 1
                elif recognized_user == real_users[j] and not border_users[j]:
                    fr += 1
                else:
                    tr += 1
                far_frr_svm = [i, ta, fa, fr, tr]
    return far_frr_euc, far_frr_manh, far_frr_euc_freq, far_frr_manh_freq, far_frr_svm

