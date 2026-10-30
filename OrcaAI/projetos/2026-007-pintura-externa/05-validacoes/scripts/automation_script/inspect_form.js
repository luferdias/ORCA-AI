const fs = require('fs');
const html = fs.readFileSync('budget_dashboard.html', 'utf8');
const idx = html.indexOf('id="modal-edit-bases"');
if (idx !== -1) {
  const chunk = html.substring(idx, idx + 100000);
  const formEnd = chunk.indexOf('</form>');
  const formHtml = chunk.substring(0, formEnd + 7);
  
  // Find all buttons or inputs
  const regex = /<(button|input|a)[^>]*>([^<]*)/gi;
  let match;
  while ((match = regex.exec(formHtml)) !== null) {
    if (match[0].includes('Salvar') || match[2].includes('Salvar')) {
      console.log('Salvar element:', match[0], 'Text:', match[2]);
    }
  }
} else {
  console.log('Not found');
}
