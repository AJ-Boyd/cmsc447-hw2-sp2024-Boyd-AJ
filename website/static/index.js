//HTML animation
function showSearch(){
    var icon = document.getElementById("navSearch");
    var roster = document.getElementById("wrapper");
    icon.classList.toggle("fa-magnifying-glass");
    icon.classList.toggle("fa-xmark");
    icon.classList.toggle("btn-secondary");
    document.getElementById("searchForm").classList.toggle("hidden");
}

//populates edit form
function showInfo(id, name, points, e_id){
    document.getElementById("i").value = id;
    document.getElementById("name").value = name;
    document.getElementById("e_id").value = e_id
    document.getElementById("points").value = points;
}

//deletes the given entry from the database
function deleteEntry(id){
    if(confirm("Deleting entry " + id + ". Proceed?")){
        console.log("deleting entry...")
        fetch('/delete-entry', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ID: id })
        }).then(response => {
            //reloads home page
            window.location.replace("/");
        })
    }

}
