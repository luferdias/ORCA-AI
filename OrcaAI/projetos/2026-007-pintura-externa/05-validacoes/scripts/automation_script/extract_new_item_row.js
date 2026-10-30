const fs = require('fs');
const html = fs.readFileSync('after_add_item_click.html', 'utf8');

// Search for inputs or elements of class 'input_code' or similar
const searchTerms = ['input_code', 'select_input_bases', 'input_descr', 'input_qty', 'save_new_item', 'add_item_end'];
const results = {};

for (const term of searchTerms) {
  const index = html.indexOf(term);
  if (index !== -1) {
    results[term] = html.substring(Math.max(0, index - 200), Math.min(html.length, index + 600));
  } else {
    results[term] = 'NOT FOUND';
  }
}

fs.writeFileSync('extracted_elements.txt', JSON.stringify(results, null, 2));
console.log('Saved extracted_elements.txt');
