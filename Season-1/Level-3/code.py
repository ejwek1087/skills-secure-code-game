# Welcome to Secure Code Game Season-1/Level-3!
# You know how to play by now, good luck!

import os
from flask import Flask, request

### Unrelated to the exercise -- Starts here -- Please ignore
app = Flask(__name__)
@app.route("/")
def source():
    TaxPayer('foo', 'bar').get_tax_form_attachment(request.args["input"])
    TaxPayer('foo', 'bar').get_prof_picture(request.args["input"])
### Unrelated to the exercise -- Ends here -- Please ignore

class TaxPayer:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.prof_picture = None
        self.tax_form_attachment = None

    # returns the path of an optional profile picture that users can set
    def get_prof_picture(self, path=None):
        # setting a profile picture is optional
        if not path:
            return None

        # defends against path traversal attacks
        if path.startswith('/') or path.startswith('..'):
            return None

        # builds path
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prof_picture_path = os.path.normpath(os.path.join(base_dir, path))

        with open(prof_picture_path, 'rb') as pic:
            _picture = bytearray(pic.read())

        # assume that image is returned on screen after this
        return prof_picture_path
    # returns the path of an attached tax form that every user should submit
    def get_tax_form_attachment(self, path=None):
        if not path:
            raise Exception("Error: Tax form is required for all users")

        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Resolve symlinks/.. and enforce the target stays within base_dir
        resolved = os.path.realpath(path)
        base_real = os.path.realpath(base_dir)

        # If resolved is outside base_dir, reject
        if os.path.commonpath([resolved, base_real]) != base_real:
            return None

        with open(resolved, 'rb') as form:
            _tax_data = bytearray(form.read())

        # assume that tax data is returned on screen after this
        return resolved


        # Reject obvious traversal/absolute paths
        if os.path.isabs(path) or path.startswith('..'):
            return None

        # Force reads to stay inside this level folder (base_dir)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        safe_path = os.path.normpath(os.path.join(base_dir, path))

        # Ensure safe_path is still within base_dir after normalization
        base_dir_norm = os.path.normpath(base_dir) + os.sep
        if not safe_path.startswith(base_dir_norm):
            return None

        with open(safe_path, 'rb') as form:
            _tax_data = bytearray(form.read())

        # assume that tax data is returned on screen after this
        return safe_path
