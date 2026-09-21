const fs = require('fs');
const html = fs.readFileSync('after_add_phase_click.html', 'utf8');

// Search for input_descr in HTML and print its surrounding structure
const idx = html.indexOf('input_descr');
if (idx !== -1) {
  console.log('--- HTML around input_descr ---');
  console.log(html.substring(idx - 500, idx + 1000));
} else {
  console.log('input_descr not found');
}
