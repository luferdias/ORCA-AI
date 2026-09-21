const puppeteer = require('puppeteer-core');

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

    console.log('Configuring all required databases...');
    await page.evaluate(() => {
      // Uncheck all first
      const checkboxes = Array.from(document.querySelectorAll('input[type="checkbox"][name$="_exibir_relatorio"]'));
      checkboxes.forEach(cb => {
        cb.checked = false;
        cb.dispatchEvent(new Event('change', { bubbles: true }));
      });

      // 1. SINAPI (ES) 02/2026
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

      // 2. IOPES (ES) 12/2025
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

      // 3. ORSE (SE) 12/2025
      const orseCheckbox = document.querySelector('#ORSE_exibir_relatorio');
      if (orseCheckbox) {
        orseCheckbox.checked = true;
        orseCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
      }
      const orseData = document.querySelector('#ORSE_data');
      if (orseData) {
        orseData.value = '12/2025';
        orseData.dispatchEvent(new Event('change', { bubbles: true }));
      }

      // 4. EMOP (RJ) 02/2026
      const emopCheckbox = document.querySelector('#EMOP_exibir_relatorio');
      if (emopCheckbox) {
        emopCheckbox.checked = true;
        emopCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
      }
      const emopData = document.querySelector('#EMOP_data');
      if (emopData) {
        emopData.value = '02/2026';
        emopData.dispatchEvent(new Event('change', { bubbles: true }));
      }

      // 5. SBC (ES) 03/2026
      const sbcCheckbox = document.querySelector('#SBC_exibir_relatorio');
      if (sbcCheckbox) {
        sbcCheckbox.checked = true;
        sbcCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
      }
      const sbcEstado = document.querySelector('#SBC_estado');
      if (sbcEstado) {
        sbcEstado.value = 'VTA'; // Vitória - ES
        sbcEstado.dispatchEvent(new Event('change', { bubbles: true }));
      }
      const sbcData = document.querySelector('#SBC_data');
      if (sbcData) {
        sbcData.value = '03/2026';
        sbcData.dispatchEvent(new Event('change', { bubbles: true }));
      }
    });

    await new Promise(resolve => setTimeout(resolve, 1500));

    console.log('Saving Database Settings...');
    const submitBtn = await page.$('input[type="submit"][value="Salvar"]');
    await Promise.all([
      submitBtn.click(),
      page.waitForNavigation({ waitUntil: 'networkidle2' })
    ]);

    console.log('Database settings saved! Current URL:', page.url());

  } catch (error) {
    console.error('Error occurred:', error);
  } finally {
    await browser.close();
    console.log('Browser closed.');
  }
})();
