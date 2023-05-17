// const selectedLang = document.querySelector('.selected-lang span')
// const lang = document.querySelectorAll('.lang-item')
// console.log(lang);
// lang.forEach((item, key) => {
//   item.addEventListener('click', function() {
//     selectedLang.innerHTML = item.innerHTML
//   })
// })




const img = document.querySelector('.product_img-img');
const btns = document.querySelectorAll('.color_squer');

changeImg();

function removeAct() {
  btns.forEach((btn) => {
    btn.classList.remove('active');
  })
}

function changeImg() {
  btns.forEach(btn => {
    btn.addEventListener('click', () => {
      removeAct();
      btn.classList.toggle('active');
      let attr = btn.getAttribute('data-tabs');
      
      if (attr == 'white') {
         img.src = '../image/goods/Rectangle 356.png';
      }else if(attr == 'black'){
        img.src = '../image/goods/Rectangle 356 (6).png'
      }
      else if(attr == 'red'){
        img.src = '../image/goods/Rectangle 356 (1).png'
      }
      
    })
  });
}






var owl = $('.product_detail-slider');
owl.owlCarousel({
    items:1,
    loop:true,
    margin:15,
    autoplay:true,
    autoplayTimeout:1000,
    autoplayHoverPause:true
});
$('.play').on('click',function(){
    owl.trigger('play.owl.autoplay',[1000])
})
$('.stop').on('click',function(){
    owl.trigger('stop.owl.autoplay')
})


























