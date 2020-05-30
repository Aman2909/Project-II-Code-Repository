"""
In fullfillment of Project Work - II
Aman Pathak
EN16CS301033
DATA SCIENCE INTERN
FEB-AUG 2020

COPYRIGHT : HVANTAGE TECHNOLOGIES
"""


from flask import Flask, request
from DucklingEntityParser.python_files import extraction

app = Flask(__name__)


@app.route('/test')
def test_server():
    return "System Entity Extraction API has been launched successfully!"


@app.route('/api', methods=['POST'])
def start_engine():
    entities = request.args['entities']
    text = request.args['text']
    parsed = extraction.parser(str(text), entities)
    return parsed


if __name__ == '__main__':
    app.run(debug=True)