/**
 * 通用模块
 *
 */
var $win = $(window),
    $doc = $(document),
    $body = $('body', $doc),
    winW = $win.width();
$(window).resize(function() {
    winW = $win.width();
})
/**
 * 图片加载
 */
$(function() {
    if (!$.fn.lazyload) return;
    $(".lazy", $body).lazyload({
        effect: "fadeIn",
        threshold: 400,
        failure_limit: 0
    });
});
// 出现
$(function() {
    if ($win.width() > 992) {
        if (!(/msie [6|7|8|9]/i.test(navigator.userAgent))) {
            new WOW().init();
        };
    }
});
//语言下拉
$(function() {
    if (winW < 768) return;
    $(".language").on("mouseenter", function() {
        $(this).children("ul").stop().slideDown(200);
    }).on("mouseleave", function() {
        $(this).children("ul").stop().slideUp(200);
    });
});
$(function() {
    if (winW < 768) return;
    $(".header .product-nav > ul > li").on("mouseenter", function() {
        $(this).children(".nav-down").stop().slideDown(200);
    }).on("mouseleave", function() {
        $(this).children(".nav-down").stop().slideUp(200);
    });
});
// $(function() {
//     if (winW < 1200) return;
//     $(".nav .nav-list1 li:nth-child(3)").on("mouseenter", function() {
//         $(".nav-down").stop().slideDown(200);
//     });
//     $(".header").on("mouseleave", function() {
//         $(".nav-down").stop().slideUp(200);
//     });
// });
// 导航有二级加more
$(function() {
    var tags = $(".header .nav .nav-list1 > li").length;
    // console.log(tags);
    for (var i = 0; i <= tags; i++) {
        var tags1 = $(".header .nav .nav-list1 > li").eq(i).find("li").length;
        if (tags1 > 0) {
            $(".header .nav .nav-list1 > li").eq(i).addClass("more");
        }
    }
});
// faq
$(function() {
    if (winW < 768) return;
    $(".wrap-faq .faq .item").on("mouseenter", function() {
        $(this).children(".text").stop().slideDown(200);
    }).on("mouseleave", function() {
        $(this).children(".text").stop().slideUp(200);
    });
});;
// 数字滚动
$(function() {
    $('.counter').countUp();
}); // 导航固定
$(function() {
    if (winW > 1199) {
        var sticky = new Waypoint.Sticky({
            element: $('.header-nav')[0]
        });
        // var sticky1 = new Waypoint.Sticky({
        //     element: $('.product-show-nav')[0]
        // });
    } else {
        var sticky = new Waypoint.Sticky({
            element: $('.header-middle')[0]
        });
    }
})
// $(function() {
//     $(window).on("scroll", function() {
//         var t = document.documentElement.scrollTop || document.body.scrollTop; //获取滚动距离
//         if (screen.width > 0) {
//             if (t >= 100) { //判断
//                 $(".header").addClass("fixed-header");
//             } else {
//                 $(".header").removeClass("fixed-header");
//             }
//         }
//     })
// });
//内页滑动导航
$(function() {
    var wrap = $(".inside-nav"),
        el_active = wrap.find(".active");
    if (!wrap.length || !el_active.length) return;
    var active_width = el_active.outerWidth(),
        wrap_width = wrap.width(),
        act_posi_left = el_active.position().left,
        act_width = el_active.outerWidth(),
        inline_wrap = el_active.parent(),
        inline_width = inline_wrap.outerWidth(true),
        distance = (act_posi_left + act_width / 2) - (wrap.outerWidth() / 2);
    //  if(inline_width <= wrap_width) {
    //  }
    if (distance <= 0) return;
    wrap.scrollLeft(distance);
});
//头部导航
$(function() {
    //折叠导航
    var oset;
    $(".nav-collapse").click(function(e) {
        if (e && e.stopPropagation) {
            e.stopPropagation();
        } else {
            window.event.cancelBubble = true;
        }
        $(".nav-collapse").toggleClass("active");
        $(".nav").stop().fadeToggle().toggleClass("fade-out");
        $("body").toggleClass("fixed");
        $(".video-box").toggle();
        $(".nav").removeClass("left-100 left-200");
        if (winW > 1200) {
            $(".nav-list1 .more").eq(0).addClass("show").children(".nav-list2").show();
        }
        if (!$(this).hasClass("active")) {
            $(".nav").hide();
            $(".nav-list1").find("li").removeClass("act");
        } else {
            if (winW > 1200) {
                var listMore = $(".nav-list1 .more");
                listMore.removeClass("show").children(".nav-list2").hide();
                listMore.eq(0).addClass("show").children(".nav-list2").fadeIn();
            }
            clearTimeout(oset);
            $(".nav-list1 >li").each(function(index, val) {
                var me = $(this);
                var num = $(this).index()
                oset = setTimeout(function() {
                    me.addClass("act");
                }, (index * 55))
            })
        }
    });
});
$(function() {
    var list1 = $(".nav-list1"),
        list2 = $(".nav-list2"),
        list3 = $(".nav-list3");
    list1.on("click", ".more", function(event) {
        if (winW > 1199) return;
        event.stopPropagation();
        event.preventDefault();
        $(".nav").addClass("left-100");
        var ostr = "";
        ostr = $(this).children(".nav-list2").html();
        ohref = $(this).children("a").clone(true);
        $(".nav-2 .content ul").html(ostr).children("li").has(".nav-list3").addClass("more");
        $(".nav-2 .nav-title").html(ohref);
    })
    $(".nav2-list2").on("click", "li", function(event) {
        if (winW > 1199) return;
        event.stopPropagation();
        if ($(this).hasClass("more")) {
            event.preventDefault();
            $(".nav").addClass("left-200");
            var ostr = "";
            ostr = $(this).children(".nav-list3").html();
            ohref = $(this).children("a").clone(true);
            console.log($(this).children("a"));
            $(".nav-3 .content ul").html(ostr);
            $(".nav-3 .nav-title").html(ohref);
        }
    })
    list1.on("mouseenter", ".more", function(event) {
        if (winW < 1200) return;
        var me2 = $(this).children(".nav-list2");
        me2
            .stop().slideDown("fast")
            .children("li").has(".nav-list3").addClass("more");
    }).on("mouseleave", ".more", function(event) {
        if (winW < 1200) return;
        $(this).children(".nav-list2").stop().slideUp("fast");
    })
    list2.on("mouseenter", "li", function(event) {
        if (winW < 1200) return;
        console.log($(this).children(".nav-list3"))
        $(this).children(".nav-list3").stop().slideDown("fast");
    }).on("mouseleave", "li", function(event) {
        if (winW < 1200) return;
        $(this).children(".nav-list3").stop().slideUp("fast");
    })
    $(".back-btn2").click(function() {
        $(".nav").removeClass("left-100");
    })
    $(".back-btn3").click(function() {
        $(".nav").removeClass("left-200");
    })
    //查找按钮
    $(".find").click(function(e) {
        if (e && e.stopPropagation) {
            //W3C取消冒泡事件
            e.stopPropagation();
        } else {
            //IE取消冒泡事件
            window.event.cancelBubble = true;
        }
        $(".search-lg").stop().fadeIn();
        $(".input-text").focus();
        $("body").addClass('searchactive');
        if (winW < 1200) {
            $("#btn").removeClass("active");
        }
    })
    $(".search-icon").click(function() {
        if (winW < 1200) {
            $(".search-xs").addClass("show")
        }
    })
    $(".nav").click(function(e) {
        if (!$(e.target).hasClass("input-text") && !$(e.target).hasClass("search-icon")) {
            console.log(e.target);
            $(".search-xs").removeClass("show")
        }
    })
    $(".close-btn").click(function() {
        $(".search-lg").fadeOut("fast");
        $("body").removeClass('searchactive');
    })
});
$(function() {
    if (!$.fn.slick) return;
    $('.slickbanner').slick({
        autoplay: true,
        autoplaySpeed: 4000, //以毫秒为单位的自动播放速度
        centerMode: true, //居中视图   slidesToShow为双数的时候慎用
        centerPadding: '0px', //左右两侧padding值
        arrows: false, //上一下，下一页
        fade: false, //启用淡入淡出
        dots: true, //显示点指示符
        speed: 500, //幻灯片/淡入淡出动画速度
        cssEase: 'ease', //CSS3动画缓和
        slidesToShow: 1, //显示的幻灯片数量
        slidesToScroll: 1, //要滚动的幻灯片数量
        focusOnSelect: true, //启用选定元素的焦点（单击）
        touchThreshold: 300, //滑动切换阈值，即滑动多少像素后切换
        infinite: true, //无限循环
        swipeToSlide: true, //允许用户将幻灯片直接拖动或滑动到幻灯片
        lazyLoad: 'ondemand', //接受'ondemand'或'progressive'<img data-lazy="img/lazyfonz1.png"/>
        variableWidth: false, //幻灯片宽度自适应
        adaptiveHeight: false, //自适应高度
        rows: 1, //将其设置为1以上将初始化网格模式。使用slidesPerRow设置每行应放置多少个幻灯片
        slidesPerRow: 1, //在通过行选项初始化网格模式时，这会设置每个网格行中的幻灯片数量
        pauseOnHover: false,
    });
    
});
//首页 banner
// $(function() {

