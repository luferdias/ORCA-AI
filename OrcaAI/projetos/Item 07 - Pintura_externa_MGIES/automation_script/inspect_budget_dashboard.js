const puppeteer = require('puppeteer-core');
const fs = require('fs');

(async () => {
  console.log('Launching Chrome...');
  const browser = await puppeteer.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();

  page.on('console', msg => console.log('BROWSER LOG:', msg.text()));
  page.on('pageerror', err => console.log('BROWSER EXCEPTION:', err.toString()));

  try {
    console.log('Navigating to login page...');
    await page.goto('https://app.orcafascio.com/', { waitUntil: 'networkidle2' });
    await page.type('input[name="email"]', 'mgi.sra-es.serl@gestao.gov.br');
    await page.type('input[name="senha"]', 'SRAES@2025');
    await Promise.all([
      page.click('button[type="submit"]'),
      page.waitForNavigation({ waitUntil: 'networkidle2' })
    ]);
    
    const budgetUrl = 'https://app.orcafascio.com/orc/orcamentos/6a283a2310bef06fabf83ea8';
    console.log(`Navigating to budget dashboard: ${budgetUrl}...`);
    await page.goto(budgetUrl, { waitUntil: 'networkidle2' });

    console.log('Dumping budget dashboard content...');
    const content = await page.content();
    fs.writeFileSync('budget_dashboard.html', content);
    
    const text = await page.evaluate(() => document.body.innerText);
    fs.writeFileSync('budget_dashboard_text.txt', text);
    
    // Dump all buttons and interactive elements in editor
    const buttons = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('button, a, input[type="button"], input[type="submit"]')).map(el => {
        return {
          tag: el.tagName.toLowerCase(),
          id: el.id,
          class: el.className,
          text: el.innerText ? el.innerText.trim() : (el.value ? el.value.trim() : ''),
          href: el.href || null
        };
      });
    });
    fs.writeFileSync('budget_buttons.json', JSON.stringify(buttons, null, 2));
    
    console.log('Current page URL:', page.url());

  } catch (error) {
    console.error('Error occurred:', error);
  } finally {
    await browser.close();
    console.log('Browser closed.');
  }
})();
