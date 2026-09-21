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
    
    console.log('Navigating directly to New Budget form...');
    await page.goto('https://app.orcafascio.com/orc/orcamentos/new?pasta_id=673b98fc859a024057c5dab7', { waitUntil: 'networkidle2' });
    
    console.log('Filling form step 1 via robust DOM events...');
    const uniqueCode = `SRAES-PINTURA-${Date.now()}`;
    console.log('Generated code:', uniqueCode);

    await page.evaluate((code) => {
      // 1. Select the new version radio (true)
      const radio = document.querySelector('#orc_orcamento_version_2023_true');
      if (radio) {
        radio.checked = true;
        // Trigger onclick handler defined inline: onclick="showCadernoTecnicoCheckbox()"
        radio.click();
        radio.dispatchEvent(new Event('change', { bubbles: true }));
      }

      // 2. Set the code input
      const codeInput = document.querySelector('#orc_orcamento_codigo');
      if (codeInput) {
        codeInput.value = code;
        codeInput.dispatchEvent(new Event('input', { bubbles: true }));
        codeInput.dispatchEvent(new Event('change', { bubbles: true }));
      }

      // 3. Set the description
      const descInput = document.querySelector('#orc_orcamento_descricao');
      if (descInput) {
        descInput.value = 'Pintura MGI/SRA-ES - Teste Reorganizado';
        descInput.dispatchEvent(new Event('input', { bubbles: true }));
        descInput.dispatchEvent(new Event('change', { bubbles: true }));
      }

      // 4. Set category
      const categorySelect = document.querySelector('#standard-category');
      if (categorySelect) {
        categorySelect.value = 'Prédios públicos - Reforma';
        categorySelect.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }, uniqueCode);

    // Wait a brief moment
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Print state
    const formState = await page.evaluate(() => {
      const code = document.querySelector('#orc_orcamento_codigo')?.value;
      const desc = document.querySelector('#orc_orcamento_descricao')?.value;
      const cat = document.querySelector('#standard-category')?.value;
      const ver = document.querySelector('#orc_orcamento_version_2023_true')?.checked;
      const verOld = document.querySelector('#version_2023_old')?.checked;
      return { code, desc, cat, ver, verOld };
    });
    console.log('Form state before submit:', formState);

    console.log('Submitting Step 1 form...');
    await page.click('#check-btn');

    console.log('Waiting 6 seconds for navigation or errors...');
    await new Promise(resolve => setTimeout(resolve, 6000));

    console.log('URL after submission:', page.url());

    // Check if there are error messages on the screen
    const errors = await page.evaluate(() => {
      const errorMsgs = Array.from(document.querySelectorAll('.error, .invalid, .help-block, .has-error, .text-danger, .invalid-feedback'))
        .map(el => el.innerText.trim())
        .filter(t => t.length > 0);
      return { errorMsgs };
    });
    console.log('Errors found on page:', errors);

    if (page.url().includes('/orc/orcamentos/new')) {
      console.log('STILL ON STEP 1 PAGE. Submission failed.');
      fs.writeFileSync('step1_fail_html_v2.html', await page.content());
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
