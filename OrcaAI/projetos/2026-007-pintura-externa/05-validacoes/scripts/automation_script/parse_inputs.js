const fs = require('fs');
const html = fs.readFileSync('after_add_item_click.html', 'utf8');

// Let's find the table row or container where items are added.
// Usually, there is a class or text that says "salvar" or "cancelar" or "add_item" or "input_code".
// Let's find the index of "input_code" and get 5000 characters before and after it.
const pos = html.indexOf('input_code');
if (pos !== -1) {
  const segment = html.substring(Math.max(0, pos - 1500), Math.min(html.length, pos + 2500));
  fs.writeFileSync('item_row_segment.html', segment);
  console.log('Saved segment of HTML to item_row_segment.html');
  
  // Also extract all tags in this segment
  const tags = [];
  const tagRegex = /<([a-z1-6]+)([^>]*)>/gi;
  let match;
  while ((match = tagRegex.exec(segment)) !== null) {
    const tagName = match[1].toLowerCase();
    const attrs = match[2];
    if (['input', 'select', 'button', 'a'].includes(tagName)) {
      tags.push(`<${tagName}${attrs}>`);
    }
  }
  fs.writeFileSync('item_row_tags.txt', tags.join('\n'));
  console.log('Saved tags list to item_row_tags.txt');
} else {
  console.log('input_code not found in HTML');
}
