const fs = require('fs');
const text = fs.readFileSync('budget_dashboard_text_after_modal.txt', 'utf8');

const check = (term) => {
  const idx = text.indexOf(term);
  if (idx !== -1) {
    console.log(`Found "${term}" at index ${idx}:`);
    console.log(text.substring(idx - 100, idx + 100));
  } else {
    console.log(`"${term}" NOT found`);
  }
};

check('ORSE');
check('EMOP');
check('SBC');
check('IOPES');
check('SINAPI');
