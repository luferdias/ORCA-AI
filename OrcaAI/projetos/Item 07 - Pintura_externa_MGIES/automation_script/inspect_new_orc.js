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
    
    console.log('Navigating directly to New Budget form under Espírito Santo folder...');
    await page.goto('https://app.orcafascio.com/orc/orcamentos/new?pasta_id=673b98fc859a024057c5dab7', { waitUntil: 'networkidle2' });
    
    console.log('New Budget Form URL:', page.url());
    
    const bodyText = await page.evaluate(() => document.body.innerText);
    fs.writeFileSync('new_orc_form_text.txt', bodyText);
    console.log('Saved form page text.');
    
    // Let's list all input fields, selects, and textareas on the form
    const inputs = await page.evaluate(() => {
      const inputFields = Array.from(document.querySelectorAll('input, select, textarea')).map(el => {
        // Find label
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
          placeholder: el.placeholder,
          labelText: labelText
        };
      });
      return inputFields;
    });
    
    fs.writeFileSync('form_inputs.json', JSON.stringify(inputs, null, 2));
    console.log('Saved form inputs list.');
    
  } catch (error) {
    console.error('Error occurred:', error);
  } finally {
    await browser.close();
    console.log('Browser closed.');
  }
})();
