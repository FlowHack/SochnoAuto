document.addEventListener('DOMContentLoaded', function() {
    function showErrorAlert(form, message) {
        var alert = document.createElement('div');
        alert.className = 'alert alert-danger alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3';
        alert.style.zIndex = '9999';
        alert.innerHTML = `${message}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
        document.body.appendChild(alert);
        setTimeout(function() { alert.remove(); }, 5000);
    }

    document.querySelectorAll('form[id$="Form"]').forEach(form => {
        const consentCheckbox = form.querySelector('input[type="checkbox"][id$="Consent"]');
        const submitBtn = form.querySelector('button[type="submit"]');

        function updateButtonState() {
            if (consentCheckbox && submitBtn) {
                submitBtn.disabled = !consentCheckbox.checked;
            }
        }

        if (consentCheckbox && submitBtn) {
            consentCheckbox.addEventListener('change', updateButtonState);
            updateButtonState();
        }

        form.closest('.modal').addEventListener('shown.bs.modal', function() {
            form.reset();
            updateButtonState();
        });

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            submitBtn.disabled = true;

            fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.errors?.__all__?.[0] || 'Ошибка при отправке формы');
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const modal = bootstrap.Modal.getInstance(form.closest('.modal'));
                    if (modal) modal.hide();
                    form.reset();
                    var alert = document.createElement('div');
                    alert.className = 'alert alert-success alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3';
                    alert.style.zIndex = '9999';
                    alert.innerHTML = `${data.message}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
                    document.body.appendChild(alert);
                    setTimeout(function() { alert.remove(); }, 5000);
                } else {
                    showErrorAlert(form, data.errors?.__all__?.[0] || 'Ошибка при отправке формы');
                }
            })
            .catch(error => {
                showErrorAlert(form, error.message);
            })
            .finally(() => { submitBtn.disabled = false; });
        });
    });
});