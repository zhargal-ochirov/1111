from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFilesForm
from .models import Data
import json
from .functions import *

def index(request):
    files = Data.objects.all()
    return render(request, 'list_files.html', {'files': files})


# def model_form_upload(request):
#     if request.method == 'POST':
#         form = FileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#     else:
#         form = FileForm()
#     return render(request, 'model_form_upload.html', {
#         'form': form
#     })
def upload_files(request):
    if request.method == 'POST':
        form = UploadFilesForm(request.POST, request.FILES)
        content = []
        if form.is_valid():
            pattern = request.FILES['pattern']
            session = request.FILES['sessions']

            pattern_data = json.load(pattern)
            session_data = json.load(session)
            temp = request.POST['choises_field']
            n_session = int(request.POST['n_session'])
            border = int(request.POST['border'])

            # pattern_data = json.loads(pattern_data)
            # session_data = json.loads(session_data)
            #
            patterns_users, expected_values, pattern = patterns(pattern_data)
            session_users, session_letters = sessions(session_data)
            frequency = get_frequency()

            result = select_method(expected_values, session_letters, n_session, frequency, patterns_users, temp,
                                   session_users, border)
            # print(expected_values)
            bollean_users, real_users = test1(patterns_users, expected_values, session_users, session_letters, border)
            print(test1(patterns_users, expected_values, session_users, session_letters, border)[0])
            # print(len(test1(patterns_users, expected_values, session_users, session_letters, border)))
            far_frr_euc, far_frr_manh, far_frr_euc_freq, far_frr_manh_freq, far_frr_svm = (far_frr(
                patterns_users, expected_values, session_users, session_letters, border, frequency))
            # for i in set(test1(patterns_users, expected_values, session_users, session_letters, border)):
            #     print(f"{i} встречается {test1(patterns_users, expected_values, session_users, session_letters, border).count(i)} раз(а)")
            # print(session_users)
            return render(request, 'result.html', {'result': result, 'far_frr_euc': far_frr_euc,
                                                   'far_frr_manh': far_frr_manh, 'far_frr_euc_freq': far_frr_euc_freq,
                                                   'far_frr_manh_freq': far_frr_manh_freq, 'far_frr_svm': far_frr_svm,
                                                   'border': border})
    else:
        form = UploadFilesForm()
    return render(request, 'upload.html', {'form': form, "form1": form})

