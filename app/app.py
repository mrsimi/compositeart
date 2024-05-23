from flask import Flask, render_template, request, send_file,send_from_directory
import os
import tempfile
from filter import apply_filter

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_form():
    temp_dir = tempfile.TemporaryDirectory()

    if request.method == 'POST':
        single_file = request.files['single_file']
        selected_filter = request.form['selected_filter']

        template_path = os.path.join(app.root_path, 'static/filters/emoji')
        output_url = apply_filter(single_file, temp_dir.name, selected_filter, template_path)
        print(output_url)
        return send_file(output_url, as_attachment=True)
    
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()