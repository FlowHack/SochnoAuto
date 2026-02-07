const index_url = document.location.protocol + "//" + document.location.hostname + ":" + document.location.port + "/";
const url_get_cars_in_category = `${index_url}api/v1/get-cars-in-category`;
const carsBlock = document.getElementById("cars-block");
const ulPaginationCars = document.getElementById("ul-pagination-cars");
let searchParams = new URLSearchParams(document.location.search);

async function addCars(element) {
    const page = Number(element.getAttribute('data-page'));
    let urlOffer = element.getAttribute('data-url-offer');
    const urlStatic = element.getAttribute('data-url-static');
    const category = searchParams.get("category");

    urlOffer = urlOffer.split("/auto-offer-slug")[0];

    const result = await fetch(`${url_get_cars_in_category}?category=${category}&page=${page}`, {
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        }
    });
    const result_json = await result.json();
    const cars = result_json.objects;
    const has_next = result_json.has_next;

    if (cars == null) {
        throw new Error("Нет такой категории или в ней нет машин");
    }

    for (let i = 0; i < cars.length; i++) {
        const car = cars[i];

        // Колонка сетки (col-md-6 col-lg-4)
        let divCol = document.createElement("div");
        divCol.className = "col-md-6 col-lg-4";

        // Карточка автомобиля
        let divCard = document.createElement("div");
        divCard.className = "card card-dark h-100";
        divCol.appendChild(divCard);

        // Карусель изображений
        let divCarousel = document.createElement("div");
        divCarousel.className = "carousel slide card-carousel";
        divCarousel.id = `carouselAuto${car.slug}`;
        divCarousel.setAttribute("data-bs-ride", "carousel");
        divCarousel.setAttribute("data-bs-touch", "true");
        divCard.appendChild(divCarousel);

        // Контейнер слайдов
        let divCarouselInner = document.createElement("div");
        divCarouselInner.className = "carousel-inner";
        divCarousel.appendChild(divCarouselInner);

        // Изображения (или заглушка)
        if (car.ordered_images && car.ordered_images.length > 0) {
            for (let imgIdx = 0; imgIdx < car.ordered_images.length; imgIdx++) {
                const photo = car.ordered_images[imgIdx];
                let divItem = document.createElement("div");
                divItem.className = `carousel-item${imgIdx === 0 ? " active" : ""}`;
                divCarouselInner.appendChild(divItem);

                let img = document.createElement("img");
                img.src = photo.image_url;
                img.className = "d-block w-100";
                img.alt = photo.caption || `${car.brand} ${car.car_model}`;
                divItem.appendChild(img);
            }
        } else {
            // Заглушка при отсутствии фото
            let divItem = document.createElement("div");
            divItem.className = "carousel-item active";
            divCarouselInner.appendChild(divItem);

            let img = document.createElement("img");
            img.src = urlStatic;
            img.className = "d-block w-100";
            img.alt = `${car.brand} ${car.car_model}`;
            divItem.appendChild(img);
        }

        // Элементы управления каруселью (если больше 1 фото)
        if (car.ordered_images && car.ordered_images.length > 1) {
            // Контейнер кнопок управления
            let divControlsWrap = document.createElement("div");
            divControlsWrap.className = "card-carousel-controls-wrap";
            divCarousel.appendChild(divControlsWrap);

            // Кнопка "Предыдущий"
            let btnPrev = document.createElement("button");
            btnPrev.type = "button";
            btnPrev.className = "carousel-control-prev card-carousel-control";
            btnPrev.setAttribute("data-bs-target", `#carouselAuto${car.slug}`);
            btnPrev.setAttribute("data-bs-slide", "prev");
            divControlsWrap.appendChild(btnPrev);

            let spanPrevIcon = document.createElement("span");
            spanPrevIcon.className = "carousel-control-prev-icon";
            spanPrevIcon.setAttribute("aria-hidden", "true");
            btnPrev.appendChild(spanPrevIcon);

            let spanPrevHidden = document.createElement("span");
            spanPrevHidden.className = "visually-hidden";
            spanPrevHidden.textContent = "Предыдущее фото";
            btnPrev.appendChild(spanPrevHidden);

            // Кнопка "Следующий"
            let btnNext = document.createElement("button");
            btnNext.type = "button";
            btnNext.className = "carousel-control-next card-carousel-control";
            btnNext.setAttribute("data-bs-target", `#carouselAuto${car.slug}`);
            btnNext.setAttribute("data-bs-slide", "next");
            divControlsWrap.appendChild(btnNext);

            let spanNextIcon = document.createElement("span");
            spanNextIcon.className = "carousel-control-next-icon";
            spanNextIcon.setAttribute("aria-hidden", "true");
            btnNext.appendChild(spanNextIcon);

            let spanNextHidden = document.createElement("span");
            spanNextHidden.className = "visually-hidden";
            spanNextHidden.textContent = "Следующее фото";
            btnNext.appendChild(spanNextHidden);

            // Индикаторы
            let divIndicators = document.createElement("div");
            divIndicators.className = "carousel-indicators";
            divCarousel.appendChild(divIndicators);

            for (let idx = 0; idx < car.ordered_images.length; idx++) {
                let btnIndicator = document.createElement("button");
                btnIndicator.type = "button";
                btnIndicator.setAttribute("data-bs-target", `#carouselAuto${car.slug}`);
                btnIndicator.setAttribute("data-bs-slide-to", idx);
                if (idx === 0) {
                    btnIndicator.className = "active";
                }
                divIndicators.appendChild(btnIndicator);
            }
        }

        // Тело карточки
        let divBody = document.createElement("div");
        divBody.className = "card-body";
        divCard.appendChild(divBody);

        // Заголовок с ссылкой
        let h5Title = document.createElement("h5");
        h5Title.className = "card-title";
        divBody.appendChild(h5Title);

        let linkTitle = document.createElement("a");
        linkTitle.href = `${urlOffer}/${car.slug}/`;
        linkTitle.className = "card-title-car text-decoration-none text-reset stretched-link-custom";
        linkTitle.textContent = `${car.brand} ${car.car_model}`;
        h5Title.appendChild(linkTitle);

        // Информация (год выпуска и пробег)
        let pInfo = document.createElement("p");
        pInfo.className = "card-text text-secondary small mb-2";
        pInfo.textContent = `${new Date(car.year_release).getFullYear()} | ${car.mileage.toLocaleString('ru-RU')} км`;
        divBody.appendChild(pInfo);

        // Цена
        let pPrice = document.createElement("p");
        pPrice.className = "card-text fw-bold text-end mb-0";
        pPrice.textContent = `${car.price.toLocaleString('ru-RU')} ₽`;
        divBody.appendChild(pPrice);

        // Добавляем карточку в колонку
        divCol.appendChild(divCard);


        // Добавляем колонку в основной контейнер (cars-block)
        carsBlock.appendChild(divCol);
    }

    ulPaginationCars.innerHTML = ""
    if (has_next) {
        let liPageItemNextCars = document.createElement("li");
        liPageItemNextCars.className = "page-item";

        let aPageLinkNextCars = document.createElement("a");
        aPageLinkNextCars.className = "page-link";
        aPageLinkNextCars.innerHTML = "Показать ещё";
        aPageLinkNextCars.setAttribute('data-page', page+1);
        aPageLinkNextCars.setAttribute('data-url-offer', urlOffer);
        aPageLinkNextCars.setAttribute('data-url-static', urlStatic);
        aPageLinkNextCars.onclick= function() {addCars(this);};

        liPageItemNextCars.appendChild(aPageLinkNextCars)
        ulPaginationCars.appendChild(liPageItemNextCars)
    };

};
