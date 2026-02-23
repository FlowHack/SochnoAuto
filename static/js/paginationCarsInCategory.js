const urlGetCarsInCategory = `${indexURL}api/v1/category/`;
ulPaginationCars = document.getElementById('ul-pagination-cars')
divCars = document.getElementById('cars-block')


async function addCarsInCategory(element) {
    const page = Number(element.getAttribute('data-page'))
    const categorySlug = element.getAttribute('data-category')

    const result = await fetch(
        `${urlGetCarsInCategory}?page=${page}&category=${categorySlug}`,
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }
    )

    const resultJSON = await result.json()
    const htmlCars = resultJSON.html_cards
    const htmlPagination = resultJSON.html_pagination

    divCars.innerHTML += htmlCars
    ulPaginationCars.innerHTML = htmlPagination
}

