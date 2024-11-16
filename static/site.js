
function test(id,name) {
    if(confirm('Are you sure you want to delete ' + name + '?') == true) {
      window.location.href = '/delete/' + id;
    }
    else {
        return false;
    }
}
function review(id) {
      window.location.href = '/review/' + id;
}
function cancel(){
      window.location.href = '/';
}