//         // isMobile = getBrowser().isMobile;
//     // if (!banner.length) return;
//      $('.slickbanner').slick({
//         autoplay: true,
//         autoplaySpeed: 4000,
//         infinite: false,
//         fade: false,
//         speed: 500,
//         arrows: true,
//         dots: true,
//         slidesToShow: 1,
//         slidesToScroll: 1,
//         centerMode: false, //居中视图   slidesToShow为双数的时候慎用
//         //      centerPadding: '50px',
//         touchThreshold: 300,
//         lazyLoad: 'anticipated',
//         adaptiveHeight: false,
//         pauseOnHover: false,
//         responsive: [{
//             breakpoint: 1200,
//             settings: {
//                 arrows: false,
//                 dots: true,
//             }
//         }],
//     });
//     // var videoBox = $("#video-id");
//     // var bannerVideo = fluidPlayer(
//     //     'video-id', {
//     //         layoutControls: {
//     //             fillToContainer: true,
//     //             autoPlay: true,
//     //             playButtonShowing: true,
//     //             posterImage: videoBox.data("img"),
//     //             loop: true,
//     //             controlBar: {
//     //                 autoHide: true,
//     //                 autoHideTimeout: 3,
//     //                 animated: true
//     //             },
//     //         },
//     //         captions: {
//     //             play: '播放',
//     //             pause: '暂停',
//     //             mute: '静音',
//     //             unmute: '取消静音',
//     //             fullscreen: '全屏',
//     //             exitFullscreen: '退出全屏'
//     //         }
//     //     }
//     // );
//     // bannerVideo.on('ended', function() {
//     //     banner.slick('slickGoTo', 1);
//     // });
//     // banner.on('beforeChange', function(event, slick, currentSlide, nextSlide) {
//     //     var _this = $(this);
//     //     if (nextSlide === slick.slideCount - 1) {
//     //         banner.addClass("hide-dots");
//     //         banner.slick("slickPause");
//     //         if (!isMobile) {
//     //             bannerVideo.play();
//     //         }
//     //     } else {
//     //         banner.slick("slickPlay");
//     //         banner.removeClass("hide-dots");
//     //         bannerVideo.play();
//     //     }
//     // });
// });
//内页产品 banner
$(function() {
    // var banner = $('#slickproduct'),
    //     isMobile = getBrowser().isMobile;
    // if (!banner.length) return;
	if (!$.fn.slick) return;
     $('#slickproduct').slick({
        autoplay: false,
        autoplaySpeed: 4000,
        infinite: false,
        fade: false,
        speed: 500,
        arrows: true,
        dots: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        centerMode: false, //居中视图   slidesToShow为双数的时候慎用
        //      centerPadding: '50px',
        touchThreshold: 300,
        lazyLoad: 'anticipated',
        adaptiveHeight: false,
        pauseOnHover: false,
        responsive: [{
            breakpoint: 1200,
            settings: {
                arrows: false,
                dots: true,
            }
        }],
    });
    // var videoBox = $("#video-id");
    // var bannerVideo = fluidPlayer(
    //     'video-id', {
    //         layoutControls: {
    //             fillToContainer: true,
    //             autoPlay: true,
    //             playButtonShowing: true,
    //             posterImage: videoBox.data("img"),
    //             loop: true,
    //             controlBar: {
    //                 autoHide: true,
    //                 autoHideTimeout: 3,
    //                 animated: true
    //             },
    //         },
    //         captions: {
    //             play: '播放',
    //             pause: '暂停',
    //             mute: '静音',
    //             unmute: '取消静音',
    //             fullscreen: '全屏',
    //             exitFullscreen: '退出全屏'
    //         }
    //     }
    // );
    // bannerVideo.on('ended', function() {
    //     banner.slick('slickGoTo', 1);
    // });
    // banner.on('beforeChange', function(event, slick, currentSlide, nextSlide) {
    //     var _this = $(this);
    //     if (nextSlide === slick.slideCount - 1) {
    //         banner.addClass("hide-dots");
    //         banner.slick("slickPause");
    //         if (!isMobile) {
    //             bannerVideo.play();
    //         }
    //     } else {
    //         banner.slick("slickPlay");
    //         banner.removeClass("hide-dots");
    //         bannerVideo.play();
    //     }
    // });
});
// 首页产品
$(function() {
    var featured = $('.slick-product');
    if (featured.length === 0) return;
    //  console.log(owlChoose.length === 0)
    var btns = $(".box-categories .sort ul");
    // var eljson = {
    //     "page": [
    //         [{
    //             "url": "product_show.html",
    //             "img": "assets/images/img/categories-1.jpg",
    //             "name1": "Rotay Water Spray Retorts",
    //             "name2": "Innovaster is a fast growing company of committed people with more than 15 years experience and passion. Innovaster has three associate factories... ",
    //         }, {
    //             "url": "product_show.html",
    //             "img": "assets/images/img/categories-1.jpg",
    //             "name1": "Rotay Water Spray Retorts",
    //             "name2": "Innovaster is a fast growing company of committed people with more than 15 years experience and passion. Innovaster has three associate factories... ",
    //         }, {
    //             "url": "product_show.html",
    //             "img": "assets/images/img/categories-1.jpg",
    //             "name1": "Rotay Water Spray Retorts",
    //             "name2": "Innovaster is a fast growing company of committed people with more than 15 years experience and passion. Innovaster has three associate factories... ",
    //         }, {
    //             "url": "product_show.html",
    //             "img": "assets/images/img/categories-1.jpg",
    //             "name1": "Rotay Water Spray Retorts",
    //             "name2": "Innovaster is a fast growing company of committed people with more than 15 years experience and passion. Innovaster has three associate factories... ",
    //         }, {
    //             "url": "product_show.html",
    //             "img": "assets/images/img/categories-1.jpg",
    //             "name1": "Rotay Water Spray Retorts",
    //             "name2": "Innovaster is a fast growing company of committed people with more than 15 years experience and passion. Innovaster has three associate factories... ",
    //         }, {
    //             "url": "product_show.html",
    //             "img": "assets/images/img/categories-1.jpg",
    //             "name1": "Rotay Water Spray Retorts",
    //             "name2": "Innovaster is a fast growing company of committed people with more than 15 years experience and passion. Innovaster has three associate factories... ",
    //         }, ],
    //         [{
    //             "url": "product_show.html",
    //             "img": "assets/images/img/categories-1.jpg",
    //             "name1": "Rotay Water Spray Retorts2",
    //             "name2": "Innovaster is a fast growing company of committed people with more than 15 years experience and passion. Innovaster has three associate factories... ",
    //         }, {
    //             "url": "product_show.html",
    //             "img": "assets/images/img/categories-1.jpg",
    //             "name1": "Rotay Water Spray Retorts2",
    //             "name2": "Innovaster is a fast growing company of committed people with more than 15 years experience and passion. Innovaster has three associate factories... ",
    //         }, {
    //             "url": "product_show.html",
    //             "img": "assets/images/img/categories-1.jpg",
    //             "name1": "Rotay Water Spray Retorts2",
    //             "name2": "Innovaster is a fast growing company of committed people with more than 15 years experience and passion. Innovaster has three associate factories... ",
    //         }, {
    //             "url": "product_show.html",
    //             "img": "assets/images/img/categories-1.jpg",
    //             "name1": "Rotay Water Spray Retorts2",
    //             "name2": "Innovaster is a fast growing company of committed people with more than 15 years experience and passion. Innovaster has three associate factories... ",
    //         }, {
    //             "url": "product_show.html",
    //             "img": "assets/images/img/categories-1.jpg",
    //             "name1": "Rotay Water Spray Retorts2",
    //             "name2": "Innovaster is a fast growing company of committed people with more than 15 years experience and passion. Innovaster has three associate factories... ",
    //         }, {
    //             "url": "product_show.html",
    //             "img": "assets/images/img/categories-1.jpg",
    //             "name1": "Rotay Water Spray Retorts2",
    //             "name2": "Innovaster is a fast growing company of committed people with more than 15 years experience and passion. Innovaster has three associate factories... ",
    //         }, ],
    //     ],
    // };
    featured.slick({
        autoplay: true,
        autoplaySpeed: 3000, //以毫秒为单位的自动播放速度
        arrows: true,
        touchThreshold: 300, //滑动切换阈值，即滑动多少像素后切换
        slidesToShow: 4, //显示的幻灯片数量
        slidesToScroll: 1,
        infinite: true, //无限循环
        dots: false,
        lazyLoad: 'ondemand', //接受'ondemand'或'progressive'<img data-lazy="img/lazyfonz1.png"/>
        pauseOnHover: true, //悬停时暂停自动播放
        responsive: [{
                breakpoint: 991,
                settings: {
                    slidesToShow: 3,
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                }
            }
        ],
    });
    //滚动内容
    function content(index) {
        btns.find("li")
            .eq(index)
            .addClass("active")
            .siblings().removeClass("active");
        //判断传输过来的产品每一类是否不为0
        if (eljson.page[index]) {
            function contentStr(i) {
                var content = '<div><div><a class="item" href="' + eljson.page[index][i].url + '">';
                content += '<div class="pic"><div class="img-box"><img data-lazy="' + eljson.page[index][i].img + '" /></div><div class="mask"><p>' + eljson.page[index][i].name2 + '</p></div>';
                content += '</div><div class="text" href="' + eljson.page[index][i].url + '"><div class="note"><b>' + eljson.page[index][i].name1 + '</b>';
                content += '</div></div></a></div></div>';
                return content;
            }
            //根据响应式判断需要几个item
            var jsonLen = eljson.page[index].length;
            for (var i = 0; i < jsonLen; i++) {
                featured.slick('slickAdd', contentStr(i));
            }
        }
    }
    content(0);
    //点击切换内容
    btns.on("click", "li", function(event) {
        event.preventDefault();
        var $this = $(this);
        if (!$this.hasClass("active")) {
            //              if($this.has("a").length !== 0) return;
            var index = $this.index(),
                items = featured.find(".item");
            var len = items.length;
            for (var i = 0; i < items.length; i++) {
                featured.slick('slickRemove', len - 1);
                if (len !== 0) {
                    len--;
                }
            }
            content(index);
        }
    });
    var elprev = $(".prev", ".featured-btn"),
        elnext = $(".next", ".featured-btn");
    elprev.click(function() {
        featured.slick('slickPrev');
    })
    elnext.click(function() {
        featured.slick('slickNext');
    })
});
// 首页case
$(function() {
    if (!$.fn.slick) return;
    $('.slick-case').slick({
        autoplay: true,
        autoplaySpeed: 3000, //以毫秒为单位的自动播放速度
        // centerMode: true, //居中视图   slidesToShow为双数的时候慎用
        // centerPadding: '0px', //左右两侧padding值
        arrows: false, //上一下，下一页
        fade: false, //启用淡入淡出
        dots: false, //显示点指示符
        speed: 500, //幻灯片/淡入淡出动画速度
        cssEase: 'ease', //CSS3动画缓和
        slidesToShow: 3, //显示的幻灯片数量
        slidesToScroll: 1, //要滚动的幻灯片数量
        focusOnSelect: false, //启用选定元素的焦点（单击）
        touchThreshold: 300, //滑动切换阈值，即滑动多少像素后切换
        infinite: true, //无限循环
        // swipeToSlide: true, //允许用户将幻灯片直接拖动或滑动到幻灯片
        lazyLoad: 'ondemand', //接受'ondemand'或'progressive'<img data-lazy="img/lazyfonz1.png"/>
        variableWidth: false, //幻灯片宽度自适应
        adaptiveHeight: false, //自适应高度
        rows: 1, //将其设置为1以上将初始化网格模式。使用slidesPerRow设置每行应放置多少个幻灯片
        slidesPerRow: 1, //在通过行选项初始化网格模式时，这会设置每个网格行中的幻灯片数量
        pauseOnHover: false,
        responsive: [{
                breakpoint: 992,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                }
            }
        ],
    });
    var arrowsNum = $(".box-case .arrow"),
        elprev = arrowsNum.children(".prev"),
        elnext = arrowsNum.children(".next");
    elprev.click(function() {
        $('.slick-case').slick('slickPrev');
    });
    elnext.click(function() {
        $('.slick-case').slick('slickNext');
    });
});
//详情页切换
$(function() {
    if (!$.fn.slick) return;
    $('.carousel-wrap .slider-for').slick({
        autoplay: false,
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: false,
        infinite: false,
        centerMode: false,
        touchThreshold: 300,
        asNavFor: '.carousel-wrap .slider-nav'
    });
    var sliderNav = $('.carousel-wrap .slider-nav');
    sliderNav.slick({
        autoplay: false,
        slidesToShow: 4,
        slidesToScroll: 1,
        infinite: false,
        // centerMode: true,
        centerPadding: '0px',
        asNavFor: '.carousel-wrap .slider-for',
        dots: false,
        arrows: false,
        touchThreshold: 300,
        focusOnSelect: true,
        vertical: false,
        responsive: [{
            breakpoint: 992,
            settings: {
                vertical: false,
            }
        }],
    });
    // if ($.fn.imagezoom && winW > 991) {
    //     $('.carousel-wrap .slider-for img').imagezoom({
    //         offset: 10,
    //         xzoom: 400,
    //         yzoom: 400
    //     });
    // }
    if (sliderNav.slick('slickGetOption', 'slidesToShow') >= sliderNav.find(".slick-slide").length) {
        sliderNav.slick('slickSetOption', 'centerMode', false);
        sliderNav.find(".slick-track").addClass("transform-0");
    }
});
// 在线客服
$(function() {
    var code = $(".code-pic");
    $(".online .code").on("mouseenter", function() {
        if (winW > 991) {
            $(this).children(".mask").stop(true, true).fadeIn();
        } else {
            $(this).children(".code-pic").stop(true, true).fadeIn();
        }
    }).on("mouseleave", function() {
        if (winW > 991) {
            $(this).children(".mask").stop(true, true).fadeOut();
        } else {
            $(this).children(".code-pic").stop(true, true).fadeOut();
        }
    });
    code.on("mouseenter", function(e) {
        $(this).stop(true, true).fadeIn();
    }).on("mouseleave", function() {
        $(this).stop(true, true).fadeOut();
    });
    $(".online-wrap .btn").on("click", function() {
        $(this).toggleClass("active");
        $(".online").toggleClass("active");
    });
    //返回顶部按钮
    $("#gotop,.backtop").click(function() {
        $("html,body").animate({
            scrollTop: 0
        }, 500)
    })
})
$(function() {
    $('.icon-online').click(function() {
        $('.online').toggleClass('active');
        $('.icon-online').toggleClass('icon');
    });
});
// 放大
$(function() {
    $("a[rel=fancybox-product]").fancybox({
        'overlayShow': true,
        'overlayColor': '#000',
        'overlayOpacity': 0.9,
        'opacity': 0.5,
        'transitionIn': 'elastic',
        'transitionOut': 'none',
        'titlePosition': 'over',
        'showCloseButton': false,
        'titleFormat': function(title, currentArray, currentIndex, currentOpts) {
            return '<span id="fancybox-title-over">' + (currentIndex + 1) + ' / ' + currentArray.length + (title.length ? ' &nbsp; ' + title : '') + ' </span>';
        }
    });
});
// 手机底部
$(".footer .foot ul li .title-foot").click(function() {
    if ($win.width() < 1199) {
        var par = $(this).parent().parent();
        if (par.attr("class") == "on") {
            $(".footer .foot ul li .title-foot").parent().parent().addClass("on").find('.info-down').slideUp();
            par.find('.info-down').slideDown();
            par.removeClass("on").addClass("current").siblings().removeClass('current');
        } else {
            par.find('.info-down').slideUp();
            par.addClass("on").removeClass("current");
        }
    }
});
// 导航下拉
$(function() {
    $('.header .nav-down .nav-left > ul > li').mouseover(function() {
        var liindex = $('.header .nav-down .nav-left > ul > li').index(this);
        $(this).addClass('active').siblings().removeClass('active');
        $('.header .nav-down .nav-right .nav-list').eq(liindex).show().siblings('.header .nav-down .nav-right .nav-list').hide();
    });
});
// 产品详情询价点击
$(function() {
    $(".btn-inquiry").on("click", function() {
        $("html,body").animate({
            scrollTop: $("#inquiry").offset().top - 100
        }, 500)
    })
});
// 首页faq
$(".box-faq-news .faq .list>ul>li .title-faq").click(function() {
    var par = $(this).parent().parent();
    if (par.attr("class") == "on") {
        $(".box-faq-news .faq .list>ul>li .title-faq").parent().parent().addClass("on").find('.text').slideUp();
        par.find('.text').slideDown();
        par.removeClass("on").addClass("current").siblings().removeClass('current');
    } else {
        par.find('.text').slideUp();
        par.addClass("on").removeClass("current");
    }
}).eq(0).click();
$(".wrap-faq .faq .list>ul>li .title-faq").click(function() {
    var par = $(this).parent().parent();
    if (par.attr("class") == "on") {
        $(".wrap-faq .faq .list>ul>li .title-faq").parent().parent().addClass("on").find('.text').slideUp();
        par.find('.text').slideDown();
        par.removeClass("on").addClass("current").siblings().removeClass('current');
    } else {
        par.find('.text').slideUp();
        par.addClass("on").removeClass("current");
    }
}).eq(0).click();
// 产品详情询价点击
// $(".product-show .btn-inquiry").click(function() {
//     $(".inquiry-sort")
//         .addClass("active")
//         .siblings().removeClass("active");
//     $(".parameter .parameter-list").eq(2)
//         .show()
//         .siblings().hide("fast");
//     $("html,body").animate({
//         scrollTop: $('.parameter .parameter-sort li').offset().top - 150
//     }, 400)
// })
// // 产品详情相关产品点击
// $(".product-show .btn-relate").click(function() {
//     $(".relate-sort")
//         .addClass("active")
//         .siblings().removeClass("active");
//     $(".parameter .text").eq(2)
//         .show()
//         .siblings().hide("fast");
//     $("html,body").animate({
//         scrollTop: $('.parameter .sort li').offset().top - 150
//     }, 400)
// })
// $(function() {
//     $('.header  ul.nav-product li').mouseover(function() {
//         var liindex = $('.header ul.nav-product li').index(this);
//         $(this).addClass('active').siblings().removeClass('active');
//         $('.nav-text').eq(liindex).show().siblings('.nav-text').hide();
//     }).eq(0).mouseover();
// });
// $(".product-show .fun-btn .btn-relate").click(function() {
//     $(".relate-sort")
//         .addClass("active")
//         .siblings().removeClass("active");
//     $(".parameter .text").eq($('.wrap-product-show .parameter .sort>li').children(".active").index())
//         .show()
//         .siblings().hide("fast");
//     $("html,body").animate({
//         scrollTop: $('.wrap-product-show .parameter .sort>li').offset().top - 150
//     }, 400)
// })
$.fn.extend({
    'sameH': function(autoEl, resize) {
        var lis = this.find(autoEl),
            num = 0,
            oset = null;
        setTimeout(autoH, 500);
        $(window).on("load resize", function() {
            clearTimeout(oset);
            oset = setTimeout(autoH, 50);
        });

        function autoH() {
            if (winW > resize) {
                lis.css("height", "auto");
                num = 0;
                lis.each(function() {
                    num = Math.max(num, $(this).height());
                })
                lis.height(num);
            } else {
                lis.height("auto");
            }
        };
    }
});
$(function() {
    if (winW > 1199) {}
    if (winW > 767) {
        // $(".box-choose .choose").sameH(".item", 220);
    }
});
// 产品侧面导航有二级加class名
// $(function() {
//     var tags = $(".sidenav>ul>li").length;
//     // console.log(tags);
//     for (var i = 0; i <= tags; i++) {
//         var tags1 = $(".sidenav>ul>li").eq(i).find("li").length;
//         if (tags1 > 0) {
//             $(".sidenav>ul>li").eq(i).addClass("more");
//         }
//     }
// });
// 表格
$(function() {
    var oTable = $("table");
    if (oTable.length !== 0) {
        var oTr = oTable.find('tr'),
            oTd = oTable.find('td');
        oTable.wrap("<div class='table-box'></div>");
        oTr.attr("style", "");
        oTd.each(function(index) {
            if (typeof($(this).attr("style")) !== "undefined") {
                if ($(this).attr("style").indexOf("text-align: center") >= 0) {
                    $(this).attr("style", "text-align: center");
                } else {
                    $(this).attr("style", "");
                }
            }
        })
    }
});
// 缓慢滑到指定id
$(".smooth").click(function() {
    var href = $(this).attr("href");
    var pos = $(href).offset().top - 30;
    $("html,body").animate({ scrollTop: pos }, 500);
    return false;
});
$(function() {
    if (!placeholderSupport()) { // 判断浏览器是否支持 placeholder
        $('[placeholder]').focus(function() {
            var input = $(this);
            if (input.val() == input.attr('placeholder')) {
                input.val('');
                input.removeClass('placeholder');
            }
        }).blur(function() {
            var input = $(this);
            if (input.val() == '' || input.val() == input.attr('placeholder')) {
                input.addClass('placeholder');
                input.val(input.attr('placeholder'));
            }
        }).blur();
    };
})

