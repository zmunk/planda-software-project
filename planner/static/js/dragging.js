// var d = dragula({
//     moves: function(el, cont, handle) {
//         return handle.className !== 'title'
//     }
// })
// var cs = document.querySelectorAll('.list-items')
// for (var i in cs) {
//     d.containers.push(cs[i])
// }


let to_list = "";
let task_id = "";
let task_order = -1;

let task_home_order = -1;
let to_list_home = "";

let temp = document.querySelector(".temp-storage");

let draggableElements = document.querySelectorAll(".draggable");
let droppableElements = document.querySelectorAll(".droppable");

draggableElements.forEach(elem => {
    elem.addEventListener("dragstart", dragStart);
    elem.addEventListener("dragend", dragEnd);
});

droppableElements.forEach(elem => {
    elem.addEventListener("dragenter", dragEnter);
    elem.addEventListener("dragover", dragOver);
    elem.addEventListener("dragleave", dragLeave);
    elem.addEventListener("drop", drop, false);
});

function dragStart(e) {
    console.log("starting drag");

    // let crt = e.target.cloneNode(true);
    // crt.style.backgroundColor = "red";
    // crt.style.visibility = "hidden"; /* or visibility: hidden, or any of the above */
    // document.body.appendChild(crt);
    // e.dataTransfer.setDragImage(crt, 0, 0);

    window.currentItem = e.target;
    window.currentItem.classList.add("current-item");

    task_id = window.currentItem.getAttribute("data-taskId");
    task_home_order = window.currentItem.getAttribute("data-taskOrder");

    // the parent that the dragged item will return to
    window.homeParent = e.target.parentNode;
    to_list = window.homeParent.getAttribute("data-parentId");
    to_list_home = window.homeParent.getAttribute("data-parentId");

    // window.homeParent.classList.add("testing1");
    setTimeout(function () {
        // window.homeParent.classList.remove("testing1");
        window.homeParent.classList.add("children-no-pointer-events");
    }, 1);

    e.dataTransfer.setData("text", e.target.id);
}

function dragEnd(e) {
    window.currentItem.classList.remove("current-item");

    if (temp.contains(window.currentItem)) {
        window.homeParent.insertBefore(window.currentItem, window.homeParent.children[task_home_order]);
        // task_order = task_home_order;
        // to_list = to_list_home;
        // window.homeParent.appendChild(window.currentItem);
        // TODO: insert in home order
        return;
    }
    console.log("to_list " + to_list);
    console.log("task_id " + task_id);
    console.log("task_order " + task_order);
    $.ajax({
        url: "update",
        data: {
            to_list: to_list,
            task_id: task_id,
            task_order: task_order,
        },
        success: function (result) {
            // $("#div1").html(result);
        },
        error: function () {
        }
    });
    window.currentItem = null;


    // }
}

function dragEnter(e) {
    if (e.target.classList.contains("droppable")) {

        // (below) allows the parent to see dragged object through its children
        e.target.classList.add("children-no-pointer-events");


        to_list = e.target.getAttribute("data-parentId");

    }
}

function dragOver(e) {
    if (e.target.classList.contains("droppable")) {
        e.preventDefault();
        const listItems = e.target.children;
        let mouseY = e.clientY;
        let j = listItems.length;
        for (let i = listItems.length - 1; i >= 0; i--) {
            const li = listItems[i];
            const liY = li.getBoundingClientRect().y + li.getBoundingClientRect().height / 2;
            if (liY > mouseY) {
                j = i;
            }
        }
        // TODO: animated transitions
        task_order = j;
        e.target.insertBefore(window.currentItem, e.target.children[j]);
    }
}

function dragLeave(e) {
    if (e.target.classList.contains("droppable")) {

        if (!temp.contains(window.currentItem)) {
            // adding dragged item to temporary storage
            temp.appendChild(window.currentItem);
        }

        e.target.classList.remove("children-no-pointer-events");
    }
}

function drop(e) {
    e.target.classList.remove("children-no-pointer-events");
}


/* AJAX code */

// $(document).ready(function(){
//   $("button").click(function(){

//   var task_id =
//   var new_state =


//     $.ajax({
//         url: "/PutToghther",
//         data:{new_state:new_state,task:task_id},
//         success: function(result){
//       $("#div1").html(result);
//     },
//     error:function(){


//             }

//     });
//   });
// });