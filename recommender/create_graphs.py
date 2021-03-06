def create_bar_graph(term_stats, class_name, info):    
    xdata = []
    ydata = []
    for term, value in term_stats.iteritems():
        xdata.append(term)
        ydata.append(value)

    chartdata = {'x': xdata, 'y': ydata}
    charttype = 'discreteBarChart'
    chartcontainer = 'discretebarchart_container'
    data = {
        'class_name': class_name,
        'info': info,
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }
    return data


def create_horizontal_bar_graph(major, term, classes):
    xdata = []
    ydata = []
    for cls in classes:
        xdata.append(cls[0])
        ydata.append(cls[2])

    chartdata = {'x': xdata, 'y': ydata}
    data = {
        'major': major,
        'term': term,
        'charttype': 'multiBarHorizontalChart',
        'chartdata': chartdata,
        'chartcontainer': 'multibarhorizontalchart_container',
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        },
    }
    return data