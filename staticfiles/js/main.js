
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



//CHECK AGE

 function checkAge() {
   let dob = new Date(document.getElementById("id_born").value); // Get the submitted date of birth
   let today = new Date();
   let age = today.getFullYear() - dob.getFullYear();

   if (age < 18) {
     alert("You must be at least 18 years old to submit this form.");
   } else {
     alert("You are eligible to submit this form");
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


///JQUERY MODAL

 $(document).ready(function () {
   $(".open-modal-button").click(function () {
     var id = $(this).data("id");
     $("#notifymyModal-" + id).show();
   });
 });


 //CHECK POSITIVE

 document.querySelector("form").addEventListener("submit", function (event) {
   var numberField = document.querySelector("#number-field");
   var number = parseFloat(numberField.value);
   if (isNaN(number) || number <= 0) {
     alert("Please enter a positive number");
     event.preventDefault();
   }
 });

 document.querySelector("form").addEventListener("submit", function (event) {
   var numberField = document.querySelector("#id_quantity");
   var number = parseFloat(numberField.value);
   if (isNaN(number) || number < 0) {
     alert("Please enter a positive number");
     event.preventDefault();
   }
 });

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



    

