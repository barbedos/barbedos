import functions_framework


FORM_HTML = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="stylesheet"
    href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
    integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T"
    crossorigin="anonymous">    <title>Document</title>
  </head>
  <body>
    <div class="container">
      <form id="myform" name="myform"
        action="https://us-central1-serverless-d2414.cloudfunctions.net/files"
        method="POST">

        <br><br>
        <div class="form-outline mb-4">
          <input type="fieldl" id="fieldl" class="form-control" />
        </div>
        <br>

        <div class="form-outline mb-4">
          <input type="fieldn" id="fieldn" class="form-control" />
        </div>
        <br>

        <div class="form-outline mb-4">
          <input type="fieldp" id="fieldp" class="form-control" />
        </div>
        <br>

        <div class="form-outline mb-4">
          <button type="submit" class="btn btn-primary btn-block">
            Submit
          </button>
        </div>
      </form>
    </div>
  </body>
</html>
"""


@functions_framework.http
def form(_):
    return FORM_HTML
