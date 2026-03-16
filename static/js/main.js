/* Omnify Store – main.js */

/**
 * Обновляет счётчик корзины в навбаре
 * @param {number} count
 */
function updateCartBadge(count) {
    const badge = document.getElementById('cart-badge');
    if (!badge) return;
    badge.textContent = count;
}

/**
 * Показывает тост уведомление — отключено (no-op)
 */
function showToast(message, type = 'success', duration = 3500) {
    // уведомления отключены
}

/* Глобальный экспорт */
window.updateCartBadge = updateCartBadge;
window.showToast = showToast;
