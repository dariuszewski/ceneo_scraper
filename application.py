from flask import Flask, render_template, Response, send_file, request
import io
import scraper


application = app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/attach/", methods=['POST'])
def attach():

    category = request.form['category']
    parameters = request.form['parameters']
    formatting = request.form['formatting']
    if parameters == '':
        parameters = category.lower()
    report = scraper.scraper(category, parameters, formatting)
    bin_rep = bytes(report, encoding='utf-8')
    bin_file = io.BytesIO(bin_rep) #to send files over network the need to be a binary stream
    formats = {
    'Python dict' : '.py',
    'JSON' : '.json',
    'CSV' : '.csv',
    'Short text' : '.txt',
    'XML' : '.xml'
    }
    return send_file(bin_file, attachment_filename=f"report{formats[formatting]}", as_attachment=True)
    
  
# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
