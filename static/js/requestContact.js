document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('form[id$="Form"]').forEach(form => {
        const consentCheckbox = form.querySelector('input[type="checkbox"][id$="Consent"]');
        const submitBtn = form.querySelector('button[type="submit"]');

        if (consentCheckbox && submitBtn) {
            consentCheckbox.addEventListener('change', function() {
                submitBtn.disabled = !this.checked;
            });
        }

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
            .then(r => r.json())
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
                    alert("Ошибка: " + data.errors.__all__[0]);
                }
            })
            .finally(() => { submitBtn.disabled = false; });
        });
    });
});