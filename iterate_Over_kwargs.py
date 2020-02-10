## Creating Tag object using **kwargs):

def tag(location, **data):
    func = {}
    func['location']=location
    for name, value in data.items():
        func[name] = value
    return func

print(tag('NYC', href="http://treyhunner.com"))
print(tag('CHI', height=20, width=40, src="face.jpg"))
