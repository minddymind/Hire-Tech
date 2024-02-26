const toggleBtn = document.querySelector('.toggle_btn')
const toggleBtnIcon = document.querySelector('.toggle_btn i')
const dropDownMenu = document.querySelector('.dropdown_menu')

toggleBtn.onclick = function () {
  dropDownMenu.classList.toggle('open')
  const isOpen = dropDownMenu.classList.contains('open')

  toggleBtnIcon.classList = isOpen ? 'fa-solid fa-xmark' : 'fa-solid fa-bars'
}

function toggleDropdown() {
  // Get the dropdown menu element
  var dropdownMenu = document.getElementById("dropdownMenuButton");
  // Toggle the 'show' class on the dropdown menu
  dropdownMenu.classList.toggle("show");
}
      