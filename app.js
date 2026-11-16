const search = document.querySelector('#search');
const category = document.querySelector('#category');
const entries = [...document.querySelectorAll('.entry')];
function filter() {
  const query = search.value.trim().toLocaleLowerCase();
  let count = 0;
  for (const entry of entries) {
    const visible = entry.dataset.search.toLocaleLowerCase().includes(query) && (!category.value || entry.dataset.category === category.value);
    entry.hidden = !visible;
    if (visible) count++;
  }
  document.querySelector('#count').textContent = `${count} 个站点`;
  document.querySelector('#empty').hidden = count !== 0;
}
search.addEventListener('input', filter);
category.addEventListener('change', filter);
