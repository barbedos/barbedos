const url = 'https://us-central1-serverless-d2414.cloudfunctions.net/files-test'
const btn = document.getElementById('btn')
const fieldl = document.getElementById('fieldl')
const fieldn = document.getElementById('fieldn')
const fieldp = document.getElementById('fieldp')
const fieldr = document.getElementById('fieldr')
function buttonClick () {
  btn.disable = true

  const data = JSON.stringify({
    fieldl: fieldl.value,
    fieldn: fieldn.value,
    fieldp: fieldp.value
  })
  async function submitFields () {
    const response = await fetch(url, {
      method: "POST",
      headers: {"ContentType": "application/json"},
      body: data
    });
    const resp = await response.json();
    console.log(resp);
    fieldr.value = resp.message;
  }
  submitFields();
  fieldl.value = "";
  fieldn.value = "";
  btn.disable = false;
}
