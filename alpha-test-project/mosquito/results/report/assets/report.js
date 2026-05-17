document.addEventListener('DOMContentLoaded', function () {
  var input = document.getElementById('table-filter');
  if (!input) return;
  input.addEventListener('input', function () {
    var query = input.value.toLowerCase();
    document.querySelectorAll('tbody tr').forEach(function (row) {
      row.hidden = query && !row.textContent.toLowerCase().includes(query);
    });
  });
});