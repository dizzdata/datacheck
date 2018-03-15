import os
from django.http import HttpResponse,HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect
from bigquery import get_client
from datacheck.settings import BASE_DIR
import pandas as pd
from bs4 import BeautifulSoup
import datetime

client = None

def html_to_list(table_html):
    """
    :desc: Converts the input html table to a 2D list that
           can be given as a input to the print_table function
    :param: `table_html` HTML text contaning <table> tag
    """
    if not table_html:
        return []

    soup = BeautifulSoup(table_html, 'html.parser')
    rows = soup.find('table').find_all('tr')
    th_tags = rows[0].find_all('th')
    headings = [[row.text.strip() for row in th_tags]]
    headings[0] = [x.upper() for x in headings[0]]
    data_rows = headings + [[data.text.strip() for data in row.find_all('td')] for row in rows[1:]]
    index = []
    # print(data_rows[0].index('DAY'),data_rows[0].index('MONTH'),data_rows[0].index('YEAR'))
    data_rows[0].pop(0)
    index.append(data_rows[0].index('DAY'))
    index.append(data_rows[0].index('MONTH'))
    index.append(data_rows[0].index('YEAR'))
    for data_row in data_rows:
        date = data_row[index[2]] + '-' + data_row[index[1]] + '-' + data_row[index[0]]
        data_row.pop(index[0])
        data_row.pop(index[1])
        data_row.pop()
        data_row.append(date)
    return data_rows

def takeSecond(elem):
    return elem[1]

def root(request):
    global client
    query_string = None
    if client is not None and request.method == 'POST':
        query_string=request.POST.get('query', 'empty')
        print(query_string)
        print('in post  ', client)
        results=compute_query(query_string)
        data_rows = html_to_list(results)
        all_results = []
        table_x = []
        table_y = []
        title = ''
        time = []
        for i in range (0,len(data_rows[0])-1):
            title = data_rows[0][i]
            for data_row in data_rows[1:]:
                table_x.append((str(data_row[len(data_row)-1])))
                table_y.append(int(data_row[0]))
                if i == 0:
                    time.append(datetime.datetime.strptime(((str(data_row[len(data_row)-1]))), '%Y-%m-%d'))
            all_results.append([title,table_x,table_y])
        print(all_results,"adasd")
        temp = []
        for i in range(0,len(data_rows[0])-1):
            all_results[i][1],temp = (list(t) for t in zip(*sorted(zip(all_results[i][1],time),key=takeSecond)))
            all_results[i][2],temp = (list(t) for t in zip(*sorted(zip(all_results[i][2],time),key=takeSecond)))
        return render(request,'index.html',{'results': all_results})

    else:
        print('in get  ', client)
        return render(request, 'index.html')


def report(request):
    return render(request, 'reporting.html')


def fileupload(request):
    if request.method == 'POST':
        myfile = request.FILES['creds']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        #uploaded_file_url = fs.url(filename)
        request=authenticate(request,filename)
        if request.authenticated and request.client!=None:
            return redirect('root')
        else:
            return render(request,'upload.html',{'status':False})
    else:
        return render(request, 'upload.html')


def authenticate(request,filename):
    try:
        global client
        f_path = os.path.join(BASE_DIR, 'media')
        fin_path=os.path.join(f_path,filename)
        json_key = fin_path
        client = get_client(json_key_file=json_key, readonly=True)
        request.authenticated=True
        request.client=client
        return request
    except Exception as e:
        print(e)
        request.authenticated = False
        request.client=None
        return request


def compute_query(query_string):
    job_id, _results = client.query(query_string)
    results = client.get_query_rows(job_id)
    resultsdf = pd.DataFrame(results)
    return resultsdf.to_html()
