{% block js %}
<script>
document.addEventListener("DOMContentLoaded", () => {

    // PRODUCT FADE ANIMATION
    const items = document.querySelectorAll('.product-card');
    items.forEach((el, index) => {
        setTimeout(() => {
            el.classList.add('fade-in');
        }, index * 80); // stagger effect
    });

    // CATEGORY ANIMATION
    const cats = document.querySelectorAll('.category-box');
    cats.forEach((el, index) => {
        setTimeout(() => {
            el.classList.add('fade-in');
        }, index * 50);
    });

});
</script>
{% endblock %}
