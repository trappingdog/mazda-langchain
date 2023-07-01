$(function() {
    $(document).on('click', '#hamburgerButton', function() {
        $('#mainSidebar').sidebar('toggle');
    });
    const cookieScrollTop = Cookies.get('scrollTop');
    if (cookieScrollTop) {
        setTimeout(function() {
            $('.simplebar-content-wrapper').scrollTop(cookieScrollTop);
        }, 10);
    }
    $('.simplebar-content-wrapper').scroll(function() {
        Cookies.set('scrollTop', $(this).scrollTop());
    });
});
new Stickyfill.add(document.querySelectorAll('.chapterSelectedHeader'));
new objectFitImages(document.querySelectorAll('.ofiImage'));
if(document.getElementById('mainSidebar') != null) {
    new SimpleBar(document.getElementById('mainSidebar'));
}
