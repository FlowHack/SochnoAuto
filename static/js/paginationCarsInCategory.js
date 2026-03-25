const urlGetCarsInCategory = `${indexURL}api/v1/category/`;
const ulPaginationCars = document.getElementById('ul-pagination-cars');
const divCars = document.getElementById('cars-block');

const CarsTemplates = {
    carCard: null,
    pagination: null,
    emptyState: null,
    loaded: false
};

async function loadCarsTemplates() {
    if (CarsTemplates.loaded) return;

    const basePath = '/static/templates/cars/';
    const templateNames = [
        'handlebars_car_card.hbs',
        'handlebars_car_pagination.hbs',
        'handlebars_car_empty.hbs'
    ];

    const [cardHtml, paginationHtml, emptyHtml] = await Promise.all(
        templateNames.map(name => fetch(`${basePath}${name}`).then(r => r.text()))
    );

    CarsTemplates.carCard = Handlebars.compile(cardHtml);
    CarsTemplates.pagination = Handlebars.compile(paginationHtml);
    CarsTemplates.emptyState = Handlebars.compile(emptyHtml);
    CarsTemplates.loaded = true;
}

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

async function addCarsInCategory(element) {
    await loadCarsTemplates();

    const page = Number(element.getAttribute('data-page'));
    const categorySlug = element.getAttribute('data-category');

    const response = await fetch(
        `${urlGetCarsInCategory}?page=${page}&category=${categorySlug}`,
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }
    );

    if (!response.ok) {
        console.error('Failed to fetch cars:', response.status);
        return;
    }

    const data = await response.json();
    const cars = data.page?.object_list || [];
    const hasPages = data.has_pages;

    if (cars.length > 0) {
        const preparedCars = cars.map(prepareCarData);
        divCars.innerHTML += CarsTemplates.carCard(preparedCars);
        
        ulPaginationCars.innerHTML = CarsTemplates.pagination({
            next_page: hasPages?.has_next ? page + 1 : '',
            has_pages: hasPages,
            category: categorySlug
        });
    } else {
        divCars.innerHTML = CarsTemplates.emptyState();
        ulPaginationCars.innerHTML = '';
    }
}

loadCarsTemplates();