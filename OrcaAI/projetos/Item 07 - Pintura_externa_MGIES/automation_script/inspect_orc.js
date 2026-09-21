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
  
  try {
    console.log('Navigating to login page...');
    await page.goto('https://app.orcafascio.com/', { waitUntil: 'networkidle2' });
    await page.type('input[name="email"]', 'mgi.sra-es.serl@gestao.gov.br');
    await page.type('input[name="senha"]', 'SRAES@2025');
    await Promise.all([
      page.click('button[type="submit"]'),
      page.waitForNavigation({ waitUntil: 'networkidle2' })
    ]);
    
    console.log('Login successful! Navigating to Lista de Orçamentos...');
    await page.goto('https://app.orcafascio.com/orc/orcamentos', { waitUntil: 'networkidle2' });
    
    console.log('Current URL:', page.url());
    
    const bodyText = await page.evaluate(() => document.body.innerText);
    fs.writeFileSync('orcamentos_text.txt', bodyText);
    console.log('Saved page text.');

    // Let's dump all folders and buttons
    const folders = await page.evaluate(() => {
      const links = Array.from(document.querySelectorAll('a')).map(a => ({
        text: a.innerText.trim(),
        href: a.href,
        class: a.className,
        id: a.id
      }));
      return { links };
    });
    
    fs.writeFileSync('folders.json', JSON.stringify(folders, null, 2));
    console.log('Saved folders and links list.');
    
  } catch (error) {
    console.error('Error occurred:', error);
  } finally {
    await browser.close();
    console.log('Browser closed.');
  }
})();
