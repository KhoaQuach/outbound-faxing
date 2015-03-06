from flask import Flask
app = Flask(__name__)

@app.route('/')
def about():
    return "Khoa's outbound faxing server"

@app.route('/obfaxes', , methods=['GET', 'POST'])
def get_obfaxes(client_id):
    if request.method == 'POST':
        submit_new_obfax(client_id)
    else:
        get_obfaxes(client_id)

if __name__ == '__main__':
    app.debug = True
    app.run()
