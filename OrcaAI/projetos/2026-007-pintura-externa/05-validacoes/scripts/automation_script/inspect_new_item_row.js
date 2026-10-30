const fs = require('fs');
const html = fs.readFileSync('after_add_item_click.html', 'utf8');

const pos = html.indexOf('item_autocomplete_code');
if (pos !== -1) {
  console.log('--- HTML around item_autocomplete_code ---');
  console.log(html.substring(pos - 500, pos + 1500));
} else {
  console.log('item_autocomplete_code not found');
}
