const puppeteer = require('puppeteer-core');
const fs = require('fs');

(async () => {
  console.log('Launching Chrome...');
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  
  try {
    console.log('Navigating to Orçafascio login page...');
    await page.goto('https://app.orcafascio.com/', { waitUntil: 'networkidle2' });
    
    console.log('Current URL:', page.url());
    
    console.log('Filling email and password...');
    await page.type('input[name="email"]', 'mgi.sra-es.serl@gestao.gov.br');
    await page.type('input[name="senha"]', 'SRAES@2025');
    
    console.log('Clicking login button...');
    await Promise.all([
      page.click('button[type="submit"]'),
      page.waitForNavigation({ waitUntil: 'networkidle2' })
    ]);
    
    console.log('Login successful! Current URL:', page.url());
    
    // Let's dump some page structure to understand where we are
    const bodyText = await page.evaluate(() => document.body.innerText);
    console.log('Body text length:', bodyText.length);
    fs.writeFileSync('dashboard_text.txt', bodyText);
    
    // Let's list some links or buttons
    const elements = await page.evaluate(() => {
      const links = Array.from(document.querySelectorAll('a')).map(a => ({ text: a.innerText.trim(), href: a.href }));
      const buttons = Array.from(document.querySelectorAll('button')).map(b => ({ text: b.innerText.trim() }));
      return { links, buttons };
    });
    
    console.log('Found links:', elements.links.slice(0, 20));
    console.log('Found buttons:', elements.buttons.slice(0, 20));
    
  } catch (error) {
    console.error('Error occurred:', error);
  } finally {
    await browser.close();
    console.log('Browser closed.');
  }
})();
