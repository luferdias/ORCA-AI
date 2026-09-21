const puppeteer = require('puppeteer-core');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('BROWSER LOG:', msg.text()));
  page.on('pageerror', err => console.log('BROWSER EXCEPTION:', err.toString()));

  try {
    await page.goto('https://app.orcafascio.com/', { waitUntil: 'networkidle2' });
    await page.type('input[name="email"]', 'mgi.sra-es.serl@gestao.gov.br');
    await page.type('input[name="senha"]', 'SRAES@2025');
    await Promise.all([
      page.click('button[type="submit"]'),
      page.waitForNavigation({ waitUntil: 'networkidle2' })
    ]);
    
    const budgetUrl = 'https://app.orcafascio.com/orc/orcamentos/6a283a2310bef06fabf83ea8';
    await page.goto(budgetUrl, { waitUntil: 'networkidle2' });

    console.log('Clicking Adicionar Composição...');
    await page.click('a.add_item_end.bg-composition');
    await new Promise(resolve => setTimeout(resolve, 1500));

    console.log('Typing code into input_code...');
    // Type code '10527' into the input
    await page.type('input.input_code', '10527');
    
    console.log('Waiting for autocomplete to load...');
    await new Promise(resolve => setTimeout(resolve, 3000));

    // Check visible elements or popup items
    const popupHtml = await page.evaluate(() => {
      const menus = document.querySelectorAll('.ui-menu, .ui-autocomplete, .ui-menu-item, ul.typeahead, div.autocomplete-suggestions');
      return Array.from(menus).map(el => {
        return {
          tag: el.tagName.toLowerCase(),
          class: el.className,
          visible: el.offsetWidth > 0 || el.offsetHeight > 0,
          html: el.innerHTML
        };
      });
    });

    console.log('Popup autocomplete elements found:', popupHtml);

  } catch (err) {
    console.error(err);
  } finally {
    await browser.close();
  }
})();
