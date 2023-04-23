from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render
from pyramid.response import FileResponse
import csv
import json
import uuid
@view_config(route_name="main")
def home(request):
    html = render('view/index.html', {}, request=request)
    return Response(html)
@view_config(route_name="benford",request_method="POST")
def Benford_law(request):
    try:
        csvfile = request.POST['file'].file
        print(csvfile)
        data_list = []
        reader = csv.reader(csvfile.read().decode('utf-8').splitlines())
        for row in reader:
            data_list.extend(row)
        results,conform= verifyLaw(data_list)
        if conform==True:
            file_location = f"json/{uuid.uuid1()}file.json"
            with open(file_location, "w+") as f:
                json.dump(results, f) 
            response = Response(json.dumps(results).encode('utf-8'))
            response.headers['Content-Disposition'] = 'attachment; filename="data.json"'
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            return Response("Data does not conform to Benford's Law.")
    except Exception as e:
        return Response("File Type Error: Please Provide a valid CSV file of Single column data!!!",status=400)

def verifyLaw(data_list):
    BENFORD_PERCENTAGES = [0, 0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]

    first_digits=[]

    for data in data_list[1:]:
        if data!='':
            int_data=int(float(data))
            first_digits.append(int_data) 

    # Count the number of first digits in the list of numbers
    first_digit_counts = {str(i): 0 for i in range(100)}
    for number in first_digits:
        first_digit = str(number)[0]
        first_digit_counts[first_digit] += 1

    
    results=[]
    for n in range(10):
        data_frequency = first_digit_counts[str(n)]
        data_frequency_percent = data_frequency / len(first_digits)
        benford_frequency = len(first_digits) * BENFORD_PERCENTAGES[n]
        benford_frequency_percent = BENFORD_PERCENTAGES[n]
        difference_frequency = data_frequency - benford_frequency
        difference_frequency_percent = data_frequency_percent - benford_frequency_percent

        results.append({"n": n,
                        "data_frequency":               data_frequency,
                        "data_frequency_percent":       data_frequency_percent,
                        "benford_frequency":            benford_frequency,
                        "benford_frequency_percent":    benford_frequency_percent,
                        "difference_frequency":         difference_frequency,
                        "difference_frequency_percent": difference_frequency_percent})
        
    conform = all(results[i]["difference_frequency_percent"] < 0.1 for i in range(1, 10))
    print(results)
    return results,conform
    
if __name__ == '__main__':
    settings = {}
    with Configurator(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.add_route('main', '/')
        config.add_route('benford','/benford')
        config.add_settings(watch_files=True)
        config.scan()
        config.add_jinja2_renderer('.html')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
