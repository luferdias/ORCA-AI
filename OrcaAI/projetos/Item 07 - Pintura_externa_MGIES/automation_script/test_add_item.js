const puppeteer = require('puppeteer-core');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
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
    
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Check visible modals or inputs
    const visibleElements = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('input:not([type="hidden"]), select, textarea, button')).map(el => {
        if (el.offsetWidth > 0 || el.offsetHeight > 0) {
          return {
            tag: el.tagName.toLowerCase(),
            id: el.id,
            class: el.className,
            name: el.name,
            placeholder: el.placeholder || '',
            text: el.innerText || el.value || ''
          };
        }
        return null;
      }).filter(x => x !== null);
    });
    console.log('Visible elements after clicking Add Composição:');
    console.log(JSON.stringify(visibleElements, null, 2));

    // Also let's save the HTML chunk around the new item row
    const html = await page.content();
    fs.writeFileSync('after_add_item_click.html', html);

  } catch (err) {
    console.error(err);
  } finally {
    await browser.close();
  }
})();
