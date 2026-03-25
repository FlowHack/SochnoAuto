const urlGetSpecialOffers = `${indexURL}api/v1/special-offers/`;
const divPaginationSpecialOffers = document.getElementById('divPaginationSpecialOffers');
const divSpecialOffers = document.getElementById('mainBlockSpecialOffers');

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
}

function formatMileage(mileage) {
    return mileage.toLocaleString('ru-RU');
}

Handlebars.registerHelper('gt', (a, b) => a > b);

function prepareCarData(car) {
    return {
        ...car,
        type_transmission_display: (car.type_transmission || '').toUpperCase(),
        price_formatted: formatNumber(car.price),
        mileage_formatted: formatMileage(car.mileage)
    };
}

const Templates = {
    carCard: null,
    pagination: null,
    emptyState: null,
    loaded: false
};

async function loadTemplates() {
    if (Templates.loaded) return;

    const basePath = '/static/templates/homepage/';
    const templateNames = [
        'handlebars_special_offer_card.hbs',
        'handlebars_special_offer_pagination.hbs',
        'handlebars_special_offer_empty.hbs'
    ];

    const [cardHtml, paginationHtml, emptyHtml] = await Promise.all(
        templateNames.map(name => fetch(`${basePath}${name}`).then(r => r.text()))
    );

    Templates.carCard = Handlebars.compile(cardHtml);
    Templates.pagination = Handlebars.compile(paginationHtml);
    Templates.emptyState = Handlebars.compile(emptyHtml);
    Templates.loaded = true;
}

async function replaceSpecialOffers(element) {
    await loadTemplates();

    const page = Number(element.getAttribute('data-page'));

    const response = await fetch(
        `${urlGetSpecialOffers}?special_offers_page=${page}`,
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }
    );

    if (!response.ok) {
        console.error('Failed to fetch special offers:', response.status);
        return;
    }

    const data = await response.json();
    const offers = data.page?.object_list || [];
    const hasPages = data.has_pages;

    if (offers.length > 0) {
        const preparedOffers = offers.map(prepareCarData);
        divSpecialOffers.innerHTML = Templates.carCard(preparedOffers);
        
        divPaginationSpecialOffers.innerHTML = Templates.pagination({
            prev_page: hasPages?.has_previous ? page - 1 : '',
            next_page: hasPages?.has_next ? page + 1 : '',
            hide_prev: !hasPages?.has_previous,
            hide_next: !hasPages?.has_next
        });
    } else {
        divSpecialOffers.innerHTML = Templates.emptyState();
        divPaginationSpecialOffers.innerHTML = '';
    }

    setTimeout(() => {
        const section = document.getElementById('special-offers-section');
        if (section) {
            section.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }, 100);
}

loadTemplates();