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
    
    const step2Url = 'https://app.orcafascio.com/orc/orcamentos/6a283a2310bef06fabf83ea8/new_passo_2';
    console.log(`Navigating to Step 2: ${step2Url}...`);
    await page.goto(step2Url, { waitUntil: 'networkidle2' });

    console.log('Configuring Step 2 inputs...');
    await page.evaluate(() => {
      // 1. Select Desonerado radio button
      const desoneradoRadio = document.querySelector('#orc_orcamento_desonerado_true');
      if (desoneradoRadio) {
        desoneradoRadio.checked = true;
        desoneradoRadio.dispatchEvent(new Event('change', { bubbles: true }));
      } else {
        console.log('Desonerado radio not found!');
      }

      // 2. Check BDI manual checkbox
      const manualBdiCheckbox = document.querySelector('#checkbox_bdi_manual');
      if (manualBdiCheckbox) {
        manualBdiCheckbox.checked = true;
        manualBdiCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
        
        // Show manual input if dynamic JS is triggered
        const manualInput = document.querySelector('#input_bdi_manual');
        if (manualInput) {
          manualInput.value = '25,00';
          manualInput.dispatchEvent(new Event('input', { bubbles: true }));
          manualInput.dispatchEvent(new Event('change', { bubbles: true }));
        } else {
          console.log('Manual BDI text input not found!');
        }
      } else {
        console.log('Manual BDI checkbox not found!');
      }
    });

    // Wait a brief moment to let UI update
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Log selected states to verify they were set in DOM
    const step2State = await page.evaluate(() => {
      const desonerado = document.querySelector('#orc_orcamento_desonerado_true')?.checked;
      const bdiChecked = document.querySelector('#checkbox_bdi_manual')?.checked;
      const bdiValue = document.querySelector('#input_bdi_manual')?.value;
      return { desonerado, bdiChecked, bdiValue };
    });
    console.log('Step 2 state before submit:', step2State);

    console.log('Submitting Step 2...');
    // Click submit button
    const submitBtn = await page.$('input[type="submit"][value="Próximo"]');
    if (submitBtn) {
      await Promise.all([
        submitBtn.click(),
        page.waitForNavigation({ waitUntil: 'networkidle2' })
      ]);
    } else {
      console.log('Submit button not found, trying check-btn or regular click...');
      await page.click('input[type="submit"]');
      await new Promise(resolve => setTimeout(resolve, 5000));
    }

    console.log('Current URL after submit:', page.url());
    fs.writeFileSync('step2_submit_html.html', await page.content());

    if (page.url().includes('new_passo_2')) {
      console.log('STILL ON STEP 2 PAGE. Submission failed.');
      const errors = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('.error, .invalid, .help-block, .has-error, .text-danger, .invalid-feedback'))
          .map(el => el.innerText.trim())
          .filter(t => t.length > 0);
      });
      console.log('Errors:', errors);
    } else {
      console.log('SUCCESS! Redirected to Step 3.');
      // Dump inputs of Step 3
      const inputs3 = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('input, select, textarea, button')).map(el => {
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
            labelText: labelText,
            class: el.className,
            text: el.innerText
          };
        });
      });
      fs.writeFileSync('step3_inputs.json', JSON.stringify(inputs3, null, 2));
      console.log('Saved step 3 inputs to step3_inputs.json');
    }

  } catch (error) {
    console.error('Error occurred:', error);
  } finally {
    await browser.close();
    console.log('Browser closed.');
  }
})();
