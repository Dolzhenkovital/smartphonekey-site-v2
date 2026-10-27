{
    'name': 'SmartphoneKey Website 2.0',
    'version': '18.0.3.0.0',
    'summary': 'smartphonekey.com 2.0: the access control management platform site, '
               'setup guide, compatibility centre and CRM enquiries',
    'category': 'Website/Website',
    'author': 'SmartphoneKey',
    'website': 'https://smartphonekey.com',
    'license': 'LGPL-3',
    'depends': [
        # AP-428/AP-429 baseline: the Webflow port, its homepage switch, the
        # retained URLs this module takes over and the site-form captcha check.
        'spk_website',
        'website_crm',
    ],
    'data': [
        'security/spk_website_v2_security.xml',
        'security/ir.model.access.csv',
        'data/website_claims.xml',
        'data/website_compatibility.xml',
        'data/website_resources.xml',
        'data/website_posts.xml',
        'data/website_team.xml',
        'views/layout.xml',
        'views/components.xml',
        'views/home.xml',
        'views/platform.xml',
        'views/solutions.xml',
        'views/products.xml',
        'views/resources.xml',
        'views/setup.xml',
        'views/contact.xml',
        'views/company.xml',
        'views/legal_pages.xml',
        'views/backend_content.xml',
        'views/crm_lead_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'assets': {
        # CSS only, like the baseline: the pages are bare web.layout documents
        # and load their three small scripts as raw deferred <script> tags.
        'spk_website_v2.assets_site': [
            'spk_website_v2/static/src/scss/site.scss',
        ],
    },
}
