const urlGetFeedbacks = `${indexURL}api/v1/feedbacks/`;
const ulPaginationFeedbacks = document.getElementById('ulPaginationFeedback');
const divFeedbacks = document.getElementById('feedbacksBlock');

const FeedbacksTemplates = {
    feedbackCard: null,
    pagination: null,
    emptyState: null,
    loaded: false
};

async function loadFeedbacksTemplates() {
    if (FeedbacksTemplates.loaded) return;

    const basePath = '/static/templates/homepage/';
    const templateNames = [
        'handlebars_feedback_card.hbs',
        'handlebars_feedback_pagination.hbs',
        'handlebars_feedback_empty.hbs'
    ];

    const [cardHtml, paginationHtml, emptyHtml] = await Promise.all(
        templateNames.map(name => fetch(`${basePath}${name}`).then(r => r.text()))
    );

    FeedbacksTemplates.feedbackCard = Handlebars.compile(cardHtml);
    FeedbacksTemplates.pagination = Handlebars.compile(paginationHtml);
    FeedbacksTemplates.emptyState = Handlebars.compile(emptyHtml);
    FeedbacksTemplates.loaded = true;
}

function prepareFeedbackData(feedback) {
    const stars = [];
    const score = feedback.score || 0;
    for (let i = 1; i <= 5; i++) {
        stars.push(i <= score ? '★' : '☆');
    }
    return {
        ...feedback,
        stars
    };
}

async function replaceFeedbacks(element) {
    await loadFeedbacksTemplates();

    const page = Number(element.getAttribute('data-page'));

    const response = await fetch(
        `${urlGetFeedbacks}?feedbacks_page=${page}`,
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }
    );

    if (!response.ok) {
        console.error('Failed to fetch feedbacks:', response.status);
        return;
    }

    const data = await response.json();
    const feedbacks = data.page?.object_list || [];
    const hasPages = data.has_pages;

    if (feedbacks.length > 0) {
        const preparedFeedbacks = feedbacks.map(prepareFeedbackData);
        divFeedbacks.innerHTML = FeedbacksTemplates.feedbackCard(preparedFeedbacks);
        
        ulPaginationFeedbacks.innerHTML = FeedbacksTemplates.pagination({
            prev_page: hasPages?.has_previous ? page - 1 : '',
            next_page: hasPages?.has_next ? page + 1 : '',
            has_pages: hasPages
        });
    } else {
        divFeedbacks.innerHTML = FeedbacksTemplates.emptyState();
        ulPaginationFeedbacks.innerHTML = '';
    }

    setTimeout(() => {
        const section = document.getElementById('feedbacks-section');
        if (section) {
            section.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }, 50);
}

loadFeedbacksTemplates();