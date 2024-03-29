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
        crossorigin="anonymous">
    <title>Document</title>
  </head>
  <body>
    <style>
      .hide { position:absolute; top:-1px; left:-1px; width:1px; height:1px; }
    </style>
    <div class="container">
      <form id="myform" name="myform">
        <br><br>
        <div class="form-outline mb-4">
          <input type="text" name="fieldl" id="fieldl" class="form-control" placeholder="l"/>
        </div>
        <br>

        <div class="form-outline mb-4">
          <input type="text" name="fieldn" id="fieldn" class="form-control" placeholder="n"/>
        </div>
        <br>

        <div class="form-outline mb-4">
          <input type="text" name="fieldp" id="fieldp" class="form-control" placeholder="p"/>
        </div>
        <br>

        <div class="form-outline mb-4">
          <button class="btn btn-primary btn-block" onclick="buttonClick()"
                  id='btn'>Submit </button>
        </div>
        <div class="form-outline mb-4">
          <p style="text-align:center" id="fieldr"></p>
        </div>
      </form>

      <script type="text/javascript">
      const url = "https://us-central1-serverless-d2414.cloudfunctions.net/files";
      const btn = document.getElementById('btn');
      const fieldl = document.getElementById('fieldl');
      const fieldn = document.getElementById('fieldn');
      const fieldp = document.getElementById('fieldp');
      const fieldr = document.getElementById('fieldr');
      function buttonClick() {
        btn.disable = true;
        btn.style.opacity = "0.3";
        event.preventDefault()

        let data = JSON.stringify({
          fieldl: fieldl.value,
          fieldn: fieldn.value,
          fieldp: fieldp.value,
        })
        async function submitFields() {
          const response = await fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: data
          });
          const resp = await response.json();
          fieldl.value = "";
          fieldn.value = "";
          fieldr.innerHTML = resp.message;
        }
        submitFields();
        btn.disable = false;
        btn.style.opacity = "1.0";
      }
      </script>
    </div>
  </body>
</html>
"""


@functions_framework.http
def form(_):
    return FORM_HTML
