document.addEventListener('DOMContentLoaded', () => {
    const toasts = document.querySelectorAll('.toast');

    toasts.forEach((toast) => {
        setTimeout(() => {
            toast.classList.add('toast-hide');
            toast.addEventListener('transitionend', () => toast.remove());
        }, 3500); // Dismiss after 3.5 seconds
    });
});