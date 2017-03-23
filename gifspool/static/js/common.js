
// @formatter:off
/*inview.js*/
!function(t,e){"object"==typeof exports&&"object"==typeof module?module.exports=e():"function"==typeof define&&define.amd?define([],e):"object"==typeof exports?exports.inView=e():t.inView=e()}(this,function(){return function(t){function e(r){if(n[r])return n[r].exports;var i=n[r]={exports:{},id:r,loaded:!1};return t[r].call(i.exports,i,i.exports,e),i.loaded=!0,i.exports}var n={};return e.m=t,e.c=n,e.p="",e(0)}([function(t,e,n){"use strict";function r(t){return t&&t.__esModule?t:{"default":t}}var i=n(2),o=r(i);t.exports=o["default"]},function(t,e){function n(t){var e=typeof t;return null!=t&&("object"==e||"function"==e)}t.exports=n},function(t,e,n){"use strict";function r(t){return t&&t.__esModule?t:{"default":t}}Object.defineProperty(e,"__esModule",{value:!0});var i=n(9),o=r(i),u=n(3),f=r(u),s=n(4),c=function(){if("undefined"!=typeof window){var t=100,e=["scroll","resize","load"],n={history:[]},r={offset:{},threshold:0,test:s.inViewport},i=(0,o["default"])(function(){n.history.forEach(function(t){n[t].check()})},t);e.forEach(function(t){return addEventListener(t,i)}),window.MutationObserver&&addEventListener("DOMContentLoaded",function(){new MutationObserver(i).observe(document.body,{attributes:!0,childList:!0,subtree:!0})});var u=function(t){if("string"==typeof t){var e=[].slice.call(document.querySelectorAll(t));return n.history.indexOf(t)>-1?n[t].elements=e:(n[t]=(0,f["default"])(e,r),n.history.push(t)),n[t]}};return u.offset=function(t){if(void 0===t)return r.offset;var e=function(t){return"number"==typeof t};return["top","right","bottom","left"].forEach(e(t)?function(e){return r.offset[e]=t}:function(n){return e(t[n])?r.offset[n]=t[n]:null}),r.offset},u.threshold=function(t){return"number"==typeof t&&t>=0&&t<=1?r.threshold=t:r.threshold},u.test=function(t){return"function"==typeof t?r.test=t:r.test},u.is=function(t){return r.test(t,r)},u.offset(0),u}};e["default"]=c()},function(t,e){"use strict";function n(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}Object.defineProperty(e,"__esModule",{value:!0});var r=function(){function t(t,e){for(var n=0;n<e.length;n++){var r=e[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(t,r.key,r)}}return function(e,n,r){return n&&t(e.prototype,n),r&&t(e,r),e}}(),i=function(){function t(e,r){n(this,t),this.options=r,this.elements=e,this.current=[],this.handlers={enter:[],exit:[]},this.singles={enter:[],exit:[]}}return r(t,[{key:"check",value:function(){var t=this;return this.elements.forEach(function(e){var n=t.options.test(e,t.options),r=t.current.indexOf(e),i=r>-1,o=n&&!i,u=!n&&i;o&&(t.current.push(e),t.emit("enter",e)),u&&(t.current.splice(r,1),t.emit("exit",e))}),this}},{key:"on",value:function(t,e){return this.handlers[t].push(e),this}},{key:"once",value:function(t,e){return this.singles[t].unshift(e),this}},{key:"emit",value:function(t,e){for(;this.singles[t].length;)this.singles[t].pop()(e);for(var n=this.handlers[t].length;--n>-1;)this.handlers[t][n](e);return this}}]),t}();e["default"]=function(t,e){return new i(t,e)}},function(t,e){"use strict";function n(t,e){var n=t.getBoundingClientRect(),r=n.top,i=n.right,o=n.bottom,u=n.left,f=n.width,s=n.height,c={t:o,r:window.innerWidth-u,b:window.innerHeight-r,l:i},a={x:e.threshold*f,y:e.threshold*s};return c.t>e.offset.top+a.y&&c.r>e.offset.right+a.x&&c.b>e.offset.bottom+a.y&&c.l>e.offset.left+a.x}Object.defineProperty(e,"__esModule",{value:!0}),e.inViewport=n},function(t,e){(function(e){var n="object"==typeof e&&e&&e.Object===Object&&e;t.exports=n}).call(e,function(){return this}())},function(t,e,n){var r=n(5),i="object"==typeof self&&self&&self.Object===Object&&self,o=r||i||Function("return this")();t.exports=o},function(t,e,n){function r(t,e,n){function r(e){var n=x,r=m;return x=m=void 0,E=e,w=t.apply(r,n)}function a(t){return E=t,j=setTimeout(h,e),M?r(t):w}function l(t){var n=t-O,r=t-E,i=e-n;return _?c(i,g-r):i}function d(t){var n=t-O,r=t-E;return void 0===O||n>=e||n<0||_&&r>=g}function h(){var t=o();return d(t)?p(t):void(j=setTimeout(h,l(t)))}function p(t){return j=void 0,T&&x?r(t):(x=m=void 0,w)}function v(){void 0!==j&&clearTimeout(j),E=0,x=O=m=j=void 0}function y(){return void 0===j?w:p(o())}function b(){var t=o(),n=d(t);if(x=arguments,m=this,O=t,n){if(void 0===j)return a(O);if(_)return j=setTimeout(h,e),r(O)}return void 0===j&&(j=setTimeout(h,e)),w}var x,m,g,w,j,O,E=0,M=!1,_=!1,T=!0;if("function"!=typeof t)throw new TypeError(f);return e=u(e)||0,i(n)&&(M=!!n.leading,_="maxWait"in n,g=_?s(u(n.maxWait)||0,e):g,T="trailing"in n?!!n.trailing:T),b.cancel=v,b.flush=y,b}var i=n(1),o=n(8),u=n(10),f="Expected a function",s=Math.max,c=Math.min;t.exports=r},function(t,e,n){var r=n(6),i=function(){return r.Date.now()};t.exports=i},function(t,e,n){function r(t,e,n){var r=!0,f=!0;if("function"!=typeof t)throw new TypeError(u);return o(n)&&(r="leading"in n?!!n.leading:r,f="trailing"in n?!!n.trailing:f),i(t,e,{leading:r,maxWait:e,trailing:f})}var i=n(7),o=n(1),u="Expected a function";t.exports=r},function(t,e){function n(t){return t}t.exports=n}])});
// @formatter:on

$(document).ready(function() {

	//arrow to top
	if ($('.back-to-top').length) {
			var scrollTrigger = 100, // px
					backToTop = function () {
							var scrollTop = $(window).scrollTop();
							if (scrollTop > scrollTrigger) {
									$('.back-to-top').addClass('show');
							} else {
									$('.back-to-top').removeClass('show');
							}
					};
			backToTop();
			$(window).on('scroll', function () {
					backToTop();
			});
			$('.back-to-top').on('click', function (e) {
					e.preventDefault();
					$('html,body').animate({
							scrollTop: 0
					}, 700);
			});
	}

	var win = $(window);
	var loading = false;
	var scrollLoad = false;

	$(window).on("load", function(){
		scrollLoad = true;
	});

	var container = $('#grid');
	if (document.getElementById('grid-item') != null) {
		container.imagesLoaded(function(){
			container.masonry({
				itemSelector: '#grid-item'
			});
		});
	}

	function autoplayWrap(text){
		$autopplay.find('span').text(text);
		if (text === 'off'){
			$autopplay.removeClass('on').find('i').removeClass('fa-play').addClass('fa-stop');
		} else {
			$autopplay.addClass('on').find('i').removeClass('fa-stop').addClass('fa-play');
		}
	}

	var $autopplay = $("a.autoplay_btn");
	$autopplay.click(function() {
			var text = $(this).find('span').text();
			if(text === 'off') {
					autoplayWrap('on');
					$.cookie('autoplay', 'on', {expires: 1, path:'/'}); // set cookie
			} else {
					autoplayWrap('off');
					$.cookie('autoplay', null); // remove cookie
			}
			setTimeout(function () {
				location.reload();
			}, 200);
	});

	var aPlayGifs = false;
	var isHome = document.getElementById("is_home");

	if (isHome != undefined) {
		if($.cookie('autoplay') === 'on') { // If cookie exists
				autoplayWrap('on');
				aPlayGifs = true;
				autolplayGifs($('li#grid-item').length);
		}
	}

	// $(document).scroll(function() {
	// 	// End of the document reached?
	// 	var top = win.scrollTop();
	// 	if (isHome != undefined) {
	// 		var offset = 500;
	// 		if  (top >= $(document).height() - win.height() - offset && scrollLoad == true ) {
	// 			if(loading) return;
	// 			$('div.grid').append('<div class="loadmore"><span class="spinner"></span></div>');
	// 			setTimeout(function () {
	// 				getContent();
	// 			}, 10);
	// 			scrollLoad = false;
	// 			return scrollLoad;
	// 		}
	// 	} else {
	// 		var offset = 1000;
	// 		if  (top >= $(document).height() - win.height() - offset && scrollLoad == true ) {
	// 			if(loading) return;
	// 			$('body').append('<div class="loadmore"><span class="spinner"></span></div>');
	// 			setTimeout(function () {
	// 				getNextContent(getNextContent);
	// 			}, 100);
	// 			scrollLoad = false;
	// 			return scrollLoad;
	// 		}
	// 	}
	// });

	function getNextContent(cb) {
			$.ajax({
					url: lNextUrl,
					dataType: 'html',
					beforeSend: function () {
							loading = true;
					},
					success: function (data) {
							$("body .loadmore").remove();
							if (data != "") {
									$('body').append(data);
									loading = false;
									gifSizer($('.single-gif_viewer').length - 1);
									preloadImage();
									scrollLoad = true;
									if (typeof cb == 'function') {
											cb();
									}
									return scrollLoad;
							} else {
									$('body').append('<div class="end_content"></div>');
							}
							
					}
			});
	}

	function getContent() {
		$.ajax({
			url: 'data/data.json',
			dataType: 'json',
			beforeSend: function(){
					loading = true;
			},
			success: function(data) {
				var dataLength = data.length;
				if ( data == "" ) {
					$(".grid .loadmore").remove();
					$('div.grid').append('<div class="end_content">Конец</div>');
				} else {
					for(var i = 0; i < dataLength; i++) { 
						createContent(data, i);
					}
					autolplayGifs(dataLength);
					$(".grid .loadmore").remove();
					loading = false;
				}
			}
		});
	}

	function autolplayGifs(leng){

		if (aPlayGifs === true) {

			if ((typeof window.orientation !== "undefined") || (navigator.userAgent.indexOf('IEMobile') !== -1)) {
				$(document).scroll(function() {
					checkInView('li#grid-item', win.height()/2)
				});
			} else {

				var leng = leng;

				var $container = $('#grid');
				var $contItem = $('li#grid-item');

				var i = $('li#grid-item').length - leng;

				console.log(i);

				var colItem = $('#grid').find('li#grid-item').length;
				console.log(colItem);
				for ( i ; i < colItem; i++) {
					// add new images
					var item = '';
					var img = $('<img>', {
						'src': item,
						'class': 'gif-autoplay',
						'style': 'display:none;'
					});
					console.log(img);
					$('.gif_viewer a').eq(i).append( img );
					var parent = replaceToGif($('.gif_viewer a').eq(i).find('.gifplayer').attr("src"));
					$('.gif_viewer a').eq(i).find('.gif-autoplay').attr("src", parent);
					$('.gif_viewer').eq(i).find('.play-gif').hide();
					console.log(parent);
					// use ImagesLoaded
					$('.gif_viewer a').eq(i).find('.gif-autoplay').imagesLoaded()
						.progress( onProgress );
				}

			}
		}

	}

	function onProgress( imgLoad, image ) {
		var $item = $( image.img ).parent().parent(),
				spinner = $( image.img ).parent().parent().find('.spinner').css('visibility', 'hidden');
		console.log($item);
		$item.addClass('is-load');
		if ( !image.isLoaded ) {
			$item.addClass('is-broken');
		}
	}

	function onProgressSingle( imgLoad, image ) {
		var $item = $( image.img ).parent();
		console.log($item);
		$item.addClass('is-load');
		if ( !image.isLoaded ) {
			$item.addClass('is-broken');
		}
	}

	function createContent(data, i) {
		var obj = data;
		var gifImg = $('<img>', {
										'class': 'gifplayer',
										'src': obj[i].jpg
								});
		var gifImgA = $('<a href="' + obj[i].url + '"></a>');
		var gifPlay = $('<ins class="play-gif"></ins>');
		var gifSpinner = $('<span class="spinner"></span>');
		var aHtml = $('<div class="gif_viewer"></div>');
		gifImgA.append(gifImg, gifPlay, gifSpinner);
		aHtml.append(gifImgA);
		var itemTitleA = $('<a href="' + obj[i].url + '">' + obj[i].title + '</a>');
		var itemTitle = $('<div class="description__title"</div>');
		var heartDescr = $('<div class="description__heart"><ul class="gif_drop-mnu"><li><i class="fa fa-heart"></i><span>' + obj[i].counts + '</span></li><ul class="left-drop emoji_heart" data-gif-id="' + obj[i].id + '"><li data-action="shocked"><img src="img/emoji/shocked.svg" alt=""></li><li data-action="loved"><img src="img/emoji/loved.svg" alt=""></li><li data-action="funny"><img src="img/emoji/funny.svg" alt=""></li></ul></ul></div>');
		var shareDescr = $('<div class="description__share"><ul class="gif_drop-mnu"><li><i class="fa fa-share-alt"></i><span>share</span></li><ul class="share_gif" data-gif-id="' + obj[i].id + '"><li data-share="facebook">Facebook</li><li data-share="twitter">Twitter</li><li data-share="whatsapp">WhatsApp</li></ul></ul></div>');
		var itemDescr = $('<div class="gif_description"></div>');
		itemTitle.append(itemTitleA);
		itemDescr.append(itemTitle, heartDescr, shareDescr);
		var gifWrapper = $('<div class="gif_wrapper"></div>');
		gifWrapper.append(aHtml, itemDescr);
		var gridItem = $('<li id="grid-item" data-gif-id="' + obj[i].id + '"></li>');
		gridItem.append(gifWrapper);

		var newElems = $( gridItem ).css({ opacity: 0 });
		newElems.imagesLoaded(function(){
			newElems.animate({ opacity: 1 });
			container.masonry( 'appended', newElems, true );
			scrollLoad = true;
			return scrollLoad;
		});

		$('#grid').append(gridItem);
	};

	// var removeImg;

	// function removeGif(gif) {
	// 	var src = replaceToJpg($(gif).find('.gifplayer').attr("src"));
	// 	$(gif).find('.gifplayer').attr("src", src);
	// 	$(gif).find('a').addClass('noLink');
	// };

	if ((typeof window.orientation !== "undefined") || (navigator.userAgent.indexOf('IEMobile') !== -1)) {
		// if (aPlayGifs === false) {
		// 	$('.gif_viewer a').addClass('noLink');
		// }
		// $(document).on('click', '#grid .gif_viewer, #related_gifs .gif_viewer', (function() {
		// 				var src = replaceToGif($(this).find('.gifplayer').attr("src")),
		// 						spinner = $(this).parent().parent().find('.spinner');
		// 				$(this).find('.gifplayer').attr("src", src);
		// 				$(this).find('a').removeClass('noLink');
		// 				if ($(this).attr('data-loaded') != 1) {
		// 						$(this).attr('data-loaded', 1);
		// 						var preloadedImg = new Image();
		// 						preloadedImg.alt = '';
		// 						preloadedImg.src = src;
								
		// 						preloadedImg.onload = function() {
		// 							var div = document.createElement('img');
		// 							$('body').append($(div).attr({"src": src}).hide());
		// 							// $('body').append($(div).attr({"src": src}).hide());
		// 							spinner.css('visibility', 'hidden');
		// 						}
		// 				}
		// 				console.log(removeImg);
		// 				if ( removeImg != undefined) {
		// 					removeGif(removeImg);
		// 				}
		// 				removeImg = $(this);
		// 				return removeImg;
		// 		}));
	} else {

				$(document).on('mouseover', '#grid .gifplayer, #related_gifs .gifplayer', (function () {
						var src = replaceToGif($(this).attr("src")),
								spinner = $(this).parent().parent().find('.spinner');
						if ($(this).attr('data-loaded') != 1) {
								$(this).attr('data-loaded', 1);
								var preloadedImg = new Image();
								preloadedImg.alt = '';
								preloadedImg.src = src;
								
								preloadedImg.onload = function() {
									var div = document.createElement('img');
									$('body').append($(div).attr({"src": src}).hide());
									// $('body').append($(div).attr({"src": src}).hide());
									spinner.css('visibility', 'hidden');
								}
						}
						$(this).attr("src", src);
				}));

		$(document).on('mouseout', '#grid .gifplayer, #related_gifs .gifplayer', (function() {
						var src = replaceToJpg($(this).attr("src"));
						$(this).attr("src", src);
				}));
	}

	var isSingle = document.getElementById("is_single");

	console.log(isSingle);

	if (isSingle != undefined){
		preloadImage();
		$(window).load(gifSizer(0)); 
		$(window).resize(gifReSizer);
		checkInView('.single-gif_viewer', 0);
		$(document).scroll(function() {
			checkInView('.single-gif_viewer', 200);
		});
	}

	function preloadImage() {
		var img = $('.single-gif_viewer .gifplayer'),
				imgLeng = img.length - 1,
				spinner = img.parent().find('.spinner');
		console.log(imgLeng);

		for (var i = 0; i <= imgLeng; i++) {
			if ($(img).eq(i).attr('data-loaded') != 1) {
					var src = replaceToGif(img.eq(i).attr("src"));
					$(img).eq(i).attr('data-loaded', 1);
					$(img).eq(i).parent().find('.play-gif').css('visibility', 'hidden');
					var preloadedImg = new Image();
					preloadedImg.alt = '';
					preloadedImg.src = src;
					
					preloadedImg.onload = function() {
						var div = document.createElement('img');
						$('body').append($(div).attr({"src": src}).hide());
						// $('body').append($(div).attr({"src": src}).hide());
						spinner.css('visibility', 'hidden');
						var top = win.height();
						console.log(top, $(document).height());
						if ( top >= $(document).height()) {

							if(loading) return;
							$('body').append('<div class="loadmore"><span class="spinner"></span></div>');
							console.log('load');
							setTimeout(function () {
								getNextContent();
							}, 100);
							scrollLoad = false;
							return scrollLoad;

						}
					}
			}

		}

	}

	function checkInView(gif, offset) {
			var inOffset = offset;
			console.log(inOffset);
			inView.offset(inOffset);
			inView(gif).once('enter', function addInView(el) {
																	var src = replaceToGif($(el).find('.gifplayer').attr("src")),																	
																			spinner = $(el).find('.spinner');
																	$(el).find('.gifplayer').attr("src", src);
																	var img = $(el).find('.gifplayer');
																	$(el).find('.play-gif').css('visibility', 'hidden');
																	if (isHome != undefined) {
																		if ($(el).attr('data-loaded') != 1) {
																				$(el).attr('data-loaded', 1);
																				var preloadedImg = new Image();
																				preloadedImg.alt = '';
																				preloadedImg.src = src;
																				
																				preloadedImg.onload = function() {
																					var div = document.createElement('img');
																					$('body').append($(div).attr({"src": src}).hide());
																					// $('body').append($(div).attr({"src": src}).hide());
																					spinner.css('visibility', 'hidden');
																				}
																		}
																	}
																	if (isSingle != undefined){
																			var newUrl = $(el).data('url');
																			console.log(newUrl);
																			// window.history.pushState("object or string", "Title", newUrl);
																	}
																})
								 .once('exit',  function removeInView(el) {
																	var src = replaceToJpg($(el).find('.gifplayer').attr("src"));
																	$(el).find('.gifplayer').attr("src", src);
																	$(el).find('.play-gif').css('visibility', 'visible');
																});
	}

	$(".category_wrap").click(function() {
		$(this).toggleClass("on");
	});

	windowSize();

	function windowSize(){
		if ($(window).width() < '768' )
		{
			$('.category_wrap').find('.btn-main').parent().remove().prependTo('.category_wrap ul');
		}
	};

	$(window).load(windowSize); 
	$(window).resize(windowSize);

	//share, report and emoji click

	$( document ).on( "click", ".emoji_heart li, .single-emoji_heart li, .report_gif", function() {
		var act = $(this).data('action');
		var id = $(this).parent().data('gif-id');
		getEmoji(act, id);
	});

	function getEmoji(act, id){
			console.log(act, id);
			$.ajax({
					type: 'POST',
					url: id,
					data: act,
					beforeSend: function () {
					},
					success: function (data) {
						if (isSingle != undefined){
							$('.section--single[data-gif-id="' + id + '"]').find('li[data-action="' + act + '"]').addClass('active').find('span').text(data);
						} else {
							$('#grid-item[data-gif-id="' + id + '"]').find('.emoji_likes').addClass('active').find('span').text(data);
						}
					}
			});
	}

	var shareTitle = document.title;
	// var btnShareUrl = window.location.href;
	var btnShareUrl = 'http://gifak.backspark.net/';

	$( document ).on( "click", ".share_gif li", function(event) {
		event.preventDefault();
		var type = $(this).data('share');
		var id = $(this).parent().data('gif-id');
		shareGif(type, id);
	});

	function shareGif(type, id){
		switch (type) {
			case 'facebook':
				href = 'https://www.facebook.com/sharer/sharer.php?u=' + btnShareUrl + '&img=http://gifak.backspark.net/img/100.gif';
				return !window.open(href, 'Facebook', 'width=640,height=300');
				break;
			case 'twitter':
				href = 'http://twitter.com/intent/tweet?text=' + shareTitle + '&url='+ btnShareUrl;
				return !window.open(href, 'Twitter', 'width=640,height=300');
				break;
			case 'whatsapp':
				href = 'whatsapp://send?text='+ shareTitle +'%0A' + btnShareUrl;
				return !window.open(href, 'WhatsApp', 'width=640,height=300');
				break;
			case 'vkontakte':
				href = 'https://vk.com/share.php?url=' + btnShareUrl;
				return !window.open(href, 'Vkontakte', 'width=640,height=300');
				break;
			default:
				console.log("url");
		}
	}

	//SVG Fallback
	if(!Modernizr.svg) {
		$("img[src*='svg']").attr("src", function() {
			return $(this).attr("src").replace(".svg", ".png");
		});
	};

	$("img, a").on("dragstart", function(event) { event.preventDefault(); });

	var t = 0;

	function replaceToGif(str) {
			t++;
			return str.replace(/\.jpg$/, '.gif');
	}
	function replaceToJpg(str) {
			return str.replace(/\.gif$/, '.jpg');
	}

	function gifSizer(el) {
		var $contItem = $('.single-gif_viewer'),
				img = $contItem.eq(el).find('.gifplayer'),
				origWidth = img.data('original-width'),
				origHeight = img.data('original-height'),
				newHeight = 490,
				wrapWidth = img.parent().width(),
				winWidth = $(window).width();
		if ( $(window).height() < 500 ) {
			newHeight = $(window).height() - 40;
			var newWidth = Math.ceil(origWidth*(newHeight/origHeight));
			img.css({'height': newHeight + 'px', 'width': 'auto'});
			if ( origHeight <= origWidth ) {
				img.css({'height': 'auto', 'width': 'auto', 'max-width': newHeight + 'px'});
			}
		} else {
			if ( origHeight > origWidth ) {
				var newWidth = Math.ceil(origWidth*(newHeight/origHeight));
				img.css({'height': newHeight + 'px', 'width': newWidth + 'px'});
			} else {
				newHeight = $(window).height() - 40;
				img.css({'height': 'auto', 'width': '100%', 'max-width': wrapWidth + 'px'});
				if (img.height() > newHeight) {
					img.css({'height': 'auto', 'width': '100%', 'max-width': newHeight + 'px'});
				}
			}
		}		
		if ( wrapWidth < newWidth ) {
			img.css({'height': 'auto', 'width': '100%'});
		}
	}

	function gifReSizer() {
		var leng = $('.single-gif_viewer').length;
		console.log(leng);
		for (var i= 0; i<leng; i++) {
			gifSizer(i);
		}
	}

});
