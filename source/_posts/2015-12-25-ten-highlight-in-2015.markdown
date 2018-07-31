---
layout: post
title: "Ten highlights in 2015"
date: 2015-12-25 13:35:55 +1100
comments: true
categories: [life, diary]
---

像去年那样，选了十张2015的照片 来回顾一下这匆匆的一年 :)      
plus: 看了整整半个多小时，选了几十张，可惜不能一一放上了，选几张我帅一点的好了 ^^。        
**圣诞快乐**<i class="fa fa-heart"></i>   

<!--more-->
   


> Happy birthday! 虽然大条神经的你连忘记我的生日的事也做的出来，    
但也会给我一个印象深刻的生日，感谢漫漫成长路上有你温柔的陪伴。    
<img class="lazy" style="max-height:400px"   
data-original="/images/blog/151225_ten_highlight_2015/1.jpg">   


> 那天从北京考试回来，你来火车站接我，还画了小妆，   
虽然看到你一直嘲笑嫌弃你，但心里其实觉得好漂亮，挺有女人味的，    
还有一刹那心动的感觉，我的女王大人。      
<img class="lazy" style="max-height:530px"  
data-original="/images/blog/151225_ten_highlight_2015/3.jpg">   


> 怀念以前去你学校找你的日子，才不是因为你们学校有好多好吃的呢，    
但话说那酸菜鸡火锅和酥肉砂锅真是久久不能忘怀呀。    
这是你拍毕业照那天的自拍，明明马上也毕业各奔天涯，可两个人在一起的时候，总是不由自主笑得很开心呢。  
<img class="lazy" style="max-height:400px"  
data-original="/images/blog/151225_ten_highlight_2015/4.JPG">   


> 一起去吃小猪猪，话说女生对这种萌萌的东西真的是没有一点抵抗力，两个吃货。   
世界上哪有比和心爱的人一起吃好吃的更幸福的事呢。   
<img class="lazy" style="max-height:530px"  
data-original="/images/blog/151225_ten_highlight_2015/5.JPG">   


> 和我一起去看的乒超比赛，嘿嘿，虽然看啦啦队跳舞被你嫌弃，但在我的解说下你也看的津津有味。    
一想起在你的加油下，拿到学校单打和团体的冠军还是热血沸腾呢~        
<img class="lazy" style="max-height:400px"  
data-original="/images/blog/151225_ten_highlight_2015/6.JPG">   


> 一起爬的长城，短短的路途却有满满的回忆。   
当然还有那好美味的北京烤鸭，闭上眼睛都是那天下雨的味道。    
<img class="lazy" style="max-height:400px"  
data-original="/images/blog/151225_ten_highlight_2015/7.JPG">   


> 这个表情，一看就是在吃鱼酷吧，哈哈。每次都说要把每个味道尝个遍，   
但总是点了我们最爱的黄金酸辣，直到毕业的时候也只完成了三分之二的口味。   
希望在未来的某一天，可以和你一起解锁这个成就。      
<img class="lazy" style="max-height:530px"  
data-original="/images/blog/151225_ten_highlight_2015/8.JPG">   


> 第一次和你约会吃的猫眼披萨店，那时青涩的回忆现在还隐隐感觉的到，   
毕业时我们一起又去了一次，不知道当时的你有没有什么特别的感觉呢。       
<img class="lazy" style="max-height:400px"  
data-original="/images/blog/151225_ten_highlight_2015/9.JPG">   


> 和你一起去的农业观光园，一起荡的秋千，一起骑的脚踏车，甜蜜的回忆现在想起，却是那么的难以触及。    
最后你想去却来不及的采摘，有一天一定要和你一起完成。   
<img class="lazy" style="max-height:530px"  
data-original="/images/blog/151225_ten_highlight_2015/11.JPG">   


> 然后。。我们的合照就只有微信视频的截图了，我去了澳洲读书，没有我的日子希望你也和以前一样坚强开心，许愿明年的圣诞节，可以和你一起过，sorry.     
<img class="lazy" style="max-height:600px"  
data-original="/images/blog/151225_ten_highlight_2015/10.PNG">   


> In conclusion, 感谢晨晨去年一年的陪伴，   
看到一些照片的时候，回忆突然涌上心头，希望明年的圣诞节，不再一个人孤单流泪。      
(未完待续)   


