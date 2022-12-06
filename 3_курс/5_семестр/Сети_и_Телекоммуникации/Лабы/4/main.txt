from flask import Flask, render_template, request

app = Flask(__name__)

result = 0
page = 1

@app.route('/')
@app.route('/home')
def index():
    global result, page
    result = 0
    page = 1
    return render_template('index.html')


@app.route('/askmemore')
def allquestions():
    global page
    return render_template('askmemore.html')


@app.route('/finish<int:id>')
def finish(id):
    return "About page " + str(id)


@app.route('/api_get', methods=['POST'])
def api_get():
    global result, page
    result = 0
    text = request.form['type1']
    if text == "1":
        result = result + 1
    text = request.form['type2']
    if text == "1":
        result = result + 1
    text = request.form['type3']
    if text == "1":
        result = result + 1
    text = request.form['type4']
    if text == "1":
        result = result + 1
    text = request.form['type5']
    if text == "1":
        result = result + 1
    text = request.form['text1']
    if text == "<title>" or text == "title":
        result += 1
    text = request.form['text2']
    if text == "ru":
        result += 1
    text = request.form['text3']
    if text == "тег" or text == "тэг":
        result += 1
    text = request.form['text4']
    if text == "css":
        result += 1
    text = request.form['text5']
    if text == "h1" or text == "H1":
        result += 1
    print(result)
    with open('tests.html', 'a') as wr:
        wr.write(str(result) + '\n')
    with open('tests.html', 'r') as rd:
        res =[]
        #for line in rd:
        #    res.append([int(x) for x in line.split()])
        for line in rd:
            # считываем строку
            res.append(line.strip())
    return render_template("result.html", result=result, res=res)


if __name__ == "__main__":
    app.run(debug=True)