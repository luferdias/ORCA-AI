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
    
    console.log('Navigating to New Budget form...');
    await page.goto('https://app.orcafascio.com/orc/orcamentos/new?pasta_id=673b98fc859a024057c5dab7', { waitUntil: 'networkidle2' });
    
    console.log('Filling form step 1...');
    // Select version 2023 radio button
    await page.click('#orc_orcamento_version_2023_true');
    
    // Clear code and type custom code
    await page.click('#orc_orcamento_codigo', { clickCount: 3 });
    await page.keyboard.press('Backspace');
    await page.type('#orc_orcamento_codigo', 'SRAES-PINTURA-TESTE');
    
    // Fill description
    await page.type('#orc_orcamento_descricao', 'Pintura MGI/SRA-ES - Teste Reorganizado');
    
    console.log('Submitting Step 1...');
    await Promise.all([
      page.click('#check-btn'),
      page.waitForNavigation({ waitUntil: 'networkidle2' })
    ]);
    
    console.log('Submitted! Current URL:', page.url());
    
    const bodyText = await page.evaluate(() => document.body.innerText);
    fs.writeFileSync('new_orc_step2_text.txt', bodyText);
    console.log('Saved step 2 text.');
    
    // Let's dump all inputs of step 2
    const inputs2 = await page.evaluate(() => {
      const inputFields = Array.from(document.querySelectorAll('input, select, textarea')).map(el => {
        let labelText = '';
        if (el.id) {
          const lbl = document.querySelector(`label[for="${el.id}"]`);
          if (lbl) labelText = lbl.innerText.trim();
        }
        if (!labelText) {
          const parentLabel = el.closest('label');
          if (parentLabel) labelText = parentLabel.innerText.trim();
        }
        return {
          tag: el.tagName.toLowerCase(),
          name: el.name,
          id: el.id,
          type: el.type,
          value: el.value,
          labelText: labelText
        };
      });
      return inputFields;
    });
    
    fs.writeFileSync('step2_inputs.json', JSON.stringify(inputs2, null, 2));
    console.log('Saved step 2 inputs list.');
    
  } catch (error) {
    console.error('Error occurred:', error);
  } finally {
    await browser.close();
    console.log('Browser closed.');
  }
})();
