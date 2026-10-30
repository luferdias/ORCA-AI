const fs = require('fs');

const html = fs.readFileSync('budget_dashboard.html', 'utf8');

// Find the modal-edit-bases div
const modalStart = html.indexOf('id="modal-edit-bases"');
if (modalStart === -1) {
  console.log('modal-edit-bases not found');
  process.exit(1);
}

// Find the closing div of the modal
// We'll just take a large chunk of HTML following the start
const chunk = html.substring(modalStart, modalStart + 100000);

// Find all inputs, selects, textareas inside this chunk before the form ends
const formEnd = chunk.indexOf('</form>');
const formHtml = chunk.substring(0, formEnd);

const regex = /<(input|select|textarea)[^>]*>/gi;
let match;
const inputs = [];

while ((match = regex.exec(formHtml)) !== null) {
  const elementHtml = match[0];
  const nameMatch = elementHtml.match(/name="([^"]+)"/i);
  const idMatch = elementHtml.match(/id="([^"]+)"/i);
  const typeMatch = elementHtml.match(/type="([^"]+)"/i);
  const valueMatch = elementHtml.match(/value="([^"]+)"/i);
  
  inputs.push({
    tag: match[1],
    name: nameMatch ? nameMatch[1] : '',
    id: idMatch ? idMatch[1] : '',
    type: typeMatch ? typeMatch[1] : '',
    value: valueMatch ? valueMatch[1] : ''
  });
}

console.log(`Found ${inputs.length} inputs in modal form:`);
console.log(JSON.stringify(inputs, null, 2));
fs.writeFileSync('modal_inputs.json', JSON.stringify(inputs, null, 2));
