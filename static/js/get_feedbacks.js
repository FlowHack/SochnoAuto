const index_url = document.location.protocol + "//" + document.location.hostname + ":" + document.location.port + "/";
const url_get_feedbacks = `${index_url}api/v1/get-feedbacks`;
const feedbacks_block = document.getElementById("feedbacksBlock");
const ulPaginationFeedback = document.getElementById("ulPaginationFeedback");

async function replaceFeedbacks(element) {
    const page = Number(element.getAttribute('data-page'));
    const favicon = element.getAttribute('data-icon');

    const result = await fetch(`${url_get_feedbacks}?page_feedbacks=${page}`, {
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        }
    });
    const result_json = await result.json();
    const feedbacks = result_json.objects;
    const has_next = result_json.has_next;
    const has_previous = result_json.has_previous;

    feedbacks_block.innerHTML = "";

    for (let i = 0; i <= feedbacks.length - 1; i++) {
        feedback = feedbacks[i];

        let divCardForFeedback = document.createElement("div");
        divCardForFeedback.className = "col-md-6 col-lg-4";

        let divCardFeedback = document.createElement("div");
        divCardFeedback.className = "card feedback-card h-100";
        divCardForFeedback.appendChild(divCardFeedback)

        let divCardBody = document.createElement("div");
        divCardBody.className = "card-body";
        divCardFeedback.appendChild(divCardBody)

        let divUserName = document.createElement("div");
        divUserName.className = "d-flex justify-content-between align-items-start mb-2";
        divCardBody.appendChild(divUserName)

        let h6UserName = document.createElement("h6");
        h6UserName.className = "card-title mb-0";
        h6UserName.style = "color: #f1f5f9";
        h6UserName.innerHTML = feedback.name_user;
        divUserName.appendChild(h6UserName)

        let divScore = document.createElement("div");
        divScore.className = "stars-rating";
        divUserName.appendChild(divScore)

        let spanScore = document.createElement("span");
        if (feedback.score != null) {
            let innerSpanScore = ""
            for (let score_i = 1; score_i <= 5; score_i++) {
                if (score_i <= feedback.score) {
                    innerSpanScore += "★"
                } else {
                    innerSpanScore += "☆"
                };
            };
            spanScore.innerHTML = innerSpanScore
        } else {
            spanScore.innerHTML = "Оценки нет"
        };
        divScore.appendChild(spanScore)

        let pFeedback = document.createElement("p");
        pFeedback.className = "card-text text-secondary small"
        if (feedback.feedback != null) {
            pFeedback.innerHTML = feedback.feedback
        } else {
            pFeedback.innerHTML = "Отзыв без текста"
        };
        divCardBody.appendChild(pFeedback)

        if (feedback.answer != null && feedback.answer != "") {
            let divCompanyAnswer = document.createElement("div");
            divCompanyAnswer.className = "company-response";
            divCardBody.appendChild(divCompanyAnswer);

            let divLogoCompanyAnswer = document.createElement("div");
            divLogoCompanyAnswer.className = "d-flex align-items-center gap-2 mb-2";
            divCompanyAnswer.appendChild(divLogoCompanyAnswer);

            let imgLogoCompanyAnswer = document.createElement("img");
            imgLogoCompanyAnswer.className = "sochno-logo-icon";
            imgLogoCompanyAnswer.style = "width: 32px; height: 32px; font-size: 0.9rem"
            imgLogoCompanyAnswer.src = favicon
            divLogoCompanyAnswer.appendChild(imgLogoCompanyAnswer);

            let strongNameCompanyAnswer = document.createElement("strong");
            strongNameCompanyAnswer.style = "color: #f1f5f9";
            strongNameCompanyAnswer.innerHTML = "СОЧНО АВТО";
            divLogoCompanyAnswer.appendChild(strongNameCompanyAnswer);

            let pAnswerCompany = document.createElement("p");
            pAnswerCompany.className = "mb-0 small text-secondary";
            pAnswerCompany.innerHTML = feedback.answer
            divCompanyAnswer.appendChild(pAnswerCompany);
        };

        feedbacks_block.appendChild(divCardForFeedback)
    };

    ulPaginationFeedback.innerHTML = ""
    if (has_previous) {
        let liPageItemPreviousFeedback = document.createElement("li");
        liPageItemPreviousFeedback.className = "page-item";

        let aPageLinkPreviousFeedback = document.createElement("a");
        aPageLinkPreviousFeedback.className = "page-link";
        aPageLinkPreviousFeedback.innerHTML = "Назад";
        aPageLinkPreviousFeedback.setAttribute('data-page', page-1)
        aPageLinkPreviousFeedback.setAttribute('data-icon', favicon)
        aPageLinkPreviousFeedback.onclick= function() {replaceFeedbacks(this);};

        liPageItemPreviousFeedback.appendChild(aPageLinkPreviousFeedback)
        ulPaginationFeedback.appendChild(liPageItemPreviousFeedback)
    }
    if (has_next) {
        let liPageItemNextFeedback = document.createElement("li");
        liPageItemNextFeedback.className = "page-item";

        let aPageLinkNextFeedback = document.createElement("a");
        aPageLinkNextFeedback.className = "page-link";
        aPageLinkNextFeedback.innerHTML = "Далее";
        aPageLinkNextFeedback.setAttribute('data-page', page+1)
        aPageLinkNextFeedback.setAttribute('data-icon', favicon)
        aPageLinkNextFeedback.onclick= function() {replaceFeedbacks(this);};

        liPageItemNextFeedback.appendChild(aPageLinkNextFeedback)
        ulPaginationFeedback.appendChild(liPageItemNextFeedback)
    };

}