var d = dragula({
    moves: function(el, cont, handle) {
        return handle.className !== 'title'
    }
})
var cs = document.querySelectorAll('.list-items')
for (var i in cs) {
    d.containers.push(cs[i])
}
