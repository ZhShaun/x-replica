document.addEventListener('DOMContentLoaded', function () {
    const myModalEl = document.getElementById('modals-here');
    let bootstrapModalInstance = null;

    // HTMX event listener for 'closeModal'
    document.body.addEventListener('closeModal', function (event) {
        if (myModalEl) {
            bootstrapModalInstance = bootstrap.Modal.getInstance(myModalEl);

            if (bootstrapModalInstance) {
                bootstrapModalInstance.hide();
            } else {
                // In case it's not yet initialized (less common for a persistent modal div)
                bootstrapModalInstance = new bootstrap.Modal(myModalEl);
                bootstrapModalInstance.hide();
            }
        }
    });

    // Bootstrap's 'hidden.bs.modal' event listener for final cleanup
    if (myModalEl) {
        myModalEl.addEventListener('hidden.bs.modal', function (event) {
            // 1. Remove any lingering modal backdrops
            const backdrops = document.querySelectorAll('.modal-backdrop');
            backdrops.forEach(backdrop => {
                backdrop.remove();
            });

            // 2. Ensure body class 'modal-open' is removed
            document.body.classList.remove('modal-open');

            // 3. Clear the content for the next open.
            const modalContentDiv = myModalEl.querySelector('.modal-content');
            if (modalContentDiv) {
                modalContentDiv.innerHTML = '';
            }
        });
    }

    // The 'refreshTimeline' event listener
    document.body.addEventListener('refreshTimeline', function (event) {
        // This now correctly triggers the 'refresh' hx-trigger on #timeline-items
        htmx.trigger("#timeline-items", "refresh");
    });
});