[《Ten highlight in 2014》](/blog/20150106/ten-highlights-in-2014/)



<audio autoplay="autopaly" >
  <source src="http://opetwnn9x.bkt.clouddn.com/luck.mp3" type="audio/mp3" />
</audio>


<style type="text/css">
	body {
		background-color: dark;
		margin: 0px;
		overflow: hidden;
	}
</style>

<script type="text/javascript" src="/lib/3dsnow/ThreeCanvas.js"></script>
<script type="text/javascript" src="/lib/3dsnow/Snow.js"></script>
<script>

	var SCREEN_WIDTH = window.innerWidth;
	var SCREEN_HEIGHT = window.innerHeight;

	var container;

	var particle;

	var camera;
	var scene;
	var renderer;

	var mouseX = 0;
	var mouseY = 0;

	var windowHalfX = window.innerWidth / 2;
	var windowHalfY = window.innerHeight / 2;
	
	var particles = []; 
	var particleImage = new Image();//THREE.ImageUtils.loadTexture( "img/ParticleSmoke.png" );
	particleImage.src = '/images/blog/151225_ten_highlight_2015/ParticleSmoke.png'; 



	function initsnow() {

		container = document.createElement('div');
		document.body.appendChild(container);

		camera = new THREE.PerspectiveCamera( 75, SCREEN_WIDTH / SCREEN_HEIGHT, 1, 10000 );
		camera.position.z = 1000;

		scene = new THREE.Scene();
		scene.add(camera);
			
		renderer = new THREE.CanvasRenderer();
		renderer.setSize(SCREEN_WIDTH, SCREEN_HEIGHT);
		var material = new THREE.ParticleBasicMaterial( { map: new THREE.Texture(particleImage) } );
			
		for (var i = 0; i < 500; i++) {

			particle = new Particle3D( material);
			particle.position.x = Math.random() * 2000 - 1000;
			particle.position.y = Math.random() * 2000 - 1000;
			particle.position.z = Math.random() * 2000 - 1000;
			particle.scale.x = particle.scale.y =  1;
			scene.add( particle );
			
			particles.push(particle); 
		}

		container.appendChild( renderer.domElement );


		document.addEventListener( 'mousemove', onDocumentMouseMove, false );
		// document.addEventListener( 'touchstart', onDocumentTouchStart, false );
		// document.addEventListener( 'touchmove', onDocumentTouchMove, false );
		
		setInterval( loop, 1000 / 60 );
		
	}
	
	function onDocumentMouseMove( event ) {

		mouseX = event.clientX - windowHalfX;
		mouseY = event.clientY - windowHalfY;
	}

	function onDocumentTouchStart( event ) {

		if ( event.touches.length == 1 ) {

			event.preventDefault();

			mouseX = event.touches[ 0 ].pageX - windowHalfX;
			mouseY = event.touches[ 0 ].pageY - windowHalfY;
		}
	}

	function onDocumentTouchMove( event ) {

		if ( event.touches.length == 1 ) {

			event.preventDefault();

			mouseX = event.touches[ 0 ].pageX - windowHalfX;
			mouseY = event.touches[ 0 ].pageY - windowHalfY;
		}
	}

	//

	function loop() {

	for(var i = 0; i<particles.length; i++)
		{

			var particle = particles[i]; 
			particle.updatePhysics(); 

			with(particle.position)
			{
				if(y<-1000) y+=2000; 
				if(x>1000) x-=2000; 
				else if(x<-1000) x+=2000; 
				if(z>1000) z-=2000; 
				else if(z<-1000) z+=2000; 
			}				
		}
	
		camera.position.x += ( mouseX - camera.position.x ) * 0.05;
		camera.position.y += ( - mouseY - camera.position.y ) * 0.05;
		camera.lookAt(scene.position); 

		renderer.render( scene, camera );

		
	}

</script>

<script>
window.onload = function() {
  initsnow();
  	$("canvas").css("position", "fixed");
  	$("canvas").css("top", "0px");
  	$("canvas").css("left", "0px");
};

function remove_can(){
    $("canvas").remove();
    $("#close_button").hide();
}
	

</script>

<i id="close_button" onclick="remove_can()" style="position:fixed;right:25px;top:25px;z-index: 1300;cursor:pointer" class="fa fa-times fa-4"></i>