function placeholderSupport() {
    return 'placeholder' in document.createElement('input');
}
$(function() {
    $('.inquire-close').click(function() {
        $('.inquire-sheet-box').hide();
        $('.cart-icon').show();
    });
    $('.cart-icon').click(function() {
        $('.inquire-sheet-box').show();
        $('.cart-icon').hide();
    });
});
$(function() {
    $('.inquire-close').click(function() {
        $('.inquire-sheet-box').hide();
        $('.cart-icon').show();
    });
    $('.cart-icon').click(function() {
        $('.inquire-sheet-box').show();
        $('.cart-icon').hide();
    });
});
// 加入购物车
$(function() {
    var tst = $(".cart span").text();
    $(".addcart").on("click", function() {
        if ($(this).data(".cart") != "has") {
            tst = parseInt(tst) + 1;
            $(".cart span").text(tst)
        }
        $(this).data(".cart", "has");
    })
});
// // 产品详情table加减数量按钮
// $(function() {
//     var iptNum = 0;
//     $(".add1").on("click", function() {
//         iptNum = parseInt($(this).siblings(".ipt-num").val());
//         $(this).siblings(".ipt-num").val(iptNum + 1);
//     });
//     $(".del1").on("click", function() {
//         iptNum = parseInt($(this).siblings(".ipt-num").val());
//         iptNum--;
//         if (iptNum < 1) {
//             iptNum = 1;
//         }
//         $(this).siblings(".ipt-num").val(iptNum);
//     })
// })


