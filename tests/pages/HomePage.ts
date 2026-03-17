import { Page, Locator } from '@playwright/test';

/**
 * Representa a Página Inicial do Portfólio.
 * Concentra todos os seletores e ações específicas desta página.
 */
export class HomePage {
    readonly page: Page;
    readonly langToggleBtn: Locator;
    readonly headerTitle: Locator;
    readonly headerSubtitle: Locator;
    readonly cvDownloadBtn: Locator;
    readonly contactNameLabel: Locator;

    constructor(page: Page) {
        this.page = page;

        // Botão de tradução
        this.langToggleBtn = page.locator('#lang-toggle');

        // Elementos com suporte a i18n
        this.headerTitle = page.locator('h1[data-i18n="header-title"]');
        this.headerSubtitle = page.locator('#subtitle[data-i18n="header-subtitle"]');
        this.cvDownloadBtn = page.locator('#download-resume-btn');

        // Um pedaço do formulário de contato para confirmar
        this.contactNameLabel = page.locator('label[data-i18n="contact-form-name"]');
    }

    /** Navega para a página principal */
    async navigate() {
        await this.page.goto('http://127.0.0.1:5000');
    }

    /** Altera o idioma clicando no toggle */
    async toggleLanguage() {
        await this.langToggleBtn.click();
    }
}
