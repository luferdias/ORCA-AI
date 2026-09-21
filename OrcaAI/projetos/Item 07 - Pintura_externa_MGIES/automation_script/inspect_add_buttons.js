const fs = require('fs');
const buttons = JSON.parse(fs.readFileSync('budget_buttons.json', 'utf8'));

const matches = buttons.filter(b => 
  (b.text && (b.text.includes('Etapa') || b.text.includes('Composi') || b.text.includes('Insumo'))) ||
  (b.class && (b.class.includes('phase') || b.class.includes('item') || b.class.includes('comp'))) ||
  (b.id && (b.id.includes('phase') || b.id.includes('item') || b.id.includes('comp')))
);

console.log(JSON.stringify(matches, null, 2));
