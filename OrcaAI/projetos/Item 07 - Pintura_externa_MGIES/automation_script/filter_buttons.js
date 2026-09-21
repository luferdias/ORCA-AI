const fs = require('fs');
const buttons = JSON.parse(fs.readFileSync('budget_buttons.json', 'utf8'));
const filtered = buttons.filter(b => 
  (b.class && (b.class.includes('add_item_end') || b.class.includes('add_phase_end'))) ||
  (b.id && (b.id.includes('add_item_end') || b.id.includes('add_phase_end')))
);
fs.writeFileSync('filtered_buttons.txt', JSON.stringify(filtered, null, 2));
console.log('Filtered ' + filtered.length + ' buttons.');
