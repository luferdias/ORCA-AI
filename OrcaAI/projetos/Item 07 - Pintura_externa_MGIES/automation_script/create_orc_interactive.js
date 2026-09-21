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

  // Route page console logs to Node process console
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
    
    console.log('Navigating directly to New Budget form...');
    await page.goto('https://app.orcafascio.com/orc/orcamentos/new?pasta_id=673b98fc859a024057c5dab7', { waitUntil: 'networkidle2' });
    
    console.log('Selecting new version option (2023)...');
    await page.click('#orc_orcamento_version_2023_true');
    // Wait a brief moment to see if clicking version radio triggers page load or dynamic shifts
    await new Promise(resolve => setTimeout(resolve, 1500));

    console.log('Clearing and entering Code...');
    // Focus the input, select all, delete, and type
    const codeInput = await page.$('#orc_orcamento_codigo');
    await codeInput.click({ clickCount: 3 });
    await page.keyboard.press('Backspace');
    const uniqueCode = `SRAES-PINTURA-${Date.now()}`;
    console.log('Unique code generated:', uniqueCode);
    await codeInput.type(uniqueCode);

    console.log('Entering Description...');
    await page.type('#orc_orcamento_descricao', 'Pintura MGI/SRA-ES - Teste Reorganizado');

    console.log('Selecting Category...');
    // We select the "Prédios públicos - Reforma" category
    await page.select('#standard-category', 'Prédios públicos - Reforma');
    
    // Check if we need to fill anything else. Let's dump current values of form to confirm they are set
    const formState = await page.evaluate(() => {
      const code = document.querySelector('#orc_orcamento_codigo') ? document.querySelector('#orc_orcamento_codigo').value : null;
      const desc = document.querySelector('#orc_orcamento_descricao') ? document.querySelector('#orc_orcamento_descricao').value : null;
      const cat = document.querySelector('#standard-category') ? document.querySelector('#standard-category').value : null;
      const ver = document.querySelector('#orc_orcamento_version_2023_true') ? document.querySelector('#orc_orcamento_version_2023_true').checked : null;
      return { code, desc, cat, ver };
    });
    console.log('Form state before submit:', formState);

    console.log('Submitting Step 1 form...');
    await page.click('#check-btn');

    console.log('Waiting 6 seconds for navigation or errors...');
    await new Promise(resolve => setTimeout(resolve, 6000));

    console.log('URL after submission:', page.url());

    // Check if there are error messages on the screen
    const errors = await page.evaluate(() => {
      // Find all error messages or highlighted fields
      const errorMsgs = Array.from(document.querySelectorAll('.error, .invalid, .help-block, .has-error, .text-danger, .invalid-feedback'))
        .map(el => el.innerText.trim())
        .filter(t => t.length > 0);
      
      const inlineErrors = Array.from(document.querySelectorAll('.form-group.has-error, .field_with_errors'))
        .map(el => el.innerText.trim());

      return { errorMsgs, inlineErrors };
    });

    console.log('Errors found on page:', errors);

    if (page.url().includes('/orc/orcamentos/new')) {
      console.log('STILL ON STEP 1 PAGE. Submission failed.');
      // Write the full body innerHTML for offline debugging
      fs.writeFileSync('step1_fail_html.html', await page.content());
    } else {
      console.log('SUCCESS! Moved past Step 1.');
      console.log('Saving new inputs for Step 2...');
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
