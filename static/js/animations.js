document.addEventListener("DOMContentLoaded", () => {
    const container = document.querySelector(".form-container");
    container.style.opacity = "0";
    container.style.transform = "scale(0.8)";
    setTimeout(() => {
        container.style.transition = "all 0.5s ease";
        container.style.opacity = "1";
        container.style.transform = "scale(1)";
    }, 100);
});
