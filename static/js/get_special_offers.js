const indexURL = document.location.protocol + "//" + document.location.hostname + ":" + document.location.port + "/";
const urlGetSpecialOffers = `${index_url}api/v1/get-special-offers`;
const specialOffersBlock = document.getElementById("mainBlockSpecialOffers");
const btnPaginationSpecialOffersPrevious = document.getElementById("btnSpecialOffersPrevious");
const btnPaginationSpecialOffersNext = document.getElementById("btnSpecialOffersNext");

async function replaceSpecialOffers(element) {
    const page = Number(element.getAttribute('data-page'));
    let urlOffer = element.getAttribute('data-url-offer');
    const urlStatic = element.getAttribute('data-url-static');

    urlOffer = urlOffer.split("/auto-offer-slug")[0];

    const result = await fetch(`${urlGetSpecialOffers}?special_offers_page=${page}`, {
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        }
    });
    const result_json = await result.json();
    const specialOffers = result_json.objects;
    const has_next = result_json.has_next;
    const has_previous = result_json.has_previous;

    specialOffersBlock.innerHTML = "";

    for (let i = 0; i < specialOffers.length; i++) {
        const offer = specialOffers[i];

        // Контейнер колонки (col-md-6 col-lg-4)
        let divCol = document.createElement("div");
        divCol.className = "col-md-6 col-lg-4";

        // Карточка предложения
        let divCard = document.createElement("div");
        divCard.className = "card card-dark h-100";
        divCol.appendChild(divCard);

        // Карусель изображений
        let divCarousel = document.createElement("div");
        divCarousel.className = "carousel slide card-carousel";
        divCarousel.id = `carouselOffer${offer.slug}`;
        divCarousel.setAttribute("data-bs-interval", "false");
        divCarousel.setAttribute("data-bs-touch", "true");
        divCard.appendChild(divCarousel);

        // Контейнер слайдов карусели
        let divCarouselInner = document.createElement("div");
        divCarouselInner.className = "carousel-inner";
        divCarousel.appendChild(divCarouselInner);

        // Добавляем слайды (изображения)
        if (offer.ordered_images && offer.ordered_images.length > 0) {
            for (let imgIdx = 0; imgIdx < offer.ordered_images.length; imgIdx++) {
                const image = offer.ordered_images[imgIdx];
                let divItem = document.createElement("div");
                divItem.className = `carousel-item${imgIdx === 0 ? " active" : ""}`;
                divCarouselInner.appendChild(divItem);

                let link = document.createElement("a");
                link.href = `${urlOffer}/${offer.slug}/`; // URL предложения
                link.className = "d-block h-100";
                divItem.appendChild(link);

                let img = document.createElement("img");
                img.src = image.image_url;
                img.className = "d-block w-100 h-100";
                img.style = "object-fit: cover;";
                img.alt = `${offer.brand} ${offer.car_model}`;
                img.loading = "lazy";
                link.appendChild(img);
            }
        } else {
            // Заполнитель, если изображений нет
            let divItem = document.createElement("div");
            divItem.className = "carousel-item active";
            divCarouselInner.appendChild(divItem);

            let link = document.createElement("a");
            link.href = `${urlOffer}/${offer.slug}/`;
            link.className = "d-block h-100";
            divItem.appendChild(link);

            let img = document.createElement("img");
            img.src = urlStatic;
            img.className = "d-block w-100 h-100";
            img.style = "object-fit: cover;";
            img.alt = "Нет фото";
            link.appendChild(img);
        }

        // Кнопки управления каруселью (если больше одного изображения)
        if (offer.ordered_images && offer.ordered_images.length > 1) {
            // Кнопка «Предыдущий»
            let btnPrev = document.createElement("button");
            btnPrev.type = "button";
            btnPrev.className = "carousel-control-prev";
            btnPrev.setAttribute("data-bs-target", `#carouselOffer${offer.slug}`);
            btnPrev.setAttribute("data-bs-slide", "prev");
            divCarousel.appendChild(btnPrev);

            let spanPrev = document.createElement("span");
            spanPrev.className = "carousel-control-prev-icon";
            spanPrev.setAttribute("aria-hidden", "true");
            btnPrev.appendChild(spanPrev);

            let spanPrevHidden = document.createElement("span");
            spanPrevHidden.className = "visually-hidden";
            spanPrevHidden.textContent = "Предыдущий";
            btnPrev.appendChild(spanPrevHidden);

            // Кнопка «Следующий»
            let btnNext = document.createElement("button");
            btnNext.type = "button";
            btnNext.className = "carousel-control-next";
            btnNext.setAttribute("data-bs-target", `#carouselOffer${offer.slug}`);
            btnNext.setAttribute("data-bs-slide", "next");
            divCarousel.appendChild(btnNext);

            let spanNext = document.createElement("span");
            spanNext.className = "carousel-control-next-icon";
            spanNext.setAttribute("aria-hidden", "true");
            btnNext.appendChild(spanNext);

            let spanNextHidden = document.createElement("span");
            spanNextHidden.className = "visually-hidden";
            spanNextHidden.textContent = "Следующий";
            btnNext.appendChild(spanNextHidden);

            // Индикаторы (точки)
            let divIndicators = document.createElement("div");
            divIndicators.className = "carousel-indicators";
            divCarousel.appendChild(divIndicators);

            for (let idx = 0; idx < offer.ordered_images.length; idx++) {
                let btnIndicator = document.createElement("button");
                btnIndicator.type = "button";
                btnIndicator.setAttribute("data-bs-target", `#carouselOffer${offer.slug}`);
                btnIndicator.setAttribute("data-bs-slide-to", idx);
                if (idx === 0) {
                    btnIndicator.className = "active";
                }
                divIndicators.appendChild(btnIndicator);
            }
        }

        // Тело карточки (информация о машине)
        let divBody = document.createElement("div");
        divBody.className = "card-body";
        divCard.appendChild(divBody);

        // Заголовок (марка и модель)
        let h5Title = document.createElement("h5");
        h5Title.className = "card-title";
        divBody.appendChild(h5Title);

        let linkTitle = document.createElement("a");
        linkTitle.href = `${urlOffer}/${offer.slug}/`;
        linkTitle.className = "text-decoration-none text-reset stretched-link-custom";
        linkTitle.textContent = `${offer.brand} ${offer.car_model}`;
        h5Title.appendChild(linkTitle);

        // Год выпуска
        let pYear = document.createElement("p");
        pYear.className = "card-text text-secondary small mb-2";
        pYear.textContent = offer.year_release.split("-")[0]; // Год из даты
        divBody.appendChild(pYear);

        // Цена
        let pPrice = document.createElement("p");
        pPrice.className = "card-text fw-bold text-end mb-0";
        pPrice.textContent = `${offer.price.toLocaleString('ru-RU')} ₽`;
        divBody.appendChild(pPrice);

        // Добавляем карточку в основной блок
        mainBlockSpecialOffers.appendChild(divCol);
    };

    if (has_previous) {
        btnPaginationSpecialOffersPrevious.setAttribute("data-page", page-1);
        btnPaginationSpecialOffersPrevious.style = ""
    } else {
        btnPaginationSpecialOffersPrevious.style = "visibility:hidden"
    }

    if (has_next) {
        btnPaginationSpecialOffersNext.setAttribute("data-page", page+1);
        btnPaginationSpecialOffersNext.style = ""
    } else {
        btnPaginationSpecialOffersNext.style = "visibility:hidden"
    };

    setTimeout(() => {
        const specialOffersSection = document.getElementById('special-offers-section');
        if (specialOffersSection) {
            specialOffersSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }, 100);
};

