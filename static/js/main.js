
//GET SEARCH FORM AND PAGE LINKS
let searchForm = document.getElementById('searchForm')
let pageLinks = document.getElementsByClassName('page-link')

//ENSURE SEARCH FORM EXISTS
if (searchForm) {
    for (let i = 0; pageLinks.length > i; i++) {
        pageLinks[i].addEventListener('click', function (e) {
            e.preventDefault()

            //GET THE DATA ATTRIBUTE
            let page = this.dataset.page

            //ADD HIDDEN SEARCH INPUT TO FORM
            searchForm.innerHTML += `<input value=${page} name="page" hidden/>`


            //SUBMIT FORM
            searchForm.submit()
        })
    }
}




// Get the modal image
var imageModal = document.getElementById("myModalImage");

// Get the button that opens the modal
var btnImage = document.getElementById("myModalImg");
// Get the image and insert it inside the modal - use its "alt" text as a caption

var modalImg = document.getElementById("productImage");
var captionTextImage = document.getElementById("captionImage");

// Get the <span> element that closes the modal
var spanImage = document.getElementsByClassName("closeImage")[0];

// When the user clicks the button, open the modal 
btnImage.onclick = function() {
  imageModal.style.display = "block";
  modalImg.src = this.src;
  captionTextImage.innerHTML = this.alt;
}

// When the user clicks on <span> (x), close the modal
spanImage.onclick = function() {
  imageModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == imageModal) {
    imageModal.style.display = "none";
  }
}



// LIVE SEARCH



    // $("#Search").on("keyup", function(){
    //   var value = $(this).val();
    //   console.log(value);
    //   $("table tr").each(function(e){
    //     if(e !== 0){
    //       $go = $(this)

    //       $go.find('td').each(function(){
    //         var id = $(this).text();

    //         if(id.indexOf(value) !==0 && id.toLowerCase().indexOf(value.toLowerCase()) < 0){
    //           $go.hide();

    //         }
    //         else {
    //           $go.show();
    //           return false;
    //         }
    //       });
    //     }
    //     var isNone = $("#MyTable tr:not('.chk-th'):visible");

    //     if(isNone.length == 0){
    //       $("#no-data").text("No result Found").show();

    //     }
    //     else {
    //       $("#no-data").text("No result Found").hide();

    //     }
    //   })
    // })

