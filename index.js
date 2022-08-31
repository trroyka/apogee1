let select = document.querySelector('#request__input_4');


let data = `"Afghanistan"
"South Africa (Republic of)"
"Marion Island"
"Angola (Republic of)"
"Albania (Republic of)"`
   
let fileRows = data.toString().replace(/"/g , '').split('\n');

for (let i=0; i < fileRows.length; i++) {
 select.options[i+1] = new Option( `${fileRows[i]}`, `${fileRows[i]}`, false, false)
}
console.log(fileRows);
