const SearchTemplates = {
    result: null,
    pagination: null,
    emptyState: null,
    loaded: false
};

async function loadSearchTemplates() {
    if (SearchTemplates.loaded) return;

    const basePath = '/static/templates/cars/';
    const templateNames = [
        'handlebars_search_result.hbs',
        'handlebars_search_pagination.hbs',
        'handlebars_search_empty.hbs'
    ];

    const [resultHtml, paginationHtml, emptyHtml] = await Promise.all(
        templateNames.map(name => fetch(`${basePath}${name}`).then(r => r.text()))
    );

    SearchTemplates.result = Handlebars.compile(resultHtml);
    SearchTemplates.pagination = Handlebars.compile(paginationHtml);
    SearchTemplates.emptyState = Handlebars.compile(emptyHtml);
    SearchTemplates.loaded = true;
}

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
}

function formatMileage(mileage) {
    return mileage.toLocaleString('ru-RU');
}

const TRANSMISSION_DISPLAY = {
    'at': 'AT',
    'amt': 'AMT',
    'mt': 'MT',
    'cvt': 'CVT'
};

function prepareSearchCarData(car) {
    const firstImage = car.ordered_images && car.ordered_images.length > 0
        ? car.ordered_images[0].image_url
        : '/static/images/placeholder-car.jpg';

    return {
        ...car,
        first_image: firstImage,
        type_transmission_display: TRANSMISSION_DISPLAY[car.type_transmission] || (car.type_transmission || '').toUpperCase(),
        mileage_formatted: formatMileage(car.mileage)
    };
}

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');

    if (searchInput && searchResults) {
        const searchUrl = '/api/v1/search-car/';
        let debounceTimer;

        searchInput.addEventListener('input', function() {
            const query = this.value.trim();

            clearTimeout(debounceTimer);

            if (query.length < 2) {
                searchResults.classList.add('d-none');
                searchResults.innerHTML = '';
                return;
            }

            debounceTimer = setTimeout(async function() {
                await loadSearchTemplates();

                try {
                    const response = await fetch(searchUrl + '?page=1&search=' + encodeURIComponent(query));
                    const data = await response.json();

                    console.log('API response:', data);
                    const cars = data.page?.object_list || [];
                    console.log('Cars:', cars);
                    const hasValidCars = cars.some(car => car.slug && car.brand);
                    console.log('hasValidCars:', hasValidCars);

                    if (hasValidCars) {
                        const preparedCars = cars.map(prepareSearchCarData);
                        searchResults.innerHTML = preparedCars.map(car => SearchTemplates.result(car)).join('') + SearchTemplates.pagination({
                            prev_page: '',
                            next_page: data.has_pages?.has_next ? '2' : '',
                            has_pages: data.has_pages
                        });
                    } else {
                        searchResults.innerHTML = SearchTemplates.emptyState() + SearchTemplates.pagination({
                            prev_page: '',
                            next_page: '',
                            has_pages: { has_next: false, has_previous: false }
                        });
                    }
                    searchResults.classList.remove('d-none');
                } catch {
                    searchResults.classList.add('d-none');
                }
            }, 300);
        });

        searchInput.addEventListener('focus', function() {
            if (searchResults.innerHTML && !searchResults.classList.contains('d-none')) {
                searchResults.classList.remove('d-none');
            }
        });

        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.classList.add('d-none');
            }
        });
    }
});

async function replaceSearchCars(element) {
    await loadSearchTemplates();

    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    const page = Number(element.getAttribute('data-page'));
    const query = searchInput.value.trim();
    const searchUrl = `/api/v1/search-car/?page=${page}&search=` + encodeURIComponent(query);

    const response = await fetch(searchUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const data = await response.json();
    const cars = data.page?.object_list || [];
    const hasValidCars = cars.some(car => car.slug && car.brand);

    if (hasValidCars) {
        const preparedCars = cars.map(prepareSearchCarData);
        searchResults.innerHTML = preparedCars.map(car => SearchTemplates.result(car)).join('') + SearchTemplates.pagination({
            prev_page: data.has_pages?.has_previous ? page - 1 : '',
            next_page: data.has_pages?.has_next ? page + 1 : '',
            has_pages: data.has_pages
        });
    } else {
        searchResults.innerHTML = SearchTemplates.emptyState() + SearchTemplates.pagination({
            prev_page: '',
            next_page: '',
            has_pages: { has_next: false, has_previous: false }
        });
    }
}

loadSearchTemplates();