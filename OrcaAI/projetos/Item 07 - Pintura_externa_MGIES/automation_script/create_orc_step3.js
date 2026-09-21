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
    
    const step3Url = 'https://app.orcafascio.com/orc/orcamentos/6a283a2310bef06fabf83ea8/set_bancos';
    console.log(`Navigating to Step 3: ${step3Url}...`);
    await page.goto(step3Url, { waitUntil: 'networkidle2' });

    console.log('Configuring Step 3 databases...');
    await page.evaluate(() => {
      // Uncheck all database checkboxes first to make sure only SINAPI and IOPES are selected
      const checkboxes = Array.from(document.querySelectorAll('input[type="checkbox"][name$="_exibir_relatorio"]'));
      checkboxes.forEach(cb => {
        cb.checked = false;
        cb.dispatchEvent(new Event('change', { bubbles: true }));
      });

      // 1. Configure SINAPI
      const sinapiCheckbox = document.querySelector('#SINAPI_exibir_relatorio');
      if (sinapiCheckbox) {
        sinapiCheckbox.checked = true;
        sinapiCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
      }
      
      const sinapiEstado = document.querySelector('#SINAPI_estado');
      if (sinapiEstado) {
        sinapiEstado.value = 'ES';
        sinapiEstado.dispatchEvent(new Event('change', { bubbles: true }));
      }

      const sinapiData = document.querySelector('#SINAPI_data');
      if (sinapiData) {
        sinapiData.value = '02/2026';
        sinapiData.dispatchEvent(new Event('change', { bubbles: true }));
      }

      // 2. Configure IOPES
      const iopesCheckbox = document.querySelector('#IOPES_exibir_relatorio');
      if (iopesCheckbox) {
        iopesCheckbox.checked = true;
        iopesCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
      }

      const iopesData = document.querySelector('#IOPES_data');
      if (iopesData) {
        iopesData.value = '12/2025';
        iopesData.dispatchEvent(new Event('change', { bubbles: true }));
      }
    });

    // Wait 1.5 seconds for UI/JS updates
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Verify selection before saving
    const step3State = await page.evaluate(() => {
      const sinapiChecked = document.querySelector('#SINAPI_exibir_relatorio')?.checked;
      const sinapiEst = document.querySelector('#SINAPI_estado')?.value;
      const sinapiDt = document.querySelector('#SINAPI_data')?.value;
      
      const iopesChecked = document.querySelector('#IOPES_exibir_relatorio')?.checked;
      const iopesDt = document.querySelector('#IOPES_data')?.value;
      
      return { sinapiChecked, sinapiEst, sinapiDt, iopesChecked, iopesDt };
    });
    console.log('Step 3 database selections:', step3State);

    console.log('Saving Step 3 / Creating Budget...');
    // Click submit button (value="Salvar")
    const submitBtn = await page.$('input[type="submit"][value="Salvar"]');
    if (submitBtn) {
      await Promise.all([
        submitBtn.click(),
        page.waitForNavigation({ waitUntil: 'networkidle2' })
      ]);
    } else {
      console.log('Submit button not found, clicking any submit...');
      await page.click('input[type="submit"]');
      await new Promise(resolve => setTimeout(resolve, 6000));
    }

    console.log('Current URL after saving:', page.url());
    fs.writeFileSync('step3_submit_html.html', await page.content());

    if (page.url().includes('set_bancos')) {
      console.log('STILL ON STEP 3 PAGE. Creation failed.');
      const errors = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('.error, .invalid, .help-block, .has-error, .text-danger, .invalid-feedback'))
          .map(el => el.innerText.trim())
          .filter(t => t.length > 0);
      });
      console.log('Errors:', errors);
    } else {
      console.log('SUCCESS! Budget fully created.');
    }

  } catch (error) {
    console.error('Error occurred:', error);
  } finally {
    await browser.close();
    console.log('Browser closed.');
  }
})();
