export function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
    } else {
        console.error(`Modal com ID "${modalId}" não encontrado.`);
    }
}

export function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    } else {
        console.error(`Modal com ID "${modalId}" não encontrado.`);
    }
}
// Lógica para o menu hambúrguer
document.addEventListener('DOMContentLoaded', function () {
    const hamburgerButton = document.getElementById('hamburgerButton');
    const mobileMenu = document.getElementById('mobileMenu');

    if (hamburgerButton && mobileMenu) {
        hamburgerButton.addEventListener('click', function () {
            mobileMenu.classList.toggle('hidden'); // Alterna a classe 'hidden' para mostrar/ocultar o menu
        });
    }
});