from flask import Flask, render_template, request


app = Flask(__name__)

NAME = 'text'

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/result")
def result():
    return render_template("result.html", name=NAME)    
    
    
@app.route("/test", methods = ["POST"])
def test():
    if request.method == "POST":
        
        
        return render_template("index.html", output = result)
    
    
if __name__ == "__main__":
    app.run(debug=True)