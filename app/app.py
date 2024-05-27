from flask import Flask, render_template, request, send_file,send_from_directory
import os
import tempfile
from filter_manager import apply_filter
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_form():
    temp_dir = tempfile.TemporaryDirectory()

    if request.method == 'POST':
        #values = request.form.getlist()
        single_file = request.files['single_file']
        selected_filter = request.form['selected_filter']
        opacity = request.form.get('selected_opacity')
        divisions =request.form.get('selected_division')

        print(f'filter: {selected_filter} \t opacity: {opacity} \t divisions; {divisions}')

        opacity = 50 if opacity is None else int(opacity)
        divisions = 100 if divisions is None else int(divisions)

        template_path = os.path.join(app.root_path, 'static/filters/')
        start_time = time.time()
        output_url = apply_filter(single_file, temp_dir.name, selected_filter, opacity=opacity, divisions=divisions, filter_file_path=template_path)
        execution_time = time.time() - start_time
        print(output_url)
        print(f"filter: {selected_filter} \t Execution time: {execution_time:.6f} seconds")
        return send_file(output_url, as_attachment=True)
    
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.route("/policy", methods=['GET'])
def policy_page():
    return render_template('policy.html')

@app.route("/about", methods=['GET'])
def about_page():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()