const fs = require('fs');
const html = fs.readFileSync('budget_dashboard_after_submit.html', 'utf8');

let pos = html.indexOf('Bancos');
while (pos !== -1) {
  console.log(`\nMatch at position ${pos}:`);
  console.log(html.substring(pos - 50, pos + 300));
  pos = html.indexOf('Bancos', pos + 1);
}
