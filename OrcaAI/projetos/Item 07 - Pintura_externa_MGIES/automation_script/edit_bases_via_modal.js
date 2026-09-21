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
    
    const budgetUrl = 'https://app.orcafascio.com/orc/orcamentos/6a283a2310bef06fabf83ea8';
    console.log(`Navigating to budget dashboard: ${budgetUrl}...`);
    await page.goto(budgetUrl, { waitUntil: 'networkidle2' });

    console.log('Opening database modal and filling values...');
    await page.evaluate(() => {
      // 1. Open the modal by adding class or triggering click on the modal link
      const modalLink = document.querySelector('a[href="#modal-edit-bases"]');
      if (modalLink) modalLink.click();

      // 2. Configure databases inside #modal-edit-bases
      // SINAPI (ES) 02/2026
      const sinapiCheckbox = document.querySelector('#modal-edit-bases #SINAPI_exibir_relatorio');
      if (sinapiCheckbox) {
        sinapiCheckbox.checked = true;
        sinapiCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
      }
      const sinapiEstado = document.querySelector('#modal-edit-bases #SINAPI_estado');
      if (sinapiEstado) {
        sinapiEstado.value = 'ES';
        sinapiEstado.dispatchEvent(new Event('change', { bubbles: true }));
      }
      const sinapiData = document.querySelector('#modal-edit-bases #SINAPI_data');
      if (sinapiData) {
        sinapiData.value = '02/2026';
        sinapiData.dispatchEvent(new Event('change', { bubbles: true }));
      }

      // IOPES (ES) 12/2025
      const iopesCheckbox = document.querySelector('#modal-edit-bases #IOPES_exibir_relatorio');
      if (iopesCheckbox) {
        iopesCheckbox.checked = true;
        iopesCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
      }
      const iopesData = document.querySelector('#modal-edit-bases #IOPES_data');
      if (iopesData) {
        iopesData.value = '12/2025';
        iopesData.dispatchEvent(new Event('change', { bubbles: true }));
      }

      // ORSE (SE) 12/2025
      const orseCheckbox = document.querySelector('#modal-edit-bases #ORSE_exibir_relatorio');
      if (orseCheckbox) {
        orseCheckbox.checked = true;
        orseCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
      }
      const orseData = document.querySelector('#modal-edit-bases #ORSE_data');
      if (orseData) {
        orseData.value = '12/2025';
        orseData.dispatchEvent(new Event('change', { bubbles: true }));
      }

      // EMOP (RJ) 02/2026
      const emopCheckbox = document.querySelector('#modal-edit-bases #EMOP_exibir_relatorio');
      if (emopCheckbox) {
        emopCheckbox.checked = true;
        emopCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
      }
      const emopData = document.querySelector('#modal-edit-bases #EMOP_data');
      if (emopData) {
        emopData.value = '02/2026';
        emopData.dispatchEvent(new Event('change', { bubbles: true }));
      }

      // SBC (ES) 03/2026
      const sbcCheckbox = document.querySelector('#modal-edit-bases #SBC_exibir_relatorio');
      if (sbcCheckbox) {
        sbcCheckbox.checked = true;
        sbcCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
      }
      const sbcEstado = document.querySelector('#modal-edit-bases #SBC_estado');
      if (sbcEstado) {
        sbcEstado.value = 'VTA'; // Vitória - ES
        sbcEstado.dispatchEvent(new Event('change', { bubbles: true }));
      }
      const sbcData = document.querySelector('#modal-edit-bases #SBC_data');
      if (sbcData) {
        sbcData.value = '03/2026';
        sbcData.dispatchEvent(new Event('change', { bubbles: true }));
      }
    });

    // Wait a bit
    await new Promise(resolve => setTimeout(resolve, 1500));

    console.log('Submitting the database modal form...');
    await Promise.all([
      page.click('#submit_button_bases'),
      page.waitForNavigation({ waitUntil: 'networkidle2' })
    ]);

    console.log('Reloaded page URL:', page.url());
    
    // Dump text to verify active databases
    const text = await page.evaluate(() => document.body.innerText);
    fs.writeFileSync('budget_dashboard_text_after_modal.txt', text);
    console.log('Saved budget_dashboard_text_after_modal.txt');

  } catch (error) {
    console.error('Error occurred:', error);
  } finally {
    await browser.close();
    console.log('Browser closed.');
  }
})();
