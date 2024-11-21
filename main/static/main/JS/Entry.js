{% load static %}
const form = document.forms[0];
const text = form.querySelectorAll(`.input-box`);

form.addEventListener(`submit`, (evt) => {
  evt.preventDefault();
  document.location.href = "{% url 'home' %}";
});