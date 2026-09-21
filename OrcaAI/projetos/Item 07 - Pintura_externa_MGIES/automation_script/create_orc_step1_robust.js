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
    const uniqueCode = `SRAES-PINTURA-${Date.now()}`;
    console.log('Using unique code:', uniqueCode);
    await page.type('#orc_orcamento_codigo', uniqueCode);
    
    // Fill description
    await page.type('#orc_orcamento_descricao', 'Pintura MGI/SRA-ES - Teste Reorganizado');
    
    // Get all category option values
    const categoryOptions = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('#standard-category option')).map(o => ({
        text: o.innerText.trim(),
        value: o.value
      }));
    });
    console.log('Category options:', categoryOptions);
    
    // Select the category option that matches 'Prédios públicos - Reforma' or similar
    const reformOption = categoryOptions.find(o => o.text.includes('Prédios públicos - Reforma'));
    if (reformOption) {
      console.log('Selecting category:', reformOption.value);
      await page.select('#standard-category', reformOption.value);
    } else {
      console.log('Reforma option not found, selecting the second option:', categoryOptions[1].value);
      await page.select('#standard-category', categoryOptions[1].value);
    }
    
    console.log('Submitting Step 1...');
    await page.click('#check-btn');
    
    console.log('Waiting for 5 seconds to allow submission processing...');
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    console.log('Current URL after submit:', page.url());
    
    const bodyText = await page.evaluate(() => document.body.innerText);
    fs.writeFileSync('step1_submit_text.txt', bodyText);
    
    // If we are still on the form page, dump validation errors
    if (page.url().includes('/orc/orcamentos/new')) {
      console.log('Validation failed or page did not redirect. Check step1_submit_text.txt');
    } else {
      console.log('Redirected successfully!');
      
      // Let's dump all inputs of the new page (step 2)
      const inputs2 = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('input, select, textarea')).map(el => {
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
      });
      fs.writeFileSync('step2_inputs.json', JSON.stringify(inputs2, null, 2));
      console.log('Saved step 2 inputs to step2_inputs.json');
    }
    
  } catch (error) {
    console.error('Error occurred:', error);
  } finally {
    await browser.close();
    console.log('Browser closed.');
  }
})();
