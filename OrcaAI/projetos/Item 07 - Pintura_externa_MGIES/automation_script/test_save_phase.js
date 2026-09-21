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

    console.log('Clicking Adicionar Etapa...');
    await page.click('a.add_phase_end');
    await new Promise(resolve => setTimeout(resolve, 1500));

    console.log('Filling stage details...');
    await page.evaluate(() => {
      const itemInput = document.querySelector('input.input_itemization');
      const descInput = document.querySelector('input.input_descr');
      const qtyInput = document.querySelector('input.input_qty');

      if (itemInput) {
        itemInput.value = '1';
        itemInput.dispatchEvent(new Event('input', { bubbles: true }));
      }
      if (descInput) {
        descInput.value = '1. SERVIÇOS PRELIMINARES E APOIO OPERACIONAL DAS TRÊS FRENTES';
        descInput.dispatchEvent(new Event('input', { bubbles: true }));
      }
      if (qtyInput) {
        qtyInput.value = '1';
        qtyInput.dispatchEvent(new Event('input', { bubbles: true }));
      }
    });

    console.log('Clicking salvar_new_etapa...');
    await page.click('a.salvar_new_etapa');
    
    console.log('Waiting 4 seconds...');
    await new Promise(resolve => setTimeout(resolve, 4000));

    const text = await page.evaluate(() => document.body.innerText);
    fs.writeFileSync('after_save_phase.txt', text);
    console.log('Saved after_save_phase.txt');

    if (text.includes('SERVIÇOS PRELIMINARES')) {
      console.log('SUCCESS: Stage "1. SERVIÇOS PRELIMINARES" successfully saved!');
    } else {
      console.log('FAIL: Stage not found in page text.');
    }

  } catch (err) {
    console.error(err);
  } finally {
    await browser.close();
  }
})();
