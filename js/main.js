$(document).ready(function() {
    const menuToggle = $('.mobile-menu-toggle');
    const mainNav = $('.main-nav');

    menuToggle.on('click', function(e) {
        console.log('Menu toggle clicked');
        e.preventDefault();
        $(this).toggleClass('active');
        mainNav.toggleClass('active');
        
        // 切换菜单按钮的样式
        const spans = $(this).find('span');
        if ($(this).hasClass('active')) {
            spans.eq(0).css({
                'transform': 'rotate(45deg)',
                'background-color': '#4CAF50'
            });
            spans.eq(1).css({
                'opacity': '0'
            });
            spans.eq(2).css({
                'transform': 'rotate(-45deg)',
                'background-color': '#4CAF50'
            });
            
            // 禁止背景滚动
            $('body').css('overflow', 'hidden');
        } else {
            spans.eq(0).css({
                'transform': 'none',
                'background-color': '#333'
            });
            spans.eq(1).css({
                'opacity': '1'
            });
            spans.eq(2).css({
                'transform': 'none',
                'background-color': '#333'
            });
            
            // 恢复背景滚动
            $('body').css('overflow', '');
        }
    });

    mainNav.find('a').on('click', function() {
        menuToggle.removeClass('active');
        mainNav.removeClass('active');
        
        // 恢复菜单按钮样式
        const spans = menuToggle.find('span');
        spans.css({
            'transform': 'none',
            'background-color': '#333',
            'opacity': '1'
        });
        
        // 恢复背景滚动
        $('body').css('overflow', '');
    });
});