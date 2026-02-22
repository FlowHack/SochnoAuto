const urlGetFeedbacks = `${indexURL}api/v1/feedbacks/`;
ulPaginationFeedbacks = document.getElementById('ulPaginationFeedback')
divFeedbacks = document.getElementById('feedbacksBlock')


async function replaceFeedbacks(element) {
    const page = Number(element.getAttribute('data-page'))

    const result = await fetch(
        `${urlGetFeedbacks}?feedbacks_page=${page}`,
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }
    )
    const resultJSON = await result.json()
    const htmlFeedbacks = resultJSON.html_feedbacks
    const htmlPagination = resultJSON.html_pagination

    divFeedbacks.innerHTML = htmlFeedbacks
    ulPaginationFeedbacks.innerHTML = htmlPagination

    setTimeout(() => {
        const feedbacksSection = document.getElementById('feedbacks-section');
        if (feedbacksSection) {
            feedbacksSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }, 50);
}
