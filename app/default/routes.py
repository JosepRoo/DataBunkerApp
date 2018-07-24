from . import default, groupon


@default.route('/')
def home():
    return default.send_static_file('index.html')


@groupon.route('/')
def home_groupon(folder=None):
    print(folder)
    return groupon.send_static_file('index.html')