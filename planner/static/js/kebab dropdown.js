function kebab_clicked(category_id) {
    alert("kebab clicked");
    // show the menu
    $("#kebab-" + category_id).classList.add('show-kebab-menu');
    $("#kebab-btn-" + category_id).setAttribute('aria-hidden', false);
    // $("#kebab-menu-" + category_id).addEventListener('mousedown', hideMenu, false);
}

// $(window).click(function() {
//     alert("window clicked");
// //Hide the menus if visible
// //     el.classList.remove('show-kebab-menu');
// //     menu.setAttribute('aria-hidden', true);
//     // document.removeEventListener('mousedown', hideMenu);
// });

// $('.kebab-click').click(function(event){
//     event.stopPropagation();
// });

// var el = document.querySelector('.kebab');
//         var btn = el.querySelector('.kebab-btn');
//         var menu = el.querySelector('.kebab-menu');
//         var visible = false;
//
//         function showMenu(e) {
//             e.preventDefault();
//             if (!visible) {
//                 visible = true;
//                 el.classList.add('show-kebab-menu');
//                 menu.setAttribute('aria-hidden', false);
//                 document.addEventListener('mousedown', hideMenu, false);
//             }
//         }
//
//         function hideMenu(e) {
//             if (btn.contains(e.target)) {
//                 return;
//             }
//             if (visible) {
//                 visible = false;
//                 el.classList.remove('show-kebab-menu');
//                 menu.setAttribute('aria-hidden', true);
//                 document.removeEventListener('mousedown', hideMenu);
//             }
//         }
//
//         btn.addEventListener('click', showMenu, false);
//
//