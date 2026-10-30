const fs = require('fs');
const html = fs.readFileSync('budget_dashboard.html', 'utf8');

const parseSelectOptions = (id) => {
  const startIdx = html.indexOf(`id="${id}"`);
  if (startIdx === -1) return [];
  const chunk = html.substring(startIdx, startIdx + 20000);
  const endSelect = chunk.indexOf('</select>');
  if (endSelect === -1) return [];
  const selectHtml = chunk.substring(0, endSelect);
  const regex = /<option[^>]*value="([^"]*)"[^>]*>([^<]*)<\/option>/gi;
  let match;
  const options = [];
  while ((match = regex.exec(selectHtml)) !== null) {
    options.push({ value: match[1], text: match[2].trim() });
  }
  return options;
};

const ids = [
  'SINAPI_estado', 'SINAPI_data',
  'IOPES_data',
  'ORSE_data',
  'EMOP_data',
  'SBC_estado', 'SBC_data'
];

const results = {};
for (const id of ids) {
  results[id] = parseSelectOptions(id);
}

fs.writeFileSync('select_options.json', JSON.stringify(results, null, 2));
console.log('Saved select_options.json');
for (const id of ids) {
  console.log(`\nOptions for ${id}:`, results[id].slice(0, 10), results[id].length > 10 ? `... total ${results[id].length}` : '');
}