$(function() {
    var iptNum = 0;
    $(".add1").on("click", function() {
        iptNum = parseInt($(this).siblings(".ipt-num").val());
        $(this).siblings(".ipt-num").val(iptNum + 1).trigger('input');
    })
    $(".del1").on("click", function() {
        iptNum = parseInt($(this).siblings(".ipt-num").val());
        iptNum--;
        if(iptNum < 1) {
            iptNum = 1;
        }
        $(this).siblings(".ipt-num").val(iptNum).trigger('input');
    })
});


// inquiry页面增减
$(function() {
    totl();
    adddel()
    //全选
    $("#all").click(function() {
        all = $(this).prop("checked")
        $(".Each").each(function() {
            $(this).prop("checked", all);
        })
    })
    //删除当前行
})
//合计
function totl() {
    var sum = 0;
    $(".totle").each(function() {
        sum += parseFloat($(this).text());
        $("#susum").text(sum);
    })
}

function adddel() {
    //小计和加减
    //加
    $(".add").each(function() {
        $(this).click(function() {
            var $multi = 0;
            var vall = $(this).prev().val();
            vall++;
            $(this).prev().val(vall);
            $multi = parseFloat(vall) * parseFloat($(this).parent().prev().text());
            totl();
        })
    })
    //减
    $(".reduc").each(function() {
        $(this).click(function() {
            var $multi1 = 0;
            var vall1 = $(this).next().val();
            vall1--;
            if (vall1 <= 0) {
                vall1 = 1;
            }
            $(this).next().val(vall1);
            $multi1 = parseFloat(vall1) * parseFloat($(this).parent().prev().text());
            totl();
        })
    })
}

