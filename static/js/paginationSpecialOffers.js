const urlGetSpecialOffers = `${indexURL}api/v1/special-offers/`;
divPaginationSpecialOffers = document.getElementById('divPaginationSpecialOffers')
divSpecialOffers = document.getElementById('mainBlockSpecialOffers')


async function replaceSpecialOffers(element) {
    const page = Number(element.getAttribute('data-page'))

    const result = await fetch(
        `${urlGetSpecialOffers}?special_offers_page=${page}`,
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }
    )
    const resultJSON = await result.json()
    const htmlSpecialOffers = resultJSON.html_cards
    const htmlPagination = resultJSON.html_pagination

    divSpecialOffers.innerHTML = htmlSpecialOffers
    divPaginationSpecialOffers.innerHTML = htmlPagination

    setTimeout(() => {
        const specialOffersSection = document.getElementById('special-offers-section');
        if (specialOffersSection) {
            specialOffersSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }, 100);
}