// function getBrowser() {
//     var ua = navigator.userAgent.toLowerCase();
//     var btypeInfo = (ua.match(/firefox|chrome|safari|opera/g) || "other")[0];
//     if ((ua.match(/msie|trident/g) || [])[0]) {
//         btypeInfo = "msie";
//     }
//     var pc = "";
//     var prefix = "";
//     var plat = "";
//     //如果没有触摸事件 判定为PC
//     var isTocuh = ("ontouchstart" in window) || (ua.indexOf("touch") !== -1) || (ua.indexOf("mobile") !== -1);
//     if (isTocuh) {
//         if (ua.indexOf("ipad") !== -1) {
//             pc = "pad";
//         } else if (ua.indexOf("mobile") !== -1) {
//             pc = "mobile";
//         } else if (ua.indexOf("android") !== -1) {
//             pc = "androidPad";
//         } else {
//             pc = "pc";
//         }
//     } else {
//         pc = "pc";
//     }
//     switch (btypeInfo) {
//         case "chrome":
//         case "safari":
//         case "mobile":
//             prefix = "webkit";
//             break;
//         case "msie":
//             prefix = "ms";
//             break;
//         case "firefox":
//             prefix = "Moz";
//             break;
//         case "opera":
//             prefix = "O";
//             break;
//         default:
//             prefix = "webkit";
//             break
//     }
//     plat = (ua.indexOf("android") > 0) ? "android" : navigator.platform.toLowerCase();
//     return {
//         version: (ua.match(/[\s\S]+(?:rv|it|ra|ie)[\/: ]([\d.]+)/) || [])[1], //版本
//         plat: plat, //系统
//         type: btypeInfo, //浏览器
//         pc: pc,
//         prefix: prefix, //前缀
//         isMobile: (pc == "pc") ? false : true //是否是移动端
//     };
